# 📖 初心者向けセットアップガイド

名刺管理アプリを使い始めるための詳しい手順を説明します。

## 🖥️ 前提条件

### Pythonのインストール確認

このアプリを動かすには **Python 3.9以上** が必要です。

#### Pythonがインストールされているか確認する方法

**Windows の場合:**
1. スタートメニューを開く
2. 「cmd」と入力してコマンドプロンプトを開く
3. 以下のコマンドを入力して Enter キーを押す

```bash
python --version
```

**Mac / Linux の場合:**
1. アプリケーション → ユーティリティ → ターミナル を開く
2. 以下のコマンドを入力して Enter キーを押す

```bash
python3 --version
```

**結果の見方:**
- `Python 3.9.0` のような表示が出れば OK です
- `'python' は、内部コマンドまたは外部コマンド...` と出た場合は、Pythonをインストールする必要があります

#### Pythonのインストール方法

**Python がインストールされていない場合:**

1. [Python公式サイト](https://www.python.org/downloads/) にアクセス
2. 「Download Python」ボタンをクリック
3. ダウンロードしたファイルを実行
4. **重要:** インストール時に「Add Python to PATH」にチェックを入れる
5. 「Install Now」をクリック

---

## 📥 STEP 1: プロジェクトファイルをダウンロード

### 方法1: GitHubからクローン（推奨）

**Gitがインストールされている場合:**

```bash
git clone https://github.com/vmax00/streamlit-llm-app.git
cd streamlit-llm-app
```

### 方法2: ZIPファイルでダウンロード

1. GitHubのプロジェクトページを開く
2. 緑色の「Code」ボタンをクリック
3. 「Download ZIP」を選択
4. ダウンロードしたZIPファイルを解凍
5. 解凍したフォルダを分かりやすい場所（デスクトップなど）に移動

---

## 📂 STEP 2: ターミナル/コマンドプロンプトでプロジェクトフォルダを開く

### Windows の場合

**方法1: エクスプローラーから開く（簡単）**
1. エクスプローラーで `streamlit-llm-app` フォルダを開く
2. アドレスバー（フォルダのパスが表示されている部分）をクリック
3. 「cmd」と入力して Enter キーを押す
4. → コマンドプロンプトがそのフォルダで開きます

**方法2: コマンドで移動**
1. スタートメニュー → 「cmd」と入力してコマンドプロンプトを開く
2. 以下のようにフォルダの場所まで移動します

```bash
# 例: デスクトップにある場合
cd Desktop\streamlit-llm-app

# 例: ダウンロードフォルダにある場合
cd Downloads\streamlit-llm-app
```

### Mac / Linux の場合

**方法1: Finderから開く（Mac）**
1. Finderで `streamlit-llm-app` フォルダを開く
2. Finderメニュー → サービス → フォルダに新規ターミナル

**方法2: コマンドで移動**
1. ターミナルを開く
2. 以下のようにフォルダの場所まで移動します

```bash
# 例: デスクトップにある場合
cd ~/Desktop/streamlit-llm-app

# 例: ダウンロードフォルダにある場合
cd ~/Downloads/streamlit-llm-app
```

### 確認方法

正しいフォルダにいるか確認するには:

```bash
# Windows
dir

# Mac / Linux
ls
```

`app.py` や `requirements.txt` などのファイルが表示されれば OK です！

---

## 🔧 STEP 3: 仮想環境を作成する（推奨）

仮想環境を使うと、このプロジェクト専用のPython環境を作れます。

### Windows の場合

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
venv\Scripts\activate
```

### Mac / Linux の場合

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate
```

**成功すると:**
- コマンドラインの先頭に `(venv)` と表示されます
- 例: `(venv) C:\Users\YourName\streamlit-llm-app>`

**注意:**
- 仮想環境を終了するには `deactivate` と入力します
- アプリを起動する際は、毎回仮想環境を有効化する必要があります

---

## 📦 STEP 4: 必要なパッケージをインストール

必要なライブラリを一括でインストールします。

### コマンドを実行

**Windows の場合:**
```bash
pip install -r requirements.txt
```

**Mac / Linux の場合:**
```bash
pip3 install -r requirements.txt
```

### インストール中の表示

```
Collecting streamlit==1.41.0
Downloading streamlit-1.41.0-py2.py3-none-any.whl (8.5 MB)
...
Successfully installed streamlit-1.41.0 pandas-2.2.3 ...
```

**所要時間:** 2〜5分程度（インターネット速度による）

### エラーが出た場合

**「pip がない」と言われたら:**
```bash
# Windows
python -m ensurepip --upgrade

# Mac / Linux
python3 -m ensurepip --upgrade
```

**「権限がない」と言われたら:**
```bash
# Windows（管理者権限で実行）
# コマンドプロンプトを右クリック → 管理者として実行

# Mac / Linux
pip3 install -r requirements.txt --user
```

---

## 🔑 STEP 5: APIキーと認証情報を準備

### 5-1. Gemini API キーを取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」ボタンをクリック
4. 表示されたAPIキーをコピーして保存（後で使います）

**重要:** APIキーは誰にも教えないでください

### 5-2. Google Cloud 認証情報を取得

#### Google Cloud プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
   - プロジェクト名: 例「名刺管理アプリ」
   - 「作成」をクリック

#### APIを有効化

1. プロジェクトを選択
2. 左側メニュー → 「APIとサービス」 → 「ライブラリ」
3. 以下のAPIを検索して有効化:
   - **Cloud Vision API** を有効化
   - **Google Sheets API** を有効化
   - **Google Drive API** を有効化

#### サービスアカウントを作成

1. 左側メニュー → 「APIとサービス」 → 「認証情報」
2. 「認証情報を作成」 → 「サービスアカウント」
3. サービスアカウント名: 例「business-card-app」
4. 「作成して続行」をクリック
5. ロール選択: 「編集者」を選択
6. 「完了」をクリック

#### JSONキーをダウンロード

1. 作成したサービスアカウントをクリック
2. 「キー」タブを選択
3. 「鍵を追加」 → 「新しい鍵を作成」
4. 「JSON」を選択して「作成」
5. JSONファイルが自動でダウンロードされます
6. ダウンロードしたJSONファイルの名前を `credentials.json` に変更
7. プロジェクトフォルダ（`streamlit-llm-app`）に配置

**フォルダ構成例:**
```
streamlit-llm-app/
├── app.py
├── requirements.txt
├── credentials.json  ← ここに配置
└── ...
```

### 5-3. 環境変数を設定（オプション）

`.env` ファイルを作成すると、毎回APIキーを入力する手間が省けます。

1. プロジェクトフォルダに `.env` ファイルを作成
2. 以下の内容を記入:

```env
GEMINI_API_KEY=ここに取得したGemini APIキーを貼り付け
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

**例:**
```env
GEMINI_API_KEY=AIzaSyABC123...XYZ789
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

---

## 🚀 STEP 6: アプリを起動する

いよいよアプリを起動します！

### コマンドを実行

ターミナル/コマンドプロンプトで以下を実行:

```bash
streamlit run app.py
```

### 起動時の表示

```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

**成功すると:**
- 自動的にブラウザが開いてアプリが表示されます
- 開かない場合は、手動で `http://localhost:8501` にアクセス

### アプリの停止方法

ターミナル/コマンドプロンプトで `Ctrl + C` を押すとアプリが停止します。

---

## 🎯 STEP 7: アプリを使ってみる

### 初回設定

アプリが開いたら:

1. **左側のサイドバー**を開く
2. 「Gemini API キー」欄に取得したAPIキーを入力
3. 「Google Cloud 認証情報 (JSON)」で `credentials.json` ファイルをアップロード

### 名刺を登録してみる

1. 「📤 名刺登録」タブを開く
2. 名刺の写真をアップロード（スマホで撮影したものでOK）
3. 「🔍 OCR処理を実行」ボタンをクリック
4. 抽出された情報を確認
5. 必要に応じて修正
6. 「💾 保存」ボタンをクリック

---

## ❓ よくある質問とトラブルシューティング

### Q1: 「streamlit: command not found」と出る

**解決方法:**

```bash
# パッケージが正しくインストールされているか確認
pip list | grep streamlit

# 表示されない場合、再インストール
pip install streamlit
```

### Q2: ブラウザが自動で開かない

**解決方法:**
- 手動でブラウザを開いて `http://localhost:8501` にアクセス

### Q3: APIキーが無効と言われる

**解決方法:**
- APIキーをコピーする際にスペースが入っていないか確認
- [Google AI Studio](https://makersuite.google.com/app/apikey) で新しいキーを作成

### Q4: Cloud Vision APIのエラーが出る

**解決方法:**
- Google Cloud Console でAPIが有効化されているか確認
- 認証情報ファイル（credentials.json）が正しい場所にあるか確認
- サービスアカウントに適切な権限があるか確認

### Q5: Google Sheetsへのエクスポートができない

**解決方法:**
1. Google Sheetsで新しいスプレッドシートを作成
2. 共有設定を開く
3. サービスアカウントのメールアドレス（credentials.jsonの中の`client_email`）を編集者として追加
4. スプレッドシートのURLをコピーしてアプリに貼り付け

---

## 🎉 完了！

これで名刺管理アプリが使えるようになりました！

### 次回起動する際の手順

1. ターミナル/コマンドプロンプトを開く
2. プロジェクトフォルダに移動
3. 仮想環境を有効化（作成した場合）
4. `streamlit run app.py` を実行

**簡単な起動スクリプト:**

次回からもっと簡単に起動できるように、スクリプトを作成できます。

**Windows用（run.bat）:**
```batch
@echo off
cd /d %~dp0
call venv\Scripts\activate
streamlit run app.py
pause
```

**Mac/Linux用（run.sh）:**
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py
```

これらのファイルをダブルクリックするだけでアプリが起動します！

---

## 💡 困ったときは

- README.md を確認
- エラーメッセージをコピーしてGoogle検索
- GitHubのIssuesで質問

お疲れさまでした！名刺管理を楽しんでください 🎊
