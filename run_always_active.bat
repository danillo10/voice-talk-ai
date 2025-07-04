@echo off
echo ================================
echo  Voice Talk AI - SEMPRE ATIVO
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
    pause
    exit /b 1
)

echo Dependências OK!
echo.

REM Informar sobre inicialização automática
echo MODO SEMPRE ATIVO:
echo - A aplicação iniciará automaticamente a captura
echo - Ficará sempre ativa capturando áudio
echo - Minimize para a bandeja para usar em segundo plano
echo - Use Pausar/Retomar para controlar
echo.

echo Iniciando Voice Talk AI em modo sempre ativo...
echo.

REM Executar a aplicação
python voice_talk_ai.py

REM Se chegou aqui, algo deu errado
echo.
echo A aplicação foi fechada. Tentando reiniciar...
echo.
timeout /t 3 /nobreak >nul

REM Tentar reiniciar
goto :start

:start
python voice_talk_ai.py
if %errorlevel% neq 0 (
    echo Erro na execução. Aguardando antes de tentar novamente...
    timeout /t 5 /nobreak >nul
    goto :start
)

pause
