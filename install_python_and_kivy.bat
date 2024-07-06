@echo off
setlocal

set PYTHON_URL=https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
set PYTHON_INSTALLER=python-3.10.6-amd64.exe

echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

echo Installing Python...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

timeout /t 10 /nobreak

python --version
if errorlevel 1 (
    echo Python installation failed.
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing Kivy...
python -m pip install kivy

python -c "import kivy; print('Kivy', kivy.__version__)"

echo Installation complete.
pause
