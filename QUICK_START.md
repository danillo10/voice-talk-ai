# 🎯 GUIA RÁPIDO - VOICE TALK AI SEMPRE ATIVO

## ⚡ Instalação e Configuração

1. **Execute o instalador**:
   ```
   Clique duas vezes em install.bat
   ```

2. **Configure para sempre ativo**:
   ```
   Clique duas vezes em run.bat
   Escolha opção 4 (Modo SEMPRE ATIVO)
   ```

## � MODO SEMPRE ATIVO

O Voice Talk AI agora **inicia automaticamente** e fica **sempre capturando áudio**!

### ✨ Recursos Automáticos:
- ✅ **Auto-start**: Inicia captura automaticamente
- ✅ **Auto-restart**: Reinicia em caso de erro
- ✅ **Monitoramento**: Verifica se está funcionando
- ✅ **Keep-alive**: Mantém sempre ativo
- ✅ **Bandeja do sistema**: Funciona em segundo plano

### 🎮 Controles Disponíveis:
- **🔄 Reiniciar**: Reinicia a captura
- **⏸️ Pausar**: Pausa temporariamente
- **🗑️ Limpar**: Limpa as legendas
- **⬇️ Minimizar**: Envia para bandeja

## 🚀 Formas de Executar

### 1. Modo Sempre Ativo (Recomendado)
```
run.bat → opção 4
```
- Inicia automaticamente
- Mantém sempre ativo
- Reinicia se der erro

### 2. Gerenciador com Auto-restart
```
run.bat → opção 6
```
- Monitora o processo
- Reinicia automaticamente
- Máximo 10 tentativas

### 3. Inicialização Automática do Windows
```
run.bat → opção 5
```
- Adiciona ao Windows Startup
- Inicia junto com o Windows
- Sempre disponível

## 🔧 Configuração Inicial

### 1. Habilitar Stereo Mix (ESSENCIAL)
1. Clique direito no ícone de som
2. "Dispositivos de gravação"
3. Clique direito no espaço vazio
4. "Mostrar dispositivos desabilitados"
5. Habilite "Stereo Mix"

### 2. Executar como Administrador
- Clique direito em run.bat
- "Executar como administrador"

## 💡 Como Usar em Calls

1. **Antes da call**:
   - Execute em modo sempre ativo
   - Minimize para bandeja

2. **Durante a call**:
   - As legendas aparecem automaticamente
   - Inglês na área superior
   - Português na área inferior

3. **Controle**:
   - Use ⏸️ Pausar se necessário
   - Use 🔄 Reiniciar se der problema

## 🔧 Solução de Problemas

### Erro: "Não foi possível iniciar a captura de áudio"
- Verifique se o Stereo Mix está habilitado
- Execute a aplicação como administrador
- Teste com `python test_dependencies.py`

### Erro: "Dependência não encontrada"
- Execute `install.bat` novamente
- Verifique se Python está instalado corretamente

### Não reconhece nenhum áudio
- Certifique-se de que há áudio sendo reproduzido
- Verifique se o volume está audível
- Teste com diferentes fontes de áudio

## 📋 Arquivos Importantes

- `voice_talk_ai.py` - Aplicação principal (mais recursos)
- `main.py` - Aplicação simples (usa microfone)
- `test_dependencies.py` - Teste de dependências
- `install.bat` - Instalador automático
- `run.bat` - Launcher da aplicação

## 🔄 Atualizações

Para atualizar as dependências:
```
pip install --upgrade -r requirements.txt
```

## 💡 Dicas de Uso

1. **Para calls**: Execute antes de iniciar a chamada
2. **Para vídeos**: Ajuste o volume para um nível audível
3. **Para melhor performance**: Feche outros programas pesados
4. **Para usar em segundo plano**: Clique em "Minimizar"

## 🚨 Problemas Conhecidos

- **PyAudio**: Pode requerer Visual C++ Build Tools
- **Google Services**: Requer conexão com internet
- **Stereo Mix**: Pode não estar disponível em todos os PCs

## 📞 Uso em Calls

Perfect para:
- Microsoft Teams
- Zoom
- Discord
- Skype
- Google Meet

Basta deixar a aplicação rodando em segundo plano!
