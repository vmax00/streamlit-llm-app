@echo off
chcp 65001 > nul
echo ========================================
echo   名刺管理アプリ - セットアップ
echo ========================================
echo.

REM プロジェクトディレクトリに移動
cd /d %~dp0

REM Pythonのバージョンを確認
echo [1/4] Pythonのバージョンを確認しています...
python --version
if %errorlevel% neq 0 (
    echo エラー: Pythonがインストールされていません。
    echo https://www.python.org/downloads/ からPythonをダウンロードしてください。
    pause
    exit /b 1
)
echo.

REM 仮想環境を作成
echo [2/4] 仮想環境を作成しています...
if exist venv (
    echo 仮想環境は既に存在します。スキップします。
) else (
    python -m venv venv
    echo 仮想環境を作成しました。
)
echo.

REM 仮想環境を有効化
echo [3/4] 仮想環境を有効化しています...
call venv\Scripts\activate.bat

REM 依存パッケージをインストール
echo [4/4] 依存パッケージをインストールしています...
echo これには数分かかる場合があります...
echo.
pip install -r requirements.txt

echo.
echo ========================================
echo   セットアップが完了しました！
echo ========================================
echo.
echo 次のステップ:
echo 1. Gemini API キーを取得
echo    https://makersuite.google.com/app/apikey
echo.
echo 2. Google Cloud 認証情報を取得
echo    https://console.cloud.google.com/
echo    - Cloud Vision API を有効化
echo    - Google Sheets API を有効化
echo    - サービスアカウントを作成してJSON認証情報をダウンロード
echo.
echo 3. アプリを起動
echo    run.bat をダブルクリック、または以下を実行:
echo    streamlit run app.py
echo.
echo 詳しい手順は SETUP_GUIDE.md を参照してください。
echo.

pause
