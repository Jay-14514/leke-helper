@echo off
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

cd /d "%~dp0"

chcp 936 >nul
title Leke Helper
cls

echo ==========================================
echo 乐课网助手 - 安装程序
echo ==========================================
echo 注意：请确保以【管理员身份】运行此脚本！
echo 按任意键开始
pause >nul

:: 步骤1：安装/检查Chrome
cls
echo ===== 步骤1：安装/检查Chrome =====
echo 正在关闭旧Chrome进程...
taskkill /f /im chrome.exe >nul 2>&1
timeout /t 1 >nul

set "CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe"
if exist "%CHROME%" (
    echo Chrome已安装：%CHROME%
) else (
    echo 未找到Chrome，开始自动下载安装...
    powershell -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest 'https://dl.google.com/chrome/install/standalonesetup64.exe' -OutFile 'chrome.exe' -TimeoutSec 120"
    start /wait chrome.exe /silent /install
    del chrome.exe >nul 2>&1
    if exist "%CHROME%" (
        echo Chrome自动安装成功
    ) else (
        echo Chrome安装失败！请手动安装后重试
        pause >nul
        exit
    )
)
echo 按任意键继续安装Python...
pause >nul

:: 步骤2：自动安装Python
cls
echo ===== 步骤2：安装/检查Python =====
python --version >nul 2>&1
if errorlevel 1 (
    echo 未找到Python，开始自动下载安装...
    powershell -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest 'https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe' -OutFile 'python.exe' -TimeoutSec 60"
    start /wait python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python.exe >nul 2>&1
    set "PATH=%PATH%;C:\Program Files\Python312;C:\Program Files\Python312\Scripts"
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Python安装失败！请手动安装并勾选Add to PATH
        pause >nul
        exit
    )
)
echo Python已安装
echo 正在安装selenium依赖...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple >nul 2>&1
python -m pip install selenium==4.17.2 -i https://pypi.tuna.tsinghua.edu.cn/simple >nul 2>&1
echo 依赖安装完成
echo 按任意键继续下载脚本...
pause >nul

:: 步骤3：下载app.py
cls
echo ===== 步骤3：下载app.py =====
powershell -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest 'https://leke.verber.eu.org/app.py' -OutFile 'app.py' -TimeoutSec 30"
if not exist app.py (
    echo app.py下载失败！请手动下载到当前文件夹
    pause >nul
    exit
)
echo app.py下载成功
echo 按任意键启动Chrome并运行脚本...
pause >nul

:: 步骤4：启动运行
cls
echo ===== 步骤4：启动运行 =====
echo 正在启动Chrome调试模式（打开乐课网）...
start /min "" "%CHROME%" --remote-debugging-port=9222 --user-data-dir="%~dp0chrome_debug" "https://www.leke.cn"
timeout /t 4 >nul
echo Chrome已启动，请先登录乐课网账号
echo 按任意键启动自动答题脚本...
pause >nul

echo 正在运行脚本（按Ctrl+C停止）...
python app.py

echo.
echo ===== 脚本运行结束 =====
echo 按 R 重试，按任意键退出
set /p CH=
if /I "%CH%"=="R" (
    taskkill /f /im chrome.exe >nul 2>&1
    start /min "" "%CHROME%" --remote-debugging-port=9222 --user-data-dir="%~dp0chrome_debug" "https://www.leke.cn"
    timeout /t 4 >nul
    python app.py
)
pause >nul