# Voice Talk AI - Tradutor de Voz em Tempo Real v2.0

## 🎯 Visão Geral

**Voice Talk AI** é uma aplicação desktop avançada em Python que captura e traduz em tempo real todo o áudio do PC (sistema e microfone), exibindo legendas em inglês e português. Ideal para calls, reuniões e comunicação internacional.

## ✨ Características Principais

- **🎤 Captura Dual**: Microfone + Áudio do Sistema
- **🔄 Tradução em Tempo Real**: Inglês ↔ Português
- **🎯 Reconhecimento Aprimorado**: Usa melhor alternativa com maior confiança
- **⚡ Sempre Ativo**: Inicia automaticamente com o sistema
- **🔧 Auto-Restart**: Reinicia automaticamente em caso de erro
- **🎨 Interface Moderna**: Botões intuitivos e status em tempo real
- **📱 Bandeja do Sistema**: Minimiza para a bandeja
- **🎛️ Controles Avançados**: Pause, limpar, configurar dispositivos

## 🚀 Início Rápido

### 1. Instalação
```bash
# Clone ou baixe o projeto
cd voice-talk-ai

# Instale as dependências
pip install -r requirements.txt
```

### 2. Execução
```bash
# Método 1: Menu interativo
menu.bat

# Método 2: Direto
python voice_talk_ai.py

# Método 3: Como administrador (recomendado)
# Clique com botão direito em menu.bat > Executar como administrador
```

## 🎯 Configuração para Calls

### Passo 1: Configurar Stereo Mix
Para capturar o áudio do sistema (voz do outro lado da call):

```bash
# Execute o configurador
configurar_stereo_mix.bat
```

**Ou manualmente:**
1. Painel de Controle → Som → Gravação
2. Botão direito → "Mostrar dispositivos desabilitados"
3. Habilitar "Stereo Mix"
4. Definir como dispositivo padrão

### Passo 2: Testar Captura Dual
```bash
python test_dual_audio.py
```

## 🎮 Como Usar

### Interface Principal
- **▶️ Iniciar**: Começa a captura
- **⏸️ Pausar**: Pausa temporariamente
- **🔄 Reiniciar**: Reinicia captura
- **🎤 Microfone**: Liga/desliga microfone
- **🔊 Sistema**: Liga/desliga áudio do sistema
- **📋 Dispositivos**: Mostra dispositivos disponíveis
- **🧹 Limpar**: Limpa as legendas
- **➖ Minimizar**: Minimiza para bandeja

### Legendas em Tempo Real
- **🎤 Microfone**: Sua voz
- **🔊 Sistema**: Voz do outro lado
- **[Hora]**: Timestamp de cada fala
- **EN**: Texto original em inglês
- **PT**: Tradução em português

## 🔧 Melhorias v2.0

### Reconhecimento Aprimorado
- ✅ Usa alternativas com maior confiança
- ✅ Filtros de volume e ruído
- ✅ Normalização de áudio
- ✅ Buffer de 3 segundos para melhor precisão
- ✅ Configurações otimizadas do recognizer

### Exemplo de Melhoria
**Antes**: "Hello i am figured out"
**Depois**: "Hello I'm fine and you" (usa alternativa com maior confiança)

### Captura Dual Robusta
- ✅ Detecção automática de dispositivos
- ✅ Fallback para alternativas
- ✅ Tratamento de erros melhorado
- ✅ Monitoramento de volume

## 🛠️ Scripts Utilitários

| Script | Função |
|--------|--------|
| `menu.bat` | Menu principal interativo |
| `configurar_stereo_mix.bat` | Configura Stereo Mix |
| `test_speech_recognition.py` | Teste de reconhecimento |
| `test_dual_audio.py` | Teste de captura dual |
| `test_dependencies.py` | Verifica dependências |

## 📋 Requisitos

### Dependências Python
```
pyaudio==0.2.11
SpeechRecognition==3.10.0
googletrans==4.0.0rc1
pystray==0.19.4
Pillow==10.0.0
numpy==1.24.3
```

### Sistema
- Windows 10/11
- Python 3.7+
- Microfone
- Stereo Mix (ou VB-Audio Virtual Cable)

## 🎤 Dispositivos de Áudio

### Microfone
- ✅ Detecta automaticamente
- ✅ Usa dispositivo padrão do sistema
- ✅ Fallback para primeiro disponível

### Áudio do Sistema
- 🎯 **Stereo Mix** (built-in)
- 🔧 **VB-Audio Virtual Cable** (gratuito)
- 🎛️ **Voicemeeter** (gratuito)

## 🚨 Troubleshooting

### Microfone não funciona
```bash
# Teste isolado
python test_speech_recognition.py

# Verificar dispositivos
python test_dual_audio.py
```

### Áudio do sistema não funciona
1. Configurar Stereo Mix
2. Ou instalar VB-Audio Virtual Cable
3. Executar como administrador

### Reconhecimento impreciso
- ✅ Fale mais claramente
- ✅ Reduza ruído ambiente
- ✅ Ajuste volume do microfone
- ✅ Use o modo administrador

## 📈 Monitoramento

### Logs em Tempo Real
- Volume de áudio
- Dispositivos detectados
- Erros de reconhecimento
- Status da conexão

### Auto-Recovery
- Reinicia automaticamente em erro
- Detecta dispositivos perdidos
- Reconecta serviços

## 🎯 Casos de Uso

### 1. Calls de Trabalho
- Traduz reuniões internacionais
- Captura ambos os lados
- Legendas em tempo real

### 2. Aprendizado de Idiomas
- Prática de conversação
- Correção de pronúncia
- Compreensão auditiva

### 3. Gaming
- Traduz voice chat
- Comunica com jogadores internacionais
- Minimiza para bandeja

## 💡 Dicas Profissionais

### Melhor Qualidade
- Execute como administrador
- Use headset com microfone
- Ambiente silencioso
- Conexão estável com internet

### Performance
- Feche aplicações desnecessárias
- Use modo de energia alta
- Mantenha drivers atualizados

## 🔄 Próximas Versões

- [ ] Suporte a mais idiomas
- [ ] Integração com Discord/Teams
- [ ] Exportar transcrições
- [ ] Modos de tema (escuro/claro)
- [ ] Atalhos de teclado

## 📞 Suporte

Para problemas específicos:
1. Execute `test_dependencies.py`
2. Execute `test_dual_audio.py`
3. Verifique logs do console
4. Configure Stereo Mix

---

**Voice Talk AI v2.0 Enhanced** - Desenvolvido para comunicação sem barreiras 🌍
