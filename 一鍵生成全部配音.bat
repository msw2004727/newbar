@echo off
chcp 65001 >nul
title 小小繪本書架 - 一鍵生成全部配音
cd /d "%~dp0"
echo ============================================================
echo   小小繪本書架 ・ 一鍵生成「全部繪本」的配音
echo ============================================================
echo.
where python >nul 2>&1
if errorlevel 1 goto NOPY
python -m pip install --quiet --upgrade edge-tts
python "生成全部配音.py" %*
echo.
pause
exit /b
:NOPY
echo.
echo 找不到 Python。請先到 https://www.python.org/downloads/ 安裝，
echo 安裝第一頁務必勾選「Add Python to PATH」。
echo.
pause
