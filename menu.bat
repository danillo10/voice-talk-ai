@echo off
title Voice Talk AI - Menu Principal
color 0A

:MENU
cls
echo ===============================================
echo          VOICE TALK AI - MENU PRINCIPAL
echo ===============================================
echo.
echo  1. Iniciar Voice Talk AI (Normal)
echo  2. Iniciar Voice Talk AI (Administrador)
echo  3. Teste de Reconhecimento de Voz
echo  4. Teste de Captura Dual (Mic + Sistema)
echo  5. Configurar Stereo Mix
echo  6. Verificar Dependencias
echo  7. Instalar Dependencias
echo  8. Sair
echo.
echo ===============================================
echo Status: Microfone OK, Sistema precisa Stereo Mix
echo ===============================================
echo.
set /p choice="Escolha uma opcao (1-8): "

if "%choice%"=="1" goto NORMAL
if "%choice%"=="2" goto ADMIN
if "%choice%"=="3" goto TEST_SPEECH
if "%choice%"=="4" goto TEST_DUAL
if "%choice%"=="5" goto CONFIG_STEREO
if "%choice%"=="6" goto CHECK_DEPS
if "%choice%"=="7" goto INSTALL_DEPS
if "%choice%"=="8" goto EXIT

echo Opcao invalida! Pressione qualquer tecla para continuar...
pause >nul
goto MENU

:NORMAL
cls
echo Iniciando Voice Talk AI...
python voice_talk_ai.py
pause
goto MENU

:ADMIN
cls
echo Iniciando Voice Talk AI como Administrador...
echo (Para melhor captura de audio do sistema)
powershell -Command "Start-Process python -ArgumentList 'voice_talk_ai.py' -Verb runAs"
pause
goto MENU

:TEST_SPEECH
cls
echo Testando Reconhecimento de Voz...
python test_speech_recognition.py
pause
goto MENU

:TEST_DUAL
cls
echo Testando Captura Dual...
python test_dual_audio.py
pause
goto MENU

:CONFIG_STEREO
cls
echo Abrindo Configurador do Stereo Mix...
call configurar_stereo_mix.bat
pause
goto MENU

:CHECK_DEPS
cls
echo Verificando Dependencias...
python test_dependencies.py
pause
goto MENU

:INSTALL_DEPS
cls
echo Instalando Dependencias...
pip install -r requirements.txt
pause
goto MENU

:EXIT
cls
echo Obrigado por usar o Voice Talk AI!
echo.
echo Developed by: Voice Talk AI Team
echo Version: 2.0 Enhanced
echo.
pause
exit
