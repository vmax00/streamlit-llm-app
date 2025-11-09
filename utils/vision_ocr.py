"""Cloud Vision API を使用した OCR 処理モジュール"""
import os
from typing import Optional
from google.cloud import vision
from google.oauth2 import service_account
import streamlit as st


class VisionOCR:
    """Cloud Vision API を使用して画像からテキストを抽出するクラス"""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        VisionOCR の初期化

        Args:
            credentials_path: Google Cloud サービスアカウントの認証情報ファイルパス
        """
        self.credentials_path = credentials_path
        self.client = None

    def initialize_client(self) -> bool:
        """
        Vision API クライアントを初期化

        Returns:
            初期化が成功したかどうか
        """
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
            else:
                # 環境変数から認証情報を取得
                self.client = vision.ImageAnnotatorClient()
            return True
        except Exception as e:
            st.error(f"Vision API クライアントの初期化に失敗しました: {str(e)}")
            return False

    def extract_text_from_image(self, image_content: bytes) -> Optional[str]:
        """
        画像からテキストを抽出

        Args:
            image_content: 画像のバイナリデータ

        Returns:
            抽出されたテキスト（失敗時は None）
        """
        if not self.client:
            if not self.initialize_client():
                return None

        try:
            image = vision.Image(content=image_content)

            # テキスト検出を実行
            response = self.client.text_detection(image=image)

            if response.error.message:
                raise Exception(response.error.message)

            texts = response.text_annotations

            if texts:
                # 最初の要素には全体のテキストが含まれる
                return texts[0].description
            else:
                return ""

        except Exception as e:
            st.error(f"OCR処理中にエラーが発生しました: {str(e)}")
            return None

    def extract_text_with_details(self, image_content: bytes) -> Optional[dict]:
        """
        画像からテキストと詳細情報を抽出

        Args:
            image_content: 画像のバイナリデータ

        Returns:
            抽出されたテキストと詳細情報の辞書（失敗時は None）
        """
        if not self.client:
            if not self.initialize_client():
                return None

        try:
            image = vision.Image(content=image_content)

            # テキスト検出を実行
            response = self.client.text_detection(image=image)

            if response.error.message:
                raise Exception(response.error.message)

            texts = response.text_annotations

            if not texts:
                return {"full_text": "", "blocks": []}

            result = {
                "full_text": texts[0].description,
                "blocks": []
            }

            # 各テキストブロックの詳細情報を取得
            for text in texts[1:]:  # 最初の要素はスキップ（全体テキスト）
                block = {
                    "text": text.description,
                    "confidence": getattr(text, 'confidence', None),
                    "bounds": self._get_bounds(text)
                }
                result["blocks"].append(block)

            return result

        except Exception as e:
            st.error(f"OCR処理中にエラーが発生しました: {str(e)}")
            return None

    @staticmethod
    def _get_bounds(text_annotation) -> dict:
        """
        テキストの境界ボックス座標を取得

        Args:
            text_annotation: Vision API のテキストアノテーション

        Returns:
            境界ボックスの座標辞書
        """
        vertices = text_annotation.bounding_poly.vertices
        return {
            "top_left": {"x": vertices[0].x, "y": vertices[0].y},
            "top_right": {"x": vertices[1].x, "y": vertices[1].y},
            "bottom_right": {"x": vertices[2].x, "y": vertices[2].y},
            "bottom_left": {"x": vertices[3].x, "y": vertices[3].y}
        }
