"""名刺管理アプリ - メインアプリケーション"""
import os
import tempfile
from io import BytesIO
import streamlit as st
from PIL import Image
import pandas as pd

from utils.vision_ocr import VisionOCR
from utils.gemini_analyzer import GeminiAnalyzer
from utils.google_sheets import GoogleSheetsManager
from utils.data_storage import DataStorage
from utils.batch_processor import BatchProcessor


# ページ設定
st.set_page_config(
    page_title="名刺管理アプリ",
    page_icon="📇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """メインアプリケーション"""

    # セッションステートの初期化
    DataStorage.initialize_session_state()

    # ヘッダー
    st.markdown('<div class="main-header">📇 名刺管理アプリ</div>', unsafe_allow_html=True)

    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")

        # API設定
        st.subheader("API 設定")

        # Gemini API キー
        gemini_api_key = st.text_input(
            "Gemini API キー",
            type="password",
            help="Gemini API キーを入力してください",
            value=os.getenv("GEMINI_API_KEY", "")
        )

        # Google Cloud 認証情報
        credentials_file = st.file_uploader(
            "Google Cloud 認証情報 (JSON)",
            type=['json'],
            help="Cloud Vision API と Google Sheets API の認証情報ファイルをアップロードしてください"
        )

        # 認証情報を一時保存
        credentials_path = None
        if credentials_file:
            # クロスプラットフォーム対応：システムの一時ディレクトリを使用
            temp_dir = tempfile.gettempdir()
            credentials_path = os.path.join(temp_dir, "google_credentials.json")
            with open(credentials_path, 'wb') as f:
                f.write(credentials_file.getvalue())

        st.divider()

        # 統計情報
        st.subheader("📊 統計")
        card_count = DataStorage.get_card_count()
        st.metric("登録件数", f"{card_count} 件")

    # メインコンテンツ
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 名刺登録", "📦 一括処理", "📋 データ一覧", "🔍 検索", "⚡ エクスポート"])

    # タブ1: 名刺登録
    with tab1:
        st.header("名刺を登録")

        uploaded_file = st.file_uploader(
            "名刺画像をアップロード",
            type=['png', 'jpg', 'jpeg'],
            help="名刺の画像ファイルを選択してください"
        )

        if uploaded_file:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("アップロード画像")
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)

                # OCR処理ボタン
                if st.button("🔍 OCR処理を実行", type="primary", use_container_width=True):
                    if not credentials_path:
                        st.error("Google Cloud 認証情報をアップロードしてください。")
                    elif not gemini_api_key:
                        st.error("Gemini API キーを入力してください。")
                    else:
                        with st.spinner("名刺を解析しています..."):
                            # 画像をバイト配列に変換
                            img_byte_arr = BytesIO()
                            image.save(img_byte_arr, format='PNG')
                            img_bytes = img_byte_arr.getvalue()

                            # OCR処理
                            ocr = VisionOCR(credentials_path=credentials_path)
                            ocr_text = ocr.extract_text_from_image(img_bytes)

                            if ocr_text:
                                st.success("✅ OCR処理が完了しました")

                                # OCRテキストを表示
                                with st.expander("📝 抽出されたテキスト"):
                                    st.text(ocr_text)

                                # Gemini で解析
                                analyzer = GeminiAnalyzer(api_key=gemini_api_key)
                                card_data = analyzer.extract_business_card_info(ocr_text)

                                if card_data:
                                    st.session_state.current_card_data = card_data
                                    st.success("✅ 名刺情報の抽出が完了しました")
                                else:
                                    st.error("名刺情報の抽出に失敗しました。")
                            else:
                                st.error("OCR処理に失敗しました。")

            with col2:
                st.subheader("抽出された情報")

                if 'current_card_data' in st.session_state:
                    card_data = st.session_state.current_card_data

                    # フォームで編集可能にする
                    with st.form("card_form"):
                        col_a, col_b = st.columns(2)

                        with col_a:
                            name = st.text_input("氏名", value=card_data.get("name", ""))
                            name_kana = st.text_input("氏名（かな）", value=card_data.get("name_kana", ""))
                            company = st.text_input("会社名", value=card_data.get("company", ""))
                            department = st.text_input("部署", value=card_data.get("department", ""))
                            position = st.text_input("役職", value=card_data.get("position", ""))
                            postal_code = st.text_input("郵便番号", value=card_data.get("postal_code", ""))

                        with col_b:
                            address = st.text_area("住所", value=card_data.get("address", ""), height=100)
                            phone = st.text_input("電話番号", value=card_data.get("phone", ""))
                            mobile = st.text_input("携帯電話", value=card_data.get("mobile", ""))
                            fax = st.text_input("FAX", value=card_data.get("fax", ""))
                            email = st.text_input("メールアドレス", value=card_data.get("email", ""))
                            website = st.text_input("ウェブサイト", value=card_data.get("website", ""))

                        # 保存ボタン
                        submitted = st.form_submit_button("💾 保存", use_container_width=True, type="primary")

                        if submitted:
                            # データを保存
                            new_card_data = {
                                "name": name,
                                "name_kana": name_kana,
                                "company": company,
                                "department": department,
                                "position": position,
                                "postal_code": postal_code,
                                "address": address,
                                "phone": phone,
                                "mobile": mobile,
                                "fax": fax,
                                "email": email,
                                "website": website
                            }
                            DataStorage.add_card(new_card_data)
                            st.success(f"✅ {name} さんの名刺を保存しました！")
                            del st.session_state.current_card_data
                            st.rerun()
                else:
                    st.info("👆 画像をアップロードして、OCR処理を実行してください。")

    # タブ2: 一括処理
    with tab2:
        st.header("📦 複数名刺の一括処理")

        st.markdown("""
        複数の名刺画像を一度にアップロードして、自動または手動で処理できます。
        """)

        # 処理モード選択
        processing_mode = st.radio(
            "処理モード",
            ["🤖 自動一括処理", "👁️ 手動確認モード"],
            help="自動モード：すべて自動で処理して保存 / 手動モード：1枚ずつ確認しながら保存"
        )

        # 複数ファイルアップロード
        uploaded_files = st.file_uploader(
            "名刺画像をアップロード（複数選択可）",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="複数の名刺画像を一度に選択できます"
        )

        if uploaded_files:
            st.info(f"📂 {len(uploaded_files)} 枚の画像が選択されています")

            # 自動一括処理モード
            if processing_mode == "🤖 自動一括処理":
                st.subheader("自動一括処理")

                if st.button("🚀 すべて自動処理して保存", type="primary", use_container_width=True):
                    if not credentials_path:
                        st.error("Google Cloud 認証情報をアップロードしてください。")
                    elif not gemini_api_key:
                        st.error("Gemini API キーを入力してください。")
                    else:
                        # バッチプロセッサーを初期化
                        batch_processor = BatchProcessor(
                            credentials_path=credentials_path,
                            gemini_api_key=gemini_api_key
                        )

                        # プログレスバーとステータス表示
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def update_progress(current, total, filename):
                            progress = current / total if total > 0 else 0
                            progress_bar.progress(progress)
                            status_text.text(f"処理中: {current}/{total} - {filename}")

                        # 一括処理実行
                        with st.spinner("名刺を一括処理しています..."):
                            result = batch_processor.process_batch_auto(
                                uploaded_files,
                                progress_callback=update_progress
                            )

                        # 結果を表示
                        st.success(f"✅ 処理完了: 成功 {result['success_count']} 件 / エラー {result['error_count']} 件")

                        # 成功した名刺をデータベースに保存
                        if result['results']:
                            for card_data in result['results']:
                                # 内部フィールドを削除
                                clean_data = {k: v for k, v in card_data.items() if not k.startswith('_')}
                                DataStorage.add_card(clean_data)

                            st.balloons()
                            st.success(f"🎉 {len(result['results'])} 件の名刺を保存しました！")

                        # エラーがあれば表示
                        if result['errors']:
                            with st.expander(f"⚠️ エラー詳細 ({len(result['errors'])} 件)", expanded=True):
                                for error in result['errors']:
                                    st.error(f"**{error['filename']}**: {error['error']}")

                        # 処理結果のプレビュー
                        if result['results']:
                            with st.expander("📋 処理された名刺のプレビュー", expanded=True):
                                df = pd.DataFrame(result['results'])
                                # 内部フィールドを除外
                                display_df = df[[col for col in df.columns if not col.startswith('_')]]
                                st.dataframe(display_df, use_container_width=True)

            # 手動確認モード
            else:
                st.subheader("手動確認モード")
                st.info("1枚ずつ確認しながら処理します。各名刺の情報を編集してから保存できます。")

                # セッションステートで現在の処理インデックスを管理
                if 'batch_index' not in st.session_state:
                    st.session_state.batch_index = 0
                if 'batch_results' not in st.session_state:
                    st.session_state.batch_results = {}

                current_index = st.session_state.batch_index

                if current_index < len(uploaded_files):
                    current_file = uploaded_files[current_index]

                    st.write(f"**進捗:** {current_index + 1} / {len(uploaded_files)}")
                    progress_percentage = (current_index + 1) / len(uploaded_files)
                    st.progress(progress_percentage)

                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.subheader(f"📄 {current_file.name}")
                        image = Image.open(current_file)
                        st.image(image, use_container_width=True)

                        # OCR処理ボタン
                        if st.button("🔍 この名刺を処理", type="primary", use_container_width=True, key=f"process_{current_index}"):
                            if not credentials_path:
                                st.error("Google Cloud 認証情報をアップロードしてください。")
                            elif not gemini_api_key:
                                st.error("Gemini API キーを入力してください。")
                            else:
                                with st.spinner(f"名刺を解析しています... ({current_index + 1}/{len(uploaded_files)})"):
                                    # 画像をバイト配列に変換
                                    img_byte_arr = BytesIO()
                                    image.save(img_byte_arr, format='PNG')
                                    img_bytes = img_byte_arr.getvalue()

                                    # バッチプロセッサーで処理
                                    batch_processor = BatchProcessor(
                                        credentials_path=credentials_path,
                                        gemini_api_key=gemini_api_key
                                    )

                                    success, card_data, error_msg = batch_processor.process_single_card(
                                        img_bytes,
                                        current_file.name
                                    )

                                    if success:
                                        st.session_state.batch_results[current_index] = card_data
                                        st.success("✅ 名刺情報の抽出が完了しました")
                                    else:
                                        st.error(f"❌ エラー: {error_msg}")

                    with col2:
                        st.subheader("抽出された情報")

                        if current_index in st.session_state.batch_results:
                            card_data = st.session_state.batch_results[current_index]

                            # フォームで編集可能にする
                            with st.form(f"batch_card_form_{current_index}"):
                                col_a, col_b = st.columns(2)

                                with col_a:
                                    name = st.text_input("氏名", value=card_data.get("name", ""))
                                    name_kana = st.text_input("氏名（かな）", value=card_data.get("name_kana", ""))
                                    company = st.text_input("会社名", value=card_data.get("company", ""))
                                    department = st.text_input("部署", value=card_data.get("department", ""))
                                    position = st.text_input("役職", value=card_data.get("position", ""))
                                    postal_code = st.text_input("郵便番号", value=card_data.get("postal_code", ""))

                                with col_b:
                                    address = st.text_area("住所", value=card_data.get("address", ""), height=100)
                                    phone = st.text_input("電話番号", value=card_data.get("phone", ""))
                                    mobile = st.text_input("携帯電話", value=card_data.get("mobile", ""))
                                    fax = st.text_input("FAX", value=card_data.get("fax", ""))
                                    email = st.text_input("メールアドレス", value=card_data.get("email", ""))
                                    website = st.text_input("ウェブサイト", value=card_data.get("website", ""))

                                # ボタン
                                col_btn1, col_btn2, col_btn3 = st.columns(3)

                                with col_btn1:
                                    save_button = st.form_submit_button("💾 保存して次へ", use_container_width=True, type="primary")

                                with col_btn2:
                                    skip_button = st.form_submit_button("⏭️ スキップ", use_container_width=True)

                                with col_btn3:
                                    cancel_button = st.form_submit_button("❌ キャンセル", use_container_width=True)

                                if save_button:
                                    # データを保存
                                    new_card_data = {
                                        "name": name,
                                        "name_kana": name_kana,
                                        "company": company,
                                        "department": department,
                                        "position": position,
                                        "postal_code": postal_code,
                                        "address": address,
                                        "phone": phone,
                                        "mobile": mobile,
                                        "fax": fax,
                                        "email": email,
                                        "website": website
                                    }
                                    DataStorage.add_card(new_card_data)
                                    st.success(f"✅ {name} さんの名刺を保存しました！")

                                    # 次の名刺へ
                                    st.session_state.batch_index += 1
                                    if current_index in st.session_state.batch_results:
                                        del st.session_state.batch_results[current_index]
                                    st.rerun()

                                if skip_button:
                                    # スキップして次へ
                                    st.session_state.batch_index += 1
                                    if current_index in st.session_state.batch_results:
                                        del st.session_state.batch_results[current_index]
                                    st.rerun()

                                if cancel_button:
                                    # 処理をキャンセル
                                    st.session_state.batch_index = 0
                                    st.session_state.batch_results = {}
                                    st.warning("処理をキャンセルしました")
                                    st.rerun()

                        else:
                            st.info("👆 「この名刺を処理」ボタンをクリックしてOCR処理を開始してください")

                else:
                    # すべての処理が完了
                    st.success("🎉 すべての名刺の処理が完了しました！")
                    if st.button("🔄 最初から再開", use_container_width=True):
                        st.session_state.batch_index = 0
                        st.session_state.batch_results = {}
                        st.rerun()

    # タブ3: データ一覧
    with tab3:
        st.header("登録済み名刺一覧")

        cards = DataStorage.get_all_cards()

        if cards:
            df = DataStorage.to_dataframe()

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
            df_display = df.rename(columns=column_names)

            # データテーブルを表示
            st.dataframe(df_display, use_container_width=True, height=400)

            # 削除機能
            st.subheader("データ管理")
            col1, col2 = st.columns([3, 1])

            with col1:
                delete_index = st.selectbox(
                    "削除する名刺を選択",
                    options=range(len(cards)),
                    format_func=lambda x: f"{cards[x].get('name', '名前なし')} - {cards[x].get('company', '会社名なし')}"
                )

            with col2:
                st.write("")  # スペース調整
                st.write("")
                if st.button("🗑️ 削除", type="secondary"):
                    if DataStorage.delete_card(delete_index):
                        st.success("削除しました")
                        st.rerun()

            # 全削除ボタン
            if st.button("🗑️ すべてのデータを削除", type="secondary"):
                DataStorage.clear_all_cards()
                st.success("すべてのデータを削除しました")
                st.rerun()

        else:
            st.info("まだ名刺が登録されていません。")

    # タブ4: 検索
    with tab4:
        st.header("名刺検索")

        search_query = st.text_input(
            "🔍 検索キーワード",
            placeholder="名前、会社名、メールアドレスなど"
        )

        search_fields = st.multiselect(
            "検索対象フィールド（空の場合は全フィールド）",
            options=["name", "company", "department", "position", "email", "phone", "mobile"],
            format_func=lambda x: {
                "name": "氏名",
                "company": "会社名",
                "department": "部署",
                "position": "役職",
                "email": "メールアドレス",
                "phone": "電話番号",
                "mobile": "携帯電話"
            }.get(x, x)
        )

        if search_query:
            results = DataStorage.search_cards(
                search_query,
                fields=search_fields if search_fields else None
            )

            st.subheader(f"検索結果: {len(results)} 件")

            if results:
                for i, card in enumerate(results):
                    with st.expander(f"{card.get('name', '名前なし')} - {card.get('company', '会社名なし')}"):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(f"**氏名:** {card.get('name', '-')}")
                            st.write(f"**氏名（かな）:** {card.get('name_kana', '-')}")
                            st.write(f"**会社名:** {card.get('company', '-')}")
                            st.write(f"**部署:** {card.get('department', '-')}")
                            st.write(f"**役職:** {card.get('position', '-')}")
                            st.write(f"**郵便番号:** {card.get('postal_code', '-')}")

                        with col2:
                            st.write(f"**住所:** {card.get('address', '-')}")
                            st.write(f"**電話番号:** {card.get('phone', '-')}")
                            st.write(f"**携帯電話:** {card.get('mobile', '-')}")
                            st.write(f"**FAX:** {card.get('fax', '-')}")
                            st.write(f"**メール:** {card.get('email', '-')}")
                            st.write(f"**ウェブサイト:** {card.get('website', '-')}")
            else:
                st.warning("検索結果が見つかりませんでした。")

    # タブ5: エクスポート
    with tab5:
        st.header("データエクスポート")

        cards = DataStorage.get_all_cards()

        if cards:
            # CSV エクスポート
            st.subheader("📥 CSV ダウンロード")
            csv_data = DataStorage.to_csv()

            st.download_button(
                label="📥 CSV ファイルをダウンロード",
                data=csv_data,
                file_name="business_cards.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.divider()

            # Google Sheets エクスポート
            st.subheader("📊 Google Sheets へエクスポート")

            if not credentials_path:
                st.warning("Google Sheets へのエクスポートには、Google Cloud 認証情報が必要です。")
            else:
                spreadsheet_url = st.text_input(
                    "スプレッドシート URL",
                    placeholder="https://docs.google.com/spreadsheets/d/...",
                    help="既存のスプレッドシートの URL を入力してください（新規作成も可能）"
                )

                worksheet_name = st.text_input(
                    "ワークシート名",
                    value="名刺データ",
                    help="エクスポート先のワークシート名"
                )

                append_mode = st.checkbox("既存データに追加", value=True)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("📤 Google Sheets へエクスポート", type="primary", use_container_width=True):
                        if not spreadsheet_url:
                            st.error("スプレッドシート URL を入力してください。")
                        else:
                            with st.spinner("エクスポート中..."):
                                sheets_manager = GoogleSheetsManager(credentials_path=credentials_path)
                                success = sheets_manager.export_to_sheet(
                                    spreadsheet_url=spreadsheet_url,
                                    worksheet_name=worksheet_name,
                                    data=cards,
                                    append=append_mode
                                )
                                if success:
                                    st.balloons()

                with col2:
                    if st.button("📝 新規スプレッドシート作成", use_container_width=True):
                        title = st.text_input(
                            "新規スプレッドシートのタイトル",
                            value="名刺管理"
                        )
                        if title:
                            with st.spinner("スプレッドシートを作成中..."):
                                sheets_manager = GoogleSheetsManager(credentials_path=credentials_path)
                                new_url = sheets_manager.create_new_spreadsheet(
                                    title=title,
                                    worksheet_name=worksheet_name
                                )
                                if new_url:
                                    st.success(f"✅ スプレッドシートを作成しました！")
                                    st.markdown(f"[スプレッドシートを開く]({new_url})")

        else:
            st.info("エクスポートするデータがありません。")

    # フッター
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #888;'>
        Powered by Cloud Vision API & Gemini API | Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
