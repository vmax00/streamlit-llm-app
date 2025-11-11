"""Gemini API を使用したテキスト解析モジュール"""
import json
import os
from typing import Optional, Dict
import google.generativeai as genai
import streamlit as st


class GeminiAnalyzer:
    """Gemini API を使用して OCR テキストを解析し、構造化データを抽出するクラス"""

    def __init__(self, api_key: Optional[str] = None):
        """
        GeminiAnalyzer の初期化

        Args:
            api_key: Gemini API キー
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None

    def initialize_model(self) -> bool:
        """
        Gemini モデルを初期化

        Returns:
            初期化が成功したかどうか
        """
        try:
            if not self.api_key:
                st.error("Gemini API キーが設定されていません。")
                return False

            genai.configure(api_key=self.api_key)
            # 利用可能な最新モデルを使用
            self.model = genai.GenerativeModel('gemini-pro')
            return True
        except Exception as e:
            st.error(f"Gemini モデルの初期化に失敗しました: {str(e)}")
            return False

    def extract_business_card_info(self, ocr_text: str) -> Optional[Dict[str, str]]:
        """
        OCR テキストから名刺情報を抽出

        Args:
            ocr_text: OCR で抽出されたテキスト

        Returns:
            構造化された名刺情報の辞書（失敗時は None）
        """
        if not self.model:
            if not self.initialize_model():
                return None

        try:
            # プロンプトを作成
            prompt = self._create_extraction_prompt(ocr_text)

            # Gemini API を呼び出し
            response = self.model.generate_content(prompt)

            # レスポンスをパース
            result = self._parse_response(response.text)

            return result

        except Exception as e:
            st.error(f"Gemini による解析中にエラーが発生しました: {str(e)}")
            return None

    def _create_extraction_prompt(self, ocr_text: str) -> str:
        """
        名刺情報抽出用のプロンプトを作成

        Args:
            ocr_text: OCR で抽出されたテキスト

        Returns:
            プロンプト文字列
        """
        prompt = f"""以下は名刺から OCR で抽出されたテキストです。
このテキストから、名刺情報を構造化して JSON 形式で抽出してください。

【抽出するフィールド】
- name: 氏名（日本語または英語）
- name_kana: 氏名の読み仮名（あれば）
- company: 会社名
- department: 部署名
- position: 役職
- postal_code: 郵便番号
- address: 住所
- phone: 電話番号（複数ある場合はカンマ区切り）
- mobile: 携帯電話番号
- fax: FAX番号
- email: メールアドレス
- website: ウェブサイトURL

【ルール】
1. 情報が見つからないフィールドは空文字列 "" を設定してください
2. 複数の値がある場合は、最も適切と思われるものを選択してください
3. 電話番号やFAX番号は、ハイフン付きの形式で出力してください
4. JSON形式のみを出力し、説明文は含めないでください
5. 文脈から判断して、適切にフィールドを割り当ててください

【OCRテキスト】
{ocr_text}

【出力形式】
以下のJSON形式で出力してください：
```json
{{
  "name": "山田太郎",
  "name_kana": "ヤマダタロウ",
  "company": "株式会社サンプル",
  "department": "営業部",
  "position": "部長",
  "postal_code": "123-4567",
  "address": "東京都渋谷区...",
  "phone": "03-1234-5678",
  "mobile": "090-1234-5678",
  "fax": "03-1234-5679",
  "email": "yamada@example.com",
  "website": "https://example.com"
}}
```

上記の形式で、抽出された情報をJSON形式のみで出力してください。
"""
        return prompt

    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """
        Gemini のレスポンスをパースして辞書形式に変換

        Args:
            response_text: Gemini からのレスポンステキスト

        Returns:
            パースされた名刺情報の辞書
        """
        try:
            # コードブロックがある場合は除去
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text.strip()

            # JSON をパース
            result = json.loads(json_text)

            # 必須フィールドを確保
            default_fields = {
                "name": "",
                "name_kana": "",
                "company": "",
                "department": "",
                "position": "",
                "postal_code": "",
                "address": "",
                "phone": "",
                "mobile": "",
                "fax": "",
                "email": "",
                "website": ""
            }

            # デフォルト値とマージ
            for key in default_fields:
                if key not in result:
                    result[key] = ""

            return result

        except json.JSONDecodeError as e:
            st.warning(f"JSONのパースに失敗しました: {str(e)}")
            st.info("生のレスポンス: " + response_text)

            # パースに失敗した場合は空の辞書を返す
            return {
                "name": "",
                "name_kana": "",
                "company": "",
                "department": "",
                "position": "",
                "postal_code": "",
                "address": "",
                "phone": "",
                "mobile": "",
                "fax": "",
                "email": "",
                "website": ""
            }
        except Exception as e:
            st.error(f"レスポンスの処理中にエラーが発生しました: {str(e)}")
            return {
                "name": "",
                "name_kana": "",
                "company": "",
                "department": "",
                "position": "",
                "postal_code": "",
                "address": "",
                "phone": "",
                "mobile": "",
                "fax": "",
                "email": "",
                "website": ""
            }
