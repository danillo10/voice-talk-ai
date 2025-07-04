@echo off
echo Instalando dependencias do Voice Talk AI...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python não está instalado ou não está no PATH
    echo Por favor, instale Python 3.7+ de https://python.org
    pause
    exit /b 1
)

REM Verificar se pip está instalado
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: pip não está instalado
    echo Por favor, instale pip
    pause
    exit /b 1
)

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo Instalando dependências...
pip install -r requirements.txt

REM Verificar se PyAudio foi instalado corretamente
echo.
echo Verificando instalação do PyAudio...
python -c "import pyaudio; print('PyAudio instalado com sucesso!')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo AVISO: PyAudio pode não ter sido instalado corretamente.
    echo Se você encontrar problemas, tente instalar PyAudio manualmente:
    echo.
    echo Para Windows:
    echo 1. Baixe o arquivo .whl apropriado de https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    echo 2. Execute: pip install nome_do_arquivo.whl
    echo.
    echo Ou instale usando conda:
    echo conda install pyaudio
    echo.
)

echo.
echo Instalação concluída!
echo.
echo Para executar o Voice Talk AI, execute: python voice_talk_ai.py
echo.
echo IMPORTANTE: Para capturar áudio do sistema:
echo 1. Clique com o botão direito no ícone de som na bandeja do sistema
echo 2. Selecione "Dispositivos de gravação"
echo 3. Clique com o botão direito no espaço vazio e marque "Mostrar dispositivos desabilitados"
echo 4. Encontre "Stereo Mix" ou "Mixagem Estéreo" e clique com o botão direito
echo 5. Selecione "Habilitar"
echo 6. Defina como dispositivo padrão (opcional)
echo.
pause
