"""バッチ処理ユーティリティモジュール"""
from typing import List, Dict, Tuple, Optional
from io import BytesIO
from PIL import Image
import streamlit as st
import time
from datetime import datetime, timedelta

from utils.vision_ocr import VisionOCR
from utils.gemini_analyzer import GeminiAnalyzer


class BatchProcessor:
    """複数の名刺画像を一括処理するクラス"""

    def __init__(self, credentials_path: str, gemini_api_key: str):
        """
        BatchProcessor の初期化

        Args:
            credentials_path: Google Cloud 認証情報ファイルパス
            gemini_api_key: Gemini API キー
        """
        self.ocr = VisionOCR(credentials_path=credentials_path)
        self.analyzer = GeminiAnalyzer(api_key=gemini_api_key)
        self.results = []
        self.errors = []
        self.skipped = []
        self.processing_times = []

    def _supplement_postal_code(self, card_data: Dict[str, str]) -> Dict[str, str]:
        """
        郵便番号が空の場合、住所1から推測して補完

        Args:
            card_data: 名刺データ

        Returns:
            郵便番号が補完された名刺データ
        """
        if not card_data.get('postal_code') and card_data.get('address_1'):
            try:
                # Gemini APIを使って郵便番号を推測
                address = card_data['address_1']
                prompt = f"""以下の住所から郵便番号を推測してください。
郵便番号のみを「123-4567」の形式で回答してください。推測できない場合は空文字列を返してください。

住所: {address}

郵便番号:"""

                if self.analyzer.model:
                    response = self.analyzer.model.generate_content(prompt)
                    postal_code = response.text.strip()
                    # 郵便番号の形式チェック（XXX-XXXXまたはXXXXXXX）
                    import re
                    if re.match(r'^\d{3}-?\d{4}$', postal_code):
                        # ハイフンがなければ追加
                        if '-' not in postal_code:
                            postal_code = postal_code[:3] + '-' + postal_code[3:]
                        card_data['postal_code'] = postal_code
            except Exception as e:
                # 失敗しても処理は継続
                pass

        return card_data

    def _validate_card_data(self, card_data: Dict[str, str]) -> Tuple[bool, Optional[str]]:
        """
        名刺データのバリデーション

        Args:
            card_data: 名刺データ

        Returns:
            (有効かどうか, エラーメッセージ)
        """
        # 名前が空の場合はスキップ
        if not card_data.get('name') or card_data.get('name').strip() == '':
            return False, "名前が抽出できませんでした"

        return True, None

    def process_single_card(
        self,
        image_bytes: bytes,
        filename: str
    ) -> Tuple[bool, Optional[Dict[str, str]], Optional[str]]:
        """
        単一の名刺画像を処理

        Args:
            image_bytes: 画像のバイナリデータ
            filename: ファイル名

        Returns:
            (成功フラグ, 抽出データ, エラーメッセージ)
        """
        try:
            # OCR処理
            ocr_text = self.ocr.extract_text_from_image(image_bytes)

            if not ocr_text:
                return False, None, "OCR処理に失敗しました"

            # Gemini で解析
            card_data = self.analyzer.extract_business_card_info(ocr_text)

            if not card_data:
                return False, None, "名刺情報の抽出に失敗しました"

            # バリデーション
            is_valid, error_msg = self._validate_card_data(card_data)
            if not is_valid:
                return False, None, error_msg

            # 郵便番号の補完
            card_data = self._supplement_postal_code(card_data)

            # ファイル名を追加
            card_data['_filename'] = filename
            card_data['_ocr_text'] = ocr_text

            return True, card_data, None

        except Exception as e:
            return False, None, str(e)

    def process_batch_auto(
        self,
        uploaded_files: List,
        progress_callback=None,
        time_callback=None
    ) -> Dict[str, any]:
        """
        複数の名刺を自動で一括処理

        Args:
            uploaded_files: アップロードされたファイルのリスト
            progress_callback: 進捗状況を報告するコールバック関数
            time_callback: 予想終了時間を報告するコールバック関数

        Returns:
            処理結果の辞書 {
                'success_count': 成功件数,
                'error_count': エラー件数,
                'skipped_count': スキップ件数,
                'results': 成功したデータのリスト,
                'errors': エラー情報のリスト,
                'skipped': スキップされたファイルのリスト
            }
        """
        self.results = []
        self.errors = []
        self.skipped = []
        self.processing_times = []
        total = len(uploaded_files)
        start_time = time.time()

        for idx, uploaded_file in enumerate(uploaded_files):
            card_start_time = time.time()

            # 進捗報告と予想時間の計算
            if progress_callback:
                progress_callback(idx, total, uploaded_file.name)

            # 予想終了時間の計算
            if time_callback and idx > 0:
                avg_time = sum(self.processing_times) / len(self.processing_times)
                remaining_count = total - idx
                estimated_seconds = avg_time * remaining_count
                estimated_time = datetime.now() + timedelta(seconds=estimated_seconds)
                time_callback(estimated_time, estimated_seconds)

            # 画像を読み込み
            try:
                image = Image.open(uploaded_file)
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
            except Exception as e:
                self.errors.append({
                    'filename': uploaded_file.name,
                    'error': f"画像の読み込みエラー: {str(e)}"
                })
                continue

            # 処理実行
            success, card_data, error_msg = self.process_single_card(
                img_bytes,
                uploaded_file.name
            )

            # 処理時間を記録
            card_end_time = time.time()
            processing_time = card_end_time - card_start_time
            self.processing_times.append(processing_time)

            if success:
                self.results.append(card_data)
            else:
                # 名前がない場合はスキップとして記録
                if "名前が抽出できませんでした" in str(error_msg):
                    self.skipped.append({
                        'filename': uploaded_file.name,
                        'reason': error_msg
                    })
                else:
                    self.errors.append({
                        'filename': uploaded_file.name,
                        'error': error_msg
                    })

        # 最終進捗報告
        if progress_callback:
            progress_callback(total, total, "完了")

        return {
            'success_count': len(self.results),
            'error_count': len(self.errors),
            'skipped_count': len(self.skipped),
            'results': self.results,
            'errors': self.errors,
            'skipped': self.skipped
        }

    def get_results(self) -> List[Dict[str, str]]:
        """
        処理結果を取得

        Returns:
            成功した名刺データのリスト
        """
        return self.results

    def get_errors(self) -> List[Dict[str, str]]:
        """
        エラー情報を取得

        Returns:
            エラー情報のリスト
        """
        return self.errors

    def clear_results(self):
        """処理結果とエラー情報をクリア"""
        self.results = []
        self.errors = []
