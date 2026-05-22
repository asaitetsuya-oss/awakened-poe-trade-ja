@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ============================================================
echo  awakened-poe-trade Japanese build script (auto-patch)
echo ============================================================
echo.

set "REPO_DIR=D:\dev\awakened-poe-trade"
set "REPO_URL=https://github.com/SnosMe/awakened-poe-trade.git"
set "JA_DIR=%REPO_DIR%\renderer\public\data\ja"
set "DATA_DIR=%REPO_DIR%\renderer\public\data"
set "SCRIPT_DIR=%~dp0"

:: [1/8] Prerequisites
echo [1/8] Checking prerequisites...
where git >nul 2>&1
if errorlevel 1 ( echo [ERROR] git not found. & pause & exit /b 1 )
where node >nul 2>&1
if errorlevel 1 ( echo [ERROR] Node.js not found. & pause & exit /b 1 )
where npm >nul 2>&1
if errorlevel 1 ( echo [ERROR] npm not found. & pause & exit /b 1 )
for /f "tokens=*" %%v in ('node -v 2^>nul') do set NODE_VER=%%v
for /f "tokens=*" %%v in ('npm -v 2^>nul') do set NPM_VER=%%v
echo     Node.js: %NODE_VER%
echo     npm:     %NPM_VER%
echo     OK
echo.

:: [2/8] Clone or pull
echo [2/8] Preparing repository...
if not exist "%REPO_DIR%\.git" (
    echo     Cloning...
    git clone "%REPO_URL%" "%REPO_DIR%"
    if errorlevel 1 ( echo [ERROR] git clone failed. & pause & exit /b 1 )
) else (
    echo     Pulling latest changes...
    pushd "%REPO_DIR%"
    git pull
    popd
)
echo     Done.
echo.

:: [3/8] Apply patches
echo [3/8] Applying patches...

echo     Patching main/src/AppTray.ts...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_apptray.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] AppTray patch failed. & pause & exit /b 1 )

echo     Patching renderer/src/web/Config.ts...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_config.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] Config patch failed. & pause & exit /b 1 )

echo     Patching renderer/src/web/settings/general.vue...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_general.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] general.vue patch failed. & pause & exit /b 1 )

echo     Patching language entries in client-log.ts and hotkeyable-actions.ts...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_ja_lang.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] ja_lang patch failed. & pause & exit /b 1 )
if defined PYTHON_CMD (
    %PYTHON_CMD% "%SCRIPT_DIR%fix_client_log.py" "%REPO_DIR%"
)

echo     Patching HostClipboard.ts (adding Japanese language detector)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_clipboard.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] clipboard patch failed. & pause & exit /b 1 )

echo     Patching patron display...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_patron.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] patron patch failed. & pause & exit /b 1 )

echo     Patching parser (quality/split fixes)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%patch_parser.ps1" "%REPO_DIR%"
if errorlevel 1 ( echo [ERROR] parser patch failed. & pause & exit /b 1 )


echo     All patches applied.
echo.

:: [4/8] Japanese i18n
echo [4/8] Placing Japanese UI translation...
if not exist "%JA_DIR%" mkdir "%JA_DIR%"
if not exist "%SCRIPT_DIR%ja_app_i18n.json" (
    echo [ERROR] ja_app_i18n.json not found.
    pause & exit /b 1
)
copy /Y "%SCRIPT_DIR%ja_app_i18n.json" "%JA_DIR%\app_i18n.json" >nul
echo     Copied ja_app_i18n.json
if not exist "%SCRIPT_DIR%client_strings.js" (
    echo [ERROR] client_strings.js not found.
    pause & exit /b 1
)
copy /Y "%SCRIPT_DIR%client_strings.js" "%JA_DIR%\client_strings.js" >nul
echo     Copied client_strings.js

echo.

:: [5/8] Python check
echo [5/8] Checking Python...
set "PYTHON_CMD="
where python >nul 2>&1 && set "PYTHON_CMD=python"
if not defined PYTHON_CMD (
    where python3 >nul 2>&1 && set "PYTHON_CMD=python3"
)
if not defined PYTHON_CMD ( echo     [SKIP] Python not found. ) else ( echo     Python: %PYTHON_CMD% )
echo.

:: [6/8] Build renderer
echo [6/8] Building renderer...
pushd "%REPO_DIR%\renderer"
echo     npm install...
call npm install
if errorlevel 1 ( echo [ERROR] npm install failed. & popd & pause & exit /b 1 )
:: Step1: make-index-files でenデータを生成
echo     npm run make-index-files (1st pass - generate en data)...
call npm run make-index-files

:: Step2: Pythonで翻訳（translate_stats.pyがen->jaコピーも実施）
if defined PYTHON_CMD (
    if exist "%SCRIPT_DIR%translate_items.py" (
        echo     Translating ja/items.ndjson...
        %PYTHON_CMD% "%SCRIPT_DIR%translate_items.py" "%DATA_DIR%"
    )
    if exist "%SCRIPT_DIR%translate_stats.py" (
        if exist "%SCRIPT_DIR%poe1_trade_stats_ja.json" (
            echo     Translating ja/stats.ndjson with Japanese trade API data...
            %PYTHON_CMD% "%SCRIPT_DIR%translate_stats.py" "%DATA_DIR%" "%SCRIPT_DIR%poe1_trade_stats_ja.json"
        ) else (
            echo     [SKIP] poe1_trade_stats_ja.json not found. Run:
            echo       curl -o "%SCRIPT_DIR%poe1_trade_stats_ja.json" "https://jp.pathofexile.com/api/trade/data/stats"
        )
    )
) else (
    :: Pythonなし: enからコピーだけ
    if exist "%DATA_DIR%\en\items.ndjson" copy /Y "%DATA_DIR%\en\items.ndjson" "%JA_DIR%\items.ndjson" >nul
    if exist "%DATA_DIR%\en\stats.ndjson" copy /Y "%DATA_DIR%\en\stats.ndjson" "%JA_DIR%\stats.ndjson" >nul
)

:: Step3: 翻訳済みデータでインデックス再生成
echo     npm run make-index-files (2nd pass - build ja index)...
call npm run make-index-files

:: Step4: ビルド
echo     npm run build...
call npm run build
if errorlevel 1 ( echo [ERROR] renderer build failed. & popd & pause & exit /b 1 )
popd
echo     Renderer build complete.
echo.

:: [7/8] Build main
echo [7/8] Building main...
pushd "%REPO_DIR%\main"
echo     npm install...
call npm install
if errorlevel 1 ( echo [ERROR] npm install failed. & popd & pause & exit /b 1 )
echo     npm run build...
call npm run build
if errorlevel 1 ( echo [ERROR] main build failed. & popd & pause & exit /b 1 )
echo     npm run package...
call npm run package
if errorlevel 1 ( echo [ERROR] package failed. & popd & pause & exit /b 1 )
popd
echo     Main build complete.
echo.

:: [8/8] Done
echo [8/8] Build finished!
echo.
set "OUT_DIR="
for %%d in ("%REPO_DIR%\main\out" "%REPO_DIR%\main\dist" "%REPO_DIR%\out" "%REPO_DIR%\dist") do (
    if exist "%%~d" if not defined OUT_DIR set "OUT_DIR=%%~d"
)
if defined OUT_DIR (
    echo Output: %OUT_DIR%
    explorer "%OUT_DIR%"
) else (
    echo Output not found. Check %REPO_DIR%\main\
)
echo.
pause