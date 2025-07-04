@echo off
echo ===============================
echo   VOICE TALK AI - STATUS
echo ===============================
echo.

echo Verificando se o Voice Talk AI está rodando...
echo.

REM Verificar se há processos Python rodando
tasklist /FI "IMAGENAME eq python.exe" /FO TABLE | find /I "python.exe" >nul
if %errorlevel% == 0 (
    echo ✓ Python em execução detectado
    echo.
    echo Processos Python ativos:
    tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
) else (
    echo ✗ Nenhum processo Python detectado
)

echo.
echo ===============================
echo   OPÇÕES DISPONÍVEIS
echo ===============================
echo.

echo 1. Executar Voice Talk AI (Sempre Ativo)
echo 2. Executar Gerenciador com Auto-restart
echo 3. Configurar Inicialização Automática
echo 4. Testar Dependências
echo 5. Verificar Status Novamente
echo 6. Sair
echo.

set /p choice=Digite sua escolha (1-6): 

if "%choice%"=="1" (
    echo Iniciando Voice Talk AI...
    start "" "run_always_active.bat"
) else if "%choice%"=="2" (
    echo Iniciando Gerenciador...
    python voice_manager.py
) else if "%choice%"=="3" (
    echo Configurando inicialização...
    python setup_startup.py
) else if "%choice%"=="4" (
    echo Testando dependências...
    python test_system.py
) else if "%choice%"=="5" (
    echo Verificando status...
    goto :start
) else if "%choice%"=="6" (
    echo Saindo...
    exit /b 0
) else (
    echo Opção inválida.
)

:start
pause
