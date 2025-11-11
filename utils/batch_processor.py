"""バッチ処理ユーティリティモジュール"""
from typing import List, Dict, Tuple, Optional
from io import BytesIO
from PIL import Image
import streamlit as st

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

            # ファイル名を追加
            card_data['_filename'] = filename
            card_data['_ocr_text'] = ocr_text

            return True, card_data, None

        except Exception as e:
            return False, None, str(e)

    def process_batch_auto(
        self,
        uploaded_files: List,
        progress_callback=None
    ) -> Dict[str, any]:
        """
        複数の名刺を自動で一括処理

        Args:
            uploaded_files: アップロードされたファイルのリスト
            progress_callback: 進捗状況を報告するコールバック関数

        Returns:
            処理結果の辞書 {
                'success_count': 成功件数,
                'error_count': エラー件数,
                'results': 成功したデータのリスト,
                'errors': エラー情報のリスト
            }
        """
        self.results = []
        self.errors = []
        total = len(uploaded_files)

        for idx, uploaded_file in enumerate(uploaded_files):
            # 進捗報告
            if progress_callback:
                progress_callback(idx, total, uploaded_file.name)

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

            if success:
                self.results.append(card_data)
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
            'results': self.results,
            'errors': self.errors
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
