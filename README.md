# 📇 名刺管理アプリ

Cloud Vision API と Gemini API を活用した、名刺のOCR読み取り・管理アプリケーションです。

## 🚀 クイックスタート（初心者向け）

**初めての方はこちらから！**

### ⚡ 3ステップで始める

1. **セットアップスクリプトを実行**
   ```bash
   # Windows の場合
   setup.bat をダブルクリック

   # Mac / Linux の場合
   ./setup.sh
   ```

2. **APIキーを取得**（詳しくは [SETUP_GUIDE.md](SETUP_GUIDE.md) を参照）
   - [Gemini API キー](https://makersuite.google.com/app/apikey)
   - [Google Cloud 認証情報](https://console.cloud.google.com/)

3. **アプリを起動**
   ```bash
   # Windows の場合
   run.bat をダブルクリック

   # Mac / Linux の場合
   ./run.sh
   ```

**詳しい手順は → [📖 SETUP_GUIDE.md](SETUP_GUIDE.md) をご覧ください**

---

## ✨ 機能

- 📤 **名刺画像のアップロード** - PNG/JPG形式の名刺画像をアップロード
- 🔍 **OCR処理** - Cloud Vision API で画像からテキストを自動抽出
- 🤖 **AI解析** - Gemini API でテキストを文脈的に理解して構造化
- 📋 **データ管理** - 抽出された名刺情報の表示・編集・削除
- 🔎 **検索機能** - 名前、会社名、メールアドレスなどで検索
- 📥 **CSVエクスポート** - データをCSV形式でダウンロード
- 📊 **Google Sheets連携** - Google Sheetsへ直接エクスポート

## 🛠️ 使用技術

- **Streamlit** - Webアプリケーションフレームワーク
- **Cloud Vision API** - Google CloudのOCRサービス
- **Gemini API** - Google の生成AIモデル
- **Google Sheets API** - スプレッドシート連携
- **Python 3.9+**

## 📋 必要な準備

### 1. Google Cloud プロジェクトの設定

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. 以下のAPIを有効化：
   - Cloud Vision API
   - Google Sheets API
   - Google Drive API
3. サービスアカウントを作成し、JSON認証情報ファイルをダウンロード

### 2. Gemini API キーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. API キーを作成

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/streamlit-llm-app.git
cd streamlit-llm-app
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、APIキーを設定します。

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

### 4. アプリケーションの起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## 📖 使い方

### 名刺の登録

1. **📤 名刺登録** タブを選択
2. サイドバーで以下を設定：
   - Gemini API キーを入力
   - Google Cloud 認証情報（JSON）をアップロード
3. 名刺画像をアップロード
4. **🔍 OCR処理を実行** ボタンをクリック
5. 抽出された情報を確認・編集
6. **💾 保存** ボタンで登録完了

### データの閲覧・管理

- **📋 データ一覧** タブで登録済みの名刺を一覧表示
- 不要なデータは削除可能

### 検索

- **🔍 検索** タブでキーワード検索
- 検索対象フィールドを指定可能

### エクスポート

#### CSV形式でダウンロード

1. **⚡ エクスポート** タブを選択
2. **📥 CSV ファイルをダウンロード** ボタンをクリック

#### Google Sheets へエクスポート

1. **⚡ エクスポート** タブを選択
2. スプレッドシートURLを入力（または新規作成）
3. ワークシート名を指定
4. **📤 Google Sheets へエクスポート** ボタンをクリック

## 📂 プロジェクト構成

```
streamlit-llm-app/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 依存パッケージ
├── .env.example               # 環境変数のサンプル
├── README.md                  # このファイル
└── utils/                     # ユーティリティモジュール
    ├── __init__.py
    ├── vision_ocr.py          # Cloud Vision API 処理
    ├── gemini_analyzer.py     # Gemini API 解析処理
    ├── google_sheets.py       # Google Sheets 連携
    └── data_storage.py        # データ管理
```

## 🔧 トラブルシューティング

### Cloud Vision API のエラー

- Google Cloud Console で Cloud Vision API が有効化されているか確認
- サービスアカウントに適切な権限があるか確認
- 認証情報ファイルのパスが正しいか確認

### Gemini API のエラー

- API キーが正しく設定されているか確認
- [API 使用量の制限](https://ai.google.dev/pricing)を超えていないか確認

### Google Sheets 連携のエラー

- Google Sheets API と Google Drive API が有効化されているか確認
- スプレッドシートの共有設定でサービスアカウントのメールアドレスを編集者として追加

## 📝 抽出される情報

名刺から以下の情報を抽出します：

- 氏名（日本語・英語）
- 氏名の読み仮名
- 会社名
- 部署名
- 役職
- 郵便番号
- 住所
- 電話番号
- 携帯電話番号
- FAX番号
- メールアドレス
- ウェブサイトURL

## 🤝 貢献

プルリクエストを歓迎します！バグ報告や機能リクエストは、Issuesで受け付けています。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

## 🙏 謝辞

このアプリケーションは以下のAPIとライブラリを使用しています：

- [Streamlit](https://streamlit.io/)
- [Google Cloud Vision API](https://cloud.google.com/vision)
- [Google Gemini API](https://ai.google.dev/)
- [Google Sheets API](https://developers.google.com/sheets/api)

---

Made with ❤️ using Streamlit, Cloud Vision API, and Gemini API
