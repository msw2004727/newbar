@echo off
chcp 65001 >nul
title 打破的那個杯子 - 配音生成
cd /d "%~dp0"
echo ============================================================
echo   打破的那個杯子  配音生成器
echo   微軟 Edge 神經語音（免費、免註冊、免金鑰）
echo ============================================================
echo.
where python >nul 2>&1
if errorlevel 1 goto NOPY
echo [1/2] 準備語音套件 ...
python -m pip install --quiet --upgrade edge-tts
echo [2/2] 開始生成配音 ...
echo.
python "生成配音.py" %*
echo.
echo 完成！audio 資料夾已產生在繪本旁邊。
echo.
pause
exit /b
:NOPY
echo.
echo 找不到 Python。請先到 https://www.python.org/downloads/ 安裝，
echo 安裝第一頁務必勾選「Add Python to PATH」。
echo.
pause
