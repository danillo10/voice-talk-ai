# 🚀 GUIA RÁPIDO - Voice Talk AI v2.0

## 📥 Instalação em 2 Passos

1. **Baixe e instale dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o menu principal**
   ```bash
   menu.bat
   ```

## 🎯 Configuração Essencial

### Para Capturar Sua Voz (Microfone)
✅ **Já funciona automaticamente!**

### Para Capturar Voz do Outro Lado (Sistema)
1. Execute: `configurar_stereo_mix.bat`
2. Ou configure manualmente:
   - Painel de Controle → Som → Gravação
   - Botão direito → "Mostrar dispositivos desabilitados"
   - Habilitar "Stereo Mix"

## 🎮 Uso Simples

### Método 1: Menu Interativo
```bash
menu.bat
```
- Opção 1: Iniciar normal
- Opção 2: Iniciar como administrador (recomendado)
- Opção 3: Teste de reconhecimento
- Opção 4: Teste de captura dual

### Método 2: Direto
```bash
python voice_talk_ai.py
```

## 🔧 Testes Rápidos

### Teste Microfone
```bash
python test_speech_recognition.py
```
- Fale: "Hello, I am fine and you"
- Deve reconhecer corretamente

### Teste Captura Dual
```bash
python test_dual_audio.py
```
- Verifica microfone ✅
- Verifica sistema ⚠️ (precisa Stereo Mix)

## 🎯 Interface Principal

### Controles
- **▶️ Iniciar**: Começa tradução
- **⏸️ Pausar**: Pausa temporariamente
- **🎤 Microfone**: Liga/desliga sua voz
- **🔊 Sistema**: Liga/desliga voz do outro lado
- **🧹 Limpar**: Limpa legendas
- **➖ Minimizar**: Minimiza para bandeja

### Legendas
- **🎤 [Hora] Microfone**: Sua voz
- **🔊 [Hora] Sistema**: Voz do outro lado
- **EN**: Texto original em inglês
- **PT**: Tradução em português

## 🚨 Problemas Comuns

### "Não está pegando minha voz"
- ✅ Execute: `python test_speech_recognition.py`
- ✅ Fale mais claramente
- ✅ Ajuste volume do microfone
- ✅ Execute como administrador

### "Não está pegando áudio do sistema"
- ⚠️ Configure Stereo Mix
- ⚠️ Ou instale VB-Audio Virtual Cable
- ⚠️ Execute como administrador

### "Reconhecimento impreciso"
- ✅ Fale mais devagar
- ✅ Reduza ruído ambiente
- ✅ Use headset
- ✅ V2.0 já melhorou muito!

## 🎯 Dicas de Ouro

### Para Calls
1. Execute como administrador
2. Configure Stereo Mix
3. Use headset com microfone
4. Ambiente silencioso
5. Minimize para bandeja

### Para Melhor Qualidade
- Volume do microfone: 70-80%
- Conexão estável com internet
- Feche aplicações desnecessárias
- Modo de energia alta

## 🔄 Novidades v2.0

### Reconhecimento Melhorado
- ✅ Usa alternativa com maior confiança
- ✅ Filtros de ruído
- ✅ Normalização de áudio
- ✅ Buffer de 3 segundos

### Exemplo Real
**Antes**: "Hello i am figured out"
**Depois**: "Hello I'm fine and you" ✅

### Captura Mais Robusta
- ✅ Detecção automática de dispositivos
- ✅ Recuperação automática de erros
- ✅ Monitoramento de volume
- ✅ Tratamento de falhas

## 📞 Suporte Rápido

### Passo 1: Testes
```bash
python test_dependencies.py  # Verifica instalação
python test_dual_audio.py    # Testa dispositivos
```

### Passo 2: Configuração
```bash
configurar_stereo_mix.bat    # Configura sistema
```

### Passo 3: Execução
```bash
menu.bat                     # Menu principal
```

---

**Voice Talk AI v2.0** - Agora com reconhecimento muito mais preciso! 🎯
