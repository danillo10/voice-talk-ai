@echo off
echo ===============================================
echo  Voice Talk AI - Configuracao Stereo Mix
echo ===============================================
echo.
echo Este script ira ajuda-lo a configurar o Stereo Mix
echo para capturar o audio do sistema (voz do outro lado da call)
echo.
echo PASSOS:
echo 1. Abrir configuracoes de som
echo 2. Habilitar Stereo Mix
echo 3. Configurar como dispositivo padrao
echo.
pause

echo.
echo Abrindo Painel de Controle do Som...
control mmsys.cpl sounds

echo.
echo ===============================================
echo  INSTRUCOES DETALHADAS:
echo ===============================================
echo.
echo 1. Na janela que abriu, va para a aba "GRAVACAO"
echo.
echo 2. Clique com o botao DIREITO em qualquer lugar vazio
echo    e selecione "Mostrar dispositivos desabilitados"
echo.
echo 3. Procure por "Stereo Mix" ou "Mix Estéreo"
echo    (pode aparecer como "What U Hear" em algumas placas)
echo.
echo 4. Clique com o botao DIREITO no "Stereo Mix"
echo    e selecione "Habilitar"
echo.
echo 5. Clique com o botao DIREITO no "Stereo Mix" novamente
echo    e selecione "Definir como dispositivo padrao"
echo.
echo 6. Clique em "OK" para salvar
echo.
echo ===============================================
echo  TESTE DEPOIS:
echo ===============================================
echo.
echo Depois de configurar, execute:
echo   python test_dual_audio.py
echo.
echo Ou use o menu do aplicativo principal.
echo.
echo ===============================================
echo  ALTERNATIVAS (se nao tiver Stereo Mix):
echo ===============================================
echo.
echo 1. VB-Audio Virtual Cable (gratuito)
echo    Download: https://vb-audio.com/Cable/
echo.
echo 2. Voicemeeter (gratuito)
echo    Download: https://vb-audio.com/Voicemeeter/
echo.
echo 3. OBS Virtual Camera (para streamers)
echo.
echo ===============================================
pause
