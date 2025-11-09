"""Google Sheets 連携モジュール"""
import os
from typing import Optional, List, Dict
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st


class GoogleSheetsManager:
    """Google Sheets との連携を管理するクラス"""

    # Google Sheets API と Google Drive API のスコープ
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self, credentials_path: Optional[str] = None):
        """
        GoogleSheetsManager の初期化

        Args:
            credentials_path: Google Cloud サービスアカウントの認証情報ファイルパス
        """
        self.credentials_path = credentials_path
        self.client = None

    def initialize_client(self) -> bool:
        """
        Google Sheets クライアントを初期化

        Returns:
            初期化が成功したかどうか
        """
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=self.SCOPES
                )
                self.client = gspread.authorize(credentials)
                return True
            else:
                st.error("Google Sheets の認証情報ファイルが見つかりません。")
                return False
        except Exception as e:
            st.error(f"Google Sheets クライアントの初期化に失敗しました: {str(e)}")
            return False

    def export_to_sheet(
        self,
        spreadsheet_url: str,
        worksheet_name: str,
        data: List[Dict[str, str]],
        append: bool = True
    ) -> bool:
        """
        名刺データを Google Sheets にエクスポート

        Args:
            spreadsheet_url: スプレッドシートの URL または ID
            worksheet_name: ワークシート名
            data: エクスポートするデータのリスト
            append: True の場合は既存データに追加、False の場合は上書き

        Returns:
            エクスポートが成功したかどうか
        """
        if not self.client:
            if not self.initialize_client():
                return False

        try:
            # スプレッドシートを開く
            if spreadsheet_url.startswith('http'):
                spreadsheet = self.client.open_by_url(spreadsheet_url)
            else:
                spreadsheet = self.client.open_by_key(spreadsheet_url)

            # ワークシートを取得または作成
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(
                    title=worksheet_name,
                    rows=1000,
                    cols=20
                )

            # データを準備
            if not data:
                st.warning("エクスポートするデータがありません。")
                return False

            # ヘッダー行を作成
            headers = list(data[0].keys())

            if append:
                # 既存のヘッダーをチェック
                existing_headers = worksheet.row_values(1)
                if not existing_headers:
                    # ヘッダーが存在しない場合は追加
                    worksheet.append_row(headers)

                # データ行を追加
                for item in data:
                    row = [item.get(header, "") for header in headers]
                    worksheet.append_row(row)
            else:
                # シートをクリアして新規作成
                worksheet.clear()
                worksheet.append_row(headers)

                # データ行を追加
                for item in data:
                    row = [item.get(header, "") for header in headers]
                    worksheet.append_row(row)

            st.success(f"Google Sheets へのエクスポートが完了しました: {worksheet_name}")
            return True

        except Exception as e:
            st.error(f"Google Sheets へのエクスポート中にエラーが発生しました: {str(e)}")
            return False

    def get_spreadsheet_data(
        self,
        spreadsheet_url: str,
        worksheet_name: str
    ) -> Optional[List[Dict[str, str]]]:
        """
        Google Sheets からデータを取得

        Args:
            spreadsheet_url: スプレッドシートの URL または ID
            worksheet_name: ワークシート名

        Returns:
            データのリスト（失敗時は None）
        """
        if not self.client:
            if not self.initialize_client():
                return None

        try:
            # スプレッドシートを開く
            if spreadsheet_url.startswith('http'):
                spreadsheet = self.client.open_by_url(spreadsheet_url)
            else:
                spreadsheet = self.client.open_by_key(spreadsheet_url)

            # ワークシートを取得
            worksheet = spreadsheet.worksheet(worksheet_name)

            # 全データを取得
            records = worksheet.get_all_records()

            return records

        except Exception as e:
            st.error(f"Google Sheets からのデータ取得中にエラーが発生しました: {str(e)}")
            return None

    def create_new_spreadsheet(
        self,
        title: str,
        worksheet_name: str = "名刺データ"
    ) -> Optional[str]:
        """
        新しいスプレッドシートを作成

        Args:
            title: スプレッドシートのタイトル
            worksheet_name: ワークシート名

        Returns:
            作成されたスプレッドシートの URL（失敗時は None）
        """
        if not self.client:
            if not self.initialize_client():
                return None

        try:
            # 新しいスプレッドシートを作成
            spreadsheet = self.client.create(title)

            # デフォルトのワークシート名を変更
            worksheet = spreadsheet.sheet1
            worksheet.update_title(worksheet_name)

            # スプレッドシートの URL を返す
            return spreadsheet.url

        except Exception as e:
            st.error(f"スプレッドシートの作成中にエラーが発生しました: {str(e)}")
            return None
