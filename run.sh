#!/bin/bash

echo "========================================"
echo "  名刺管理アプリを起動しています..."
echo "========================================"
echo ""

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境が存在するか確認
if [ -f "venv/bin/activate" ]; then
    echo "仮想環境を有効化しています..."
    source venv/bin/activate
else
    echo "警告: 仮想環境が見つかりません。システムのPythonを使用します。"
    echo "仮想環境を作成する場合は、以下を実行してください:"
    echo "python3 -m venv venv"
    echo ""
fi

# Streamlitアプリを起動
echo "Streamlitアプリを起動しています..."
echo "ブラウザが自動的に開きます。開かない場合は以下にアクセス:"
echo "http://localhost:8501"
echo ""
echo "アプリを停止するには Ctrl+C を押してください"
echo ""

streamlit run app.py
