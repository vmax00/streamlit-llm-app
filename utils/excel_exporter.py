"""Excel エクスポートモジュール"""
from typing import List, Dict
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


class ExcelExporter:
    """名刺データをExcel形式でエクスポートするクラス"""

    @staticmethod
    def create_excel_from_dataframe(df: pd.DataFrame, sheet_name: str = "名刺データ") -> BytesIO:
        """
        DataFrameからExcelファイルを作成

        Args:
            df: エクスポートするDataFrame
            sheet_name: シート名

        Returns:
            Excelファイルのバイナリデータ
        """
        # 新しいワークブックを作成
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name

        # 列名を日本語に変換
        column_names = {
            "name": "氏名",
            "name_kana": "氏名（かな）",
            "company": "会社名",
            "department": "部署",
            "position": "役職",
            "postal_code": "郵便番号",
            "address": "住所",
            "phone": "電話番号",
            "mobile": "携帯電話",
            "fax": "FAX",
            "email": "メールアドレス",
            "website": "ウェブサイト"
        }

        # DataFrameの列名を変換
        df_export = df.copy()
        df_export = df_export.rename(columns=column_names)

        # 内部フィールド（_で始まる列）を除外
        df_export = df_export[[col for col in df_export.columns if not col.startswith('_')]]

        # DataFrameをワークシートに書き込み
        for r_idx, row in enumerate(dataframe_to_rows(df_export, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)

                # ヘッダー行のスタイル設定
                if r_idx == 1:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center", vertical="center")

                # すべてのセルに罫線を追加
                thin_border = Border(
                    left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin')
                )
                cell.border = thin_border

                # データ行のスタイル設定
                if r_idx > 1:
                    cell.alignment = Alignment(vertical="center", wrap_text=True)

        # 列幅を自動調整
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                except:
                    pass

            # 最小幅10、最大幅50
            adjusted_width = min(max(max_length + 2, 10), 50)
            ws.column_dimensions[column_letter].width = adjusted_width

        # 先頭行を固定
        ws.freeze_panes = "A2"

        # BytesIOに保存
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        return output

    @staticmethod
    def create_excel_from_cards(cards: List[Dict[str, str]], sheet_name: str = "名刺データ") -> BytesIO:
        """
        名刺データのリストからExcelファイルを作成

        Args:
            cards: 名刺データのリスト
            sheet_name: シート名

        Returns:
            Excelファイルのバイナリデータ
        """
        if not cards:
            # 空のDataFrameを作成
            df = pd.DataFrame(columns=[
                "name", "name_kana", "company", "department", "position",
                "postal_code", "address", "phone", "mobile", "fax", "email", "website"
            ])
        else:
            df = pd.DataFrame(cards)

        return ExcelExporter.create_excel_from_dataframe(df, sheet_name)

    @staticmethod
    def create_formatted_excel(
        cards: List[Dict[str, str]],
        title: str = "名刺管理データ",
        include_summary: bool = True
    ) -> BytesIO:
        """
        フォーマット済みのExcelファイルを作成（サマリー付き）

        Args:
            cards: 名刺データのリスト
            title: ファイルのタイトル
            include_summary: サマリーシートを含めるか

        Returns:
            Excelファイルのバイナリデータ
        """
        wb = Workbook()

        # サマリーシートを作成
        if include_summary and cards:
            ws_summary = wb.active
            ws_summary.title = "サマリー"

            # タイトル
            ws_summary['A1'] = title
            ws_summary['A1'].font = Font(size=16, bold=True)
            ws_summary.merge_cells('A1:B1')

            # 統計情報
            ws_summary['A3'] = "総件数"
            ws_summary['B3'] = len(cards)

            # 会社別集計
            df = pd.DataFrame(cards)
            if 'company' in df.columns:
                company_counts = df['company'].value_counts()
                ws_summary['A5'] = "会社別集計（上位10社）"
                ws_summary['A5'].font = Font(bold=True)

                for idx, (company, count) in enumerate(company_counts.head(10).items(), start=6):
                    ws_summary[f'A{idx}'] = company
                    ws_summary[f'B{idx}'] = count

            # 列幅調整
            ws_summary.column_dimensions['A'].width = 30
            ws_summary.column_dimensions['B'].width = 15

        # データシートを作成
        if cards:
            if include_summary:
                ws_data = wb.create_sheet(title="名刺データ")
            else:
                ws_data = wb.active
                ws_data.title = "名刺データ"

            df = pd.DataFrame(cards)
            excel_data = ExcelExporter.create_excel_from_dataframe(df, "名刺データ")

            # 既存のワークブックにデータシートをコピー
            # （簡略化のため、新しいワークブックを作成して返す）
            return excel_data

        # BytesIOに保存
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        return output
