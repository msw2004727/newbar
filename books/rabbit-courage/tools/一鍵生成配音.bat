@echo off
chcp 65001 >nul
title 小豆的勇氣 - 配音生成
cd /d "%~dp0"

echo ============================================================
echo   小豆的勇氣  配音生成器
echo   使用微軟 Edge 神經語音（免費、免註冊、免金鑰）
echo ============================================================
echo.

REM ---- 檢查 Python ----
where python >nul 2>&1
if errorlevel 1 goto NOPY
python -c "import sys; sys.exit(0 if sys.version_info>=(3,8) else 1)" >nul 2>&1
if errorlevel 1 goto NOPY

echo [1/2] 準備語音套件 ...
python -m pip install --quiet --upgrade edge-tts
if errorlevel 1 (
    echo.
    echo 套件安裝失敗，請確認電腦有連上網路。
    echo.
    pause
    exit /b
)

echo [2/2] 開始生成配音，請稍候 ...
echo.
python "生成配音.py" %*

echo.
echo ============================================================
echo   完成！audio 資料夾已經產生在這裡。
echo   把 audio 資料夾跟「小豆的勇氣.html」放在同一層即可。
echo ============================================================
echo.
pause
exit /b

:NOPY
echo.
echo 找不到 Python（或版本太舊，需要 3.8 以上）。
echo.
echo 請先安裝 Python：
echo   1. 打開 https://www.python.org/downloads/
echo   2. 下載 Windows 版本並安裝
echo   3. 安裝畫面第一頁務必勾選「Add Python to PATH」再按 Install
echo   4. 裝完後重新雙擊這個檔案
echo.
echo （或到 Microsoft Store 搜尋 Python 安裝，一樣可以）
echo.
pause
