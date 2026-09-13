@echo off
echo =========================================
echo   Smart Audit Cerdas - Menjalankan Server
echo =========================================
echo.
echo Menggunakan Python dari Virtual Environment...
echo.

:: Pastikan Python yang dipakai adalah dari venv (bukan sistem global)
:: Ini anti-gagal tanpa perlu 'activate'
set PYTHON="%~dp0venv\Scripts\python.exe"

:: Cek apakah venv python ada
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo Jalankan: python -m venv venv
    echo Lalu: venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo Server akan berjalan. URL ngrok akan tampil di bawah ini...
echo Tekan Ctrl+C untuk menghentikan.
echo.

%PYTHON% app.py
pause
