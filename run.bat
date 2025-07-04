@echo off
echo ================================
echo     Voice Talk AI - Launcher
echo ================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python não está instalado ou não está no PATH
    echo Execute install.bat primeiro para instalar as dependências
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Verificar se as dependências estão instaladas
echo Verificando dependências...
python -c "import speech_recognition; import googletrans; import pyaudio; import pystray; print('Dependências OK')" 2>nul
if %errorlevel% neq 0 (
    echo ERRO: Dependências não instaladas ou com problemas
    echo Execute install.bat primeiro para instalar as dependências
    echo.
    echo Ou execute o teste: python test_dependencies.py
    pause
    exit /b 1
)

echo Dependências OK!
echo.

REM Mostrar opções
echo Escolha uma opção:
echo 1. Executar aplicação completa (voice_talk_ai.py)
echo 2. Executar teste de dependências (test_dependencies.py)
echo 3. Executar aplicação simples (main.py)
echo 4. Executar em modo SEMPRE ATIVO (recomendado)
echo 5. Configurar inicialização automática do Windows
echo 6. Gerenciador com auto-restart
echo 7. Testar captura DUAL (microfone + sistema)
echo 8. Configurar Stereo Mix (áudio do sistema)
echo 9. Sair
echo.

set /p choice=Digite sua escolha (1-9): 

if "%choice%"=="1" (
    echo Executando aplicação completa...
    python voice_talk_ai.py
) else if "%choice%"=="2" (
    echo Executando teste de dependências...
    python test_dependencies.py
) else if "%choice%"=="3" (
    echo Executando aplicação simples...
    python main.py
) else if "%choice%"=="4" (
    echo Executando em modo SEMPRE ATIVO...
    call run_always_active.bat
) else if "%choice%"=="5" (
    echo Configurando inicialização automática...
    python setup_startup.py
) else if "%choice%"=="6" (
    echo Iniciando gerenciador com auto-restart...
    python voice_manager.py
) else if "%choice%"=="7" (
    echo Testando captura DUAL...
    python test_dual_audio.py
) else if "%choice%"=="8" (
    echo Configurando Stereo Mix...
    call setup_stereo_mix.bat
) else if "%choice%"=="9" (
    echo Saindo...
    exit /b 0
) else (
    echo Opção inválida. Executando em modo SEMPRE ATIVO...
    call run_always_active.bat
)

pause
