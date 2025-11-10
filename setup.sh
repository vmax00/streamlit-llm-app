#!/bin/bash

echo "========================================"
echo "  名刺管理アプリ - セットアップ"
echo "========================================"
echo ""

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

# Pythonのバージョンを確認
echo "[1/4] Pythonのバージョンを確認しています..."
if command -v python3 &> /dev/null; then
    python3 --version
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    python --version
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "エラー: Pythonがインストールされていません。"
    echo "https://www.python.org/downloads/ からPythonをダウンロードしてください。"
    exit 1
fi
echo ""

# 仮想環境を作成
echo "[2/4] 仮想環境を作成しています..."
if [ -d "venv" ]; then
    echo "仮想環境は既に存在します。スキップします。"
else
    $PYTHON_CMD -m venv venv
    echo "仮想環境を作成しました。"
fi
echo ""

# 仮想環境を有効化
echo "[3/4] 仮想環境を有効化しています..."
source venv/bin/activate

# 依存パッケージをインストール
echo "[4/4] 依存パッケージをインストールしています..."
echo "これには数分かかる場合があります..."
echo ""
$PIP_CMD install -r requirements.txt

echo ""
echo "========================================"
echo "  セットアップが完了しました！"
echo "========================================"
echo ""
echo "次のステップ:"
echo "1. Gemini API キーを取得"
echo "   https://makersuite.google.com/app/apikey"
echo ""
echo "2. Google Cloud 認証情報を取得"
echo "   https://console.cloud.google.com/"
echo "   - Cloud Vision API を有効化"
echo "   - Google Sheets API を有効化"
echo "   - サービスアカウントを作成してJSON認証情報をダウンロード"
echo ""
echo "3. アプリを起動"
echo "   ./run.sh を実行、または以下を実行:"
echo "   streamlit run app.py"
echo ""
echo "詳しい手順は SETUP_GUIDE.md を参照してください。"
echo ""

read -p "Enterキーを押して終了..."
