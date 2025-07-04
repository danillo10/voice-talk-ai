@echo off
cls
echo.
echo ████████████████████████████████████████████████████████████████████████████████
echo █                                                                              █
echo █                    🔧 CONFIGURAÇÃO DO STEREO MIX                           █
echo █                      Para Capturar Áudio do Sistema                         █
echo █                                                                              █
echo ████████████████████████████████████████████████████████████████████████████████
echo.
echo 🎯 OBJETIVO: Habilitar captura do áudio que está sendo reproduzido no PC
echo    (necessário para ouvir o outro lado das calls)
echo.
echo 📋 PASSO A PASSO:
echo.
echo    1️⃣  Clique com o botão DIREITO no ícone de som (canto inferior direito)
echo.
echo    2️⃣  Selecione "Dispositivos de gravação" ou "Sons"
echo.
echo    3️⃣  Na janela que abrir, clique na aba "GRAVAÇÃO"
echo.
echo    4️⃣  Clique com o botão DIREITO em qualquer espaço vazio da lista
echo.
echo    5️⃣  Marque as opções:
echo         ✅ "Mostrar dispositivos desabilitados"
echo         ✅ "Mostrar dispositivos desconectados"
echo.
echo    6️⃣  Procure por "Stereo Mix" ou "Mixagem Estéreo" na lista
echo.
echo    7️⃣  Clique com o botão DIREITO em "Stereo Mix"
echo.
echo    8️⃣  Selecione "HABILITAR"
echo.
echo    9️⃣  (Opcional) Clique com o botão direito novamente e "Definir como padrão"
echo.
echo ⚠️  SE NÃO APARECER "STEREO MIX":
echo     • Seu driver de áudio pode não suportar
echo     • Tente atualizar driver de áudio (Realtek, etc.)
echo     • Algumas placas-mãe não têm essa função
echo.
echo 🔍 ALTERNATIVAS SE NÃO TIVER STEREO MIX:
echo     • VB-Audio Virtual Cable (software gratuito)
echo     • Voicemeeter (software gratuito)
echo     • Use apenas captura de microfone
echo.
echo ████████████████████████████████████████████████████████████████████████████████
echo.
echo Após configurar o Stereo Mix, execute:
echo.
echo  📱 python test_dual_audio.py    (para testar)
echo  🚀 python voice_talk_ai.py      (para usar)
echo.
echo ████████████████████████████████████████████████████████████████████████████████
echo.
pause

REM Opção para abrir configurações automaticamente
echo.
echo 🤖 Deseja abrir as configurações de som automaticamente? (s/n)
set /p open_settings="Digite s para SIM ou n para NÃO: "

if /i "%open_settings%"=="s" (
    echo.
    echo 🔧 Abrindo configurações de som...
    start ms-settings:sound-devices
    echo.
    echo ✅ Siga os passos acima na janela que abriu!
) else (
    echo.
    echo 👍 OK! Você pode abrir manualmente quando quiser.
)

echo.
echo 🎯 Após configurar, teste com: python test_dual_audio.py
echo.
pause
