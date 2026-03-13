@echo off
chcp 65001 >nul
echo ======================================
echo 📦 电话测试工具 - Windows 打包脚本
echo ======================================
echo.

:: 配置
set APP_NAME=PhoneCallTester
set APP_VERSION=1.0.0
set DIST_DIR=dist
set BUILD_DIR=build

:: 检查 Python
echo 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

python --version
echo.

:: 检查/安装 PyInstaller
echo 检查 PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ PyInstaller 未安装，正在安装...
    pip install pyinstaller
)

echo ✓ PyInstaller 已就绪
echo.

:: 安装依赖
echo 安装项目依赖...
pip install -q PyQt6 pandas openpyxl pyinstaller

echo ✓ 依赖安装完成
echo.

:: 清理旧构建
echo 清理旧构建文件...
if exist %BUILD_DIR% rmdir /s /q %BUILD_DIR%
if exist %DIST_DIR% rmdir /s /q %DIST_DIR%

echo ✓ 清理完成
echo.

:: 创建图标目录
if not exist resources mkdir resources

:: 打包
echo ======================================
echo 🔨 开始打包...
echo ======================================
echo.

echo 打包 Windows 可执行文件...
pyinstaller ^
    --name="%APP_NAME%" ^
    --windowed ^
    --onefile ^
    --clean ^
    --noconfirm ^
    --icon=resources\icon.ico ^
    --add-data "resources;resources" ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=pandas ^
    --hidden-import=openpyxl ^
    --exclude-module=matplotlib ^
    --exclude-module=scipy ^
    --exclude-module=tkinter ^
    phone_call_tester.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ======================================
echo ✅ 打包完成!
echo ======================================
echo.

if exist "%DIST_DIR%\%APP_NAME%.exe" (
    echo ✓ 可执行文件已生成:
    echo   %DIST_DIR%\%APP_NAME%.exe
    echo.
    echo 文件信息:
    dir "%DIST_DIR%\%APP_NAME%.exe"
    echo.
    echo ======================================
    echo 📋 使用说明
    echo ======================================
    echo.
    echo 1. 将 %DIST_DIR%\%APP_NAME%.exe 复制到目标电脑
    echo 2. 无需安装 Python，直接双击运行即可
    echo.
    echo 注意:
    echo   - 目标电脑需要有 ADB 工具才能连接手机
    echo   - 首次运行 Windows 可能会提示"Windows 已保护你的电脑"
    echo   - 点击"更多信息" → "仍要运行"即可
    echo.
) else (
    echo ❌ 可执行文件生成失败
    pause
    exit /b 1
)

pause
