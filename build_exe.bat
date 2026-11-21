@echo off
REM ============================================================================
REM MyBot ATK GENERATOR - Build Script
REM Compila para .exe único com PyInstaller + UPX
REM ============================================================================

echo [1/4] Limpando builds anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del /q *.spec 2>nul

echo [2/4] Verificando dependencias...
python -c "import PySide6; import attackgen" 2>nul || (
    echo ERRO: Dependencias nao instaladas. Rode: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [3/4] Compilando com PyInstaller...
REM Parametros para reduzir falsos positivos de antivirus:
REM --noconfirm           : sobrescreve sem perguntar
REM --clean               : limpa cache antes de buildar
REM --onefile             : unico .exe
REM --noconsole           : sem janela de console (GUI)
REM --strip               : remove simbolos de debug (menor, mais rapido)
REM --upx-dir=...         : usa UPX do sistema (ja no PATH)
REM --icon=icon.ico       : icone personalizado
REM --name=...            : nome do executavel
REM --exclude-module=...  : remove modulos desnecessarios
REM --hidden-import=...   : garante imports dinamicos

pyinstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --noconsole ^
    --strip ^
    --upx-dir=%UPX_DIR% ^
    --icon=icon.ico ^
    --name=MyBot_ATK_GEN ^
    --exclude-module=tkinter ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=scipy ^
    --exclude-module=pandas ^
    --exclude-module=PIL ^
    --exclude-module=cv2 ^
    --exclude-module=torch ^
    --exclude-module=tensorflow ^
    --exclude-module=jupyter ^
    --exclude-module=notebook ^
    --exclude-module=IPython ^
    --exclude-module=pytest ^
    --exclude-module=setuptools ^
    --exclude-module=wheel ^
    --exclude-module=pip ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    --hidden-import=PySide6.QtPrintSupport ^
    --hidden-import=attackgen.schema ^
    --hidden-import=attackgen.model ^
    --hidden-import=attackgen.parser ^
    --hidden-import=attackgen.emitter ^
    --hidden-import=attackgen.validate ^
    --hidden-import=attackgen.geometry ^
    --hidden-import=attackgen.templates ^
    --hidden-import=attackgen.i18n ^
    --hidden-import=attackgen.cli ^
    --hidden-import=attackgen.ui_main ^
    --add-data="templates;templates" ^
    --add-data="icon.ico;." ^
    main.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha na compilacao
    pause
    exit /b 1
)

echo [4/4] Verificando resultado...
if exist "dist\MyBot_ATK_GEN.exe" (
    echo.
    echo ============================================================================
    echo SUCESSO! Executavel criado em: dist\MyBot_ATK_GEN.exe
    echo Tamanho: 
    for %%F in (dist\MyBot_ATK_GEN.exe) do echo %%~zF bytes
    echo ============================================================================
    echo.
    echo Dicas para evitar falsos positivos:
    echo 1. Assine digitalmente o .exe (code signing certificate)
    echo 2. Submeta ao VirusTotal / Microsoft para analise
    echo 3. Adicione a pasta dist nas exclusoes do seu AV durante desenvolvimento
) else (
    echo ERRO: Executavel nao encontrado em dist\
)

pause