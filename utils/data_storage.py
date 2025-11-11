"""データストレージモジュール"""
from typing import List, Dict, Optional
import pandas as pd
import streamlit as st
import json
import os


class DataStorage:
    """名刺データを管理するクラス"""

    # データファイルのパス
    DATA_DIR = "data"
    DATA_FILE = os.path.join(DATA_DIR, "business_cards.json")

    @staticmethod
    def initialize_session_state():
        """セッションステートを初期化"""
        if 'business_cards' not in st.session_state:
            st.session_state.business_cards = []

    @staticmethod
    def save_to_file():
        """
        セッションステートのデータをJSONファイルに保存
        """
        try:
            # データディレクトリが存在しない場合は作成
            if not os.path.exists(DataStorage.DATA_DIR):
                os.makedirs(DataStorage.DATA_DIR)

            # データをJSONファイルに保存
            DataStorage.initialize_session_state()
            cards = st.session_state.business_cards

            with open(DataStorage.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(cards, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            st.error(f"データの保存に失敗しました: {str(e)}")
            return False

    @staticmethod
    def load_from_file():
        """
        JSONファイルからデータを読み込んでセッションステートに設定
        """
        try:
            if os.path.exists(DataStorage.DATA_FILE):
                with open(DataStorage.DATA_FILE, 'r', encoding='utf-8') as f:
                    cards = json.load(f)

                DataStorage.initialize_session_state()
                st.session_state.business_cards = cards
                return True
            else:
                # ファイルが存在しない場合は空の状態で初期化
                DataStorage.initialize_session_state()
                return True
        except Exception as e:
            st.error(f"データの読み込みに失敗しました: {str(e)}")
            DataStorage.initialize_session_state()
            return False

    @staticmethod
    def add_card(card_data: Dict[str, str]):
        """
        名刺データを追加

        Args:
            card_data: 名刺データの辞書
        """
        DataStorage.initialize_session_state()
        st.session_state.business_cards.append(card_data)
        # 自動保存
        DataStorage.save_to_file()

    @staticmethod
    def get_all_cards() -> List[Dict[str, str]]:
        """
        すべての名刺データを取得

        Returns:
            名刺データのリスト
        """
        DataStorage.initialize_session_state()
        return st.session_state.business_cards

    @staticmethod
    def get_card(index: int) -> Optional[Dict[str, str]]:
        """
        指定されたインデックスの名刺データを取得

        Args:
            index: インデックス

        Returns:
            名刺データ（存在しない場合は None）
        """
        DataStorage.initialize_session_state()
        cards = st.session_state.business_cards
        if 0 <= index < len(cards):
            return cards[index]
        return None

    @staticmethod
    def update_card(index: int, card_data: Dict[str, str]) -> bool:
        """
        名刺データを更新

        Args:
            index: 更新する名刺のインデックス
            card_data: 新しい名刺データ

        Returns:
            更新が成功したかどうか
        """
        DataStorage.initialize_session_state()
        cards = st.session_state.business_cards
        if 0 <= index < len(cards):
            st.session_state.business_cards[index] = card_data
            # 自動保存
            DataStorage.save_to_file()
            return True
        return False

    @staticmethod
    def delete_card(index: int) -> bool:
        """
        名刺データを削除

        Args:
            index: 削除する名刺のインデックス

        Returns:
            削除が成功したかどうか
        """
        DataStorage.initialize_session_state()
        cards = st.session_state.business_cards
        if 0 <= index < len(cards):
            st.session_state.business_cards.pop(index)
            # 自動保存
            DataStorage.save_to_file()
            return True
        return False

    @staticmethod
    def clear_all_cards():
        """すべての名刺データをクリア"""
        st.session_state.business_cards = []
        # 自動保存
        DataStorage.save_to_file()

    @staticmethod
    def search_cards(query: str, fields: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        名刺データを検索

        Args:
            query: 検索クエリ
            fields: 検索対象のフィールドリスト（None の場合はすべてのフィールドを検索）

        Returns:
            検索結果のリスト
        """
        DataStorage.initialize_session_state()
        cards = st.session_state.business_cards

        if not query:
            return cards

        query_lower = query.lower()
        results = []

        for card in cards:
            if fields:
                # 指定されたフィールドのみを検索
                search_values = [str(card.get(field, "")) for field in fields]
            else:
                # すべてのフィールドを検索
                search_values = [str(value) for value in card.values()]

            # いずれかのフィールドにクエリが含まれているかチェック
            if any(query_lower in value.lower() for value in search_values):
                results.append(card)

        return results

    @staticmethod
    def to_dataframe() -> pd.DataFrame:
        """
        名刺データを DataFrame に変換

        Returns:
            DataFrame
        """
        DataStorage.initialize_session_state()
        cards = st.session_state.business_cards

        if not cards:
            # 空の DataFrame を返す
            return pd.DataFrame(columns=[
                "name", "name_kana", "company", "department", "position",
                "postal_code", "address_1", "address_2", "phone", "mobile", "fax", "email", "website"
            ])

        return pd.DataFrame(cards)

    @staticmethod
    def to_csv() -> str:
        """
        名刺データを CSV 形式に変換

        Returns:
            CSV 文字列
        """
        df = DataStorage.to_dataframe()
        return df.to_csv(index=False, encoding='utf-8-sig')

    @staticmethod
    def from_dataframe(df: pd.DataFrame):
        """
        DataFrame から名刺データをインポート

        Args:
            df: インポートする DataFrame
        """
        DataStorage.initialize_session_state()
        st.session_state.business_cards = df.to_dict('records')

    @staticmethod
    def get_card_count() -> int:
        """
        登録されている名刺の件数を取得

        Returns:
            名刺の件数
        """
        DataStorage.initialize_session_state()
        return len(st.session_state.business_cards)
