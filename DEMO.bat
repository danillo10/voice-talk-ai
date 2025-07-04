@echo off
cls
echo.
echo ░██╗░░░░░░░██╗░█████╗░██╗░█████╗░███████╗  ████████╗░█████╗░██╗░░░░░██╗░░██╗
echo ░██║░░██╗░░██║██╔══██╗██║██╔══██╗██╔════╝  ╚══██╔══╝██╔══██╗██║░░░░░██║░██╔╝
echo ░╚██╗████╗██╔╝██║░░██║██║██║░░╚═╝█████╗░░  ░░░██║░░░███████║██║░░░░░█████═╝░
echo ░░████╔═████║░██║░░██║██║██║░░██╗██╔══╝░░  ░░░██║░░░██╔══██║██║░░░░░██╔═██╗░
echo ░░╚██╔╝░╚██╔╝░╚█████╔╝██║╚█████╔╝███████╗  ░░░██║░░░██║░░██║███████╗██║░╚██╗
echo ░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░╚════╝░╚══════╝  ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
echo.
echo ░█████╗░██╗  ░░░░░░░░█████╗░████████╗██╗██╗░░░██╗░█████╗░██╗
echo ██╔══██╗██║  ░░░░░░░██╔══██╗╚══██╔══╝██║██║░░░██║██╔══██╗██║
echo ███████║██║  ░░░░░░░███████║░░░██║░░░██║╚██╗░██╔╝██║░░██║██║
echo ██╔══██║██║  ░░░░░░░██╔══██║░░░██║░░░██║░╚████╔╝░██║░░██║╚═╝
echo ██║░░██║██║  ░░░░░░░██║░░██║░░░██║░░░██║░░╚██╔╝░░╚█████╔╝██╗
echo ╚═╝░░╚═╝╚═╝  ░░░░░░░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝
echo.
echo ====================================================================
echo                    VOICE TALK AI - SEMPRE ATIVO
echo ====================================================================
echo.
echo ✨ RECURSOS AUTOMÁTICOS:
echo  🚀 Auto-start: Inicia captura automaticamente
echo  🔄 Auto-restart: Reinicia em caso de erro
echo  💪 Keep-alive: Monitora e mantém funcionando
echo  🎯 Monitoramento: Verifica integridade constantemente
echo  🛡️ Proteção: Máximo 3 tentativas de restart
echo  📱 Notificações: Avisa sobre status
echo.
echo ✅ PRONTO PARA CALLS:
echo  • Microsoft Teams
echo  • Zoom
echo  • Discord
echo  • Skype
echo  • Google Meet
echo  • Qualquer aplicativo de áudio
echo.
echo 🎮 CONTROLES DISPONÍVEIS:
echo  🔄 Reiniciar Captura
echo  ⏸️ Pausar/Retomar
echo  🗑️ Limpar Legendas
echo  ⬇️ Minimizar para Bandeja
echo.
echo ====================================================================
echo.
echo Pressione qualquer tecla para iniciar o Voice Talk AI...
pause >nul

echo.
echo 🚀 Iniciando Voice Talk AI em modo SEMPRE ATIVO...
echo.
echo ⚠️  IMPORTANTE: Execute como administrador para melhor performance
echo 🔧 Certifique-se de que o Stereo Mix está habilitado
echo 🌐 Mantenha conexão estável com internet
echo.
echo 🎯 O Voice Talk AI iniciará automaticamente a captura em 2 segundos
echo 📱 Minimize para bandeja para usar em segundo plano
echo.

python voice_talk_ai.py

echo.
echo ====================================================================
echo Voice Talk AI foi finalizado.
echo.
echo 🔄 Tentando reiniciar automaticamente...
timeout /t 3 /nobreak >nul
echo.
goto :start

:start
echo 🚀 Reiniciando Voice Talk AI...
python voice_talk_ai.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Erro detectado. Aguardando 5 segundos antes de tentar novamente...
    timeout /t 5 /nobreak >nul
    goto :start
)
echo.
echo ✅ Voice Talk AI funcionou corretamente!
pause
