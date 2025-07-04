# 🎙️ Voice Talk AI - Real-time Speech Recognition & Translation

Uma aplicação desktop em Python que captura e traduz em tempo real todo o áudio do PC (microfone e sistema), exibindo legendas em inglês e português, ideal para uso em calls e reuniões.

## 🚀 Principais Funcionalidades

- **🎤 Captura de Áudio Dupla**: Microfone + Sistema (Stereo Mix)
- **🤖 IA Whisper**: Reconhecimento de voz de alta precisão
- **📝 Correção Automática**: IA corrige texto transcrito
- **🌐 Tradução Instantânea**: Inglês → Português em tempo real
- **📱 Interface Lateral**: Compacta (15% da tela) sempre no topo
- **🔄 Auto-Start**: Inicia automaticamente no boot
- **🎯 Filtros Anti-Ruído**: Evita transcrições aleatórias
- **� Sempre Ativo**: Funciona em segundo plano

- **Captura de áudio do sistema**: Captura todo o áudio que está sendo reproduzido no seu PC
- **Reconhecimento de fala**: Converte áudio em texto usando Google Speech Recognition
- **Tradução automática**: Traduz automaticamente do inglês para português
- **Interface moderna**: Interface gráfica elegante e intuitiva
- **Legendas em tempo real**: Mostra tanto o texto original quanto a tradução
- **Minimização para bandeja**: Funciona em segundo plano
- **Timestamps**: Registra horário de cada fala capturada
- **Scroll automático**: Acompanha automaticamente as novas traduções

## 🛠️ Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Windows 10/11 (recomendado)
- Acesso à internet para tradução

### Instalação Automática
1. Execute `install.bat` como administrador
2. Aguarde a instalação das dependências
3. Execute `run.bat` para iniciar a aplicação

### Instalação Manual
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python voice_talk_ai.py
```

## ⚙️ Configuração do Sistema

### Habilitar Stereo Mix (Essencial)
Para capturar áudio do sistema, você precisa habilitar o Stereo Mix:

1. Clique com o botão direito no ícone de som na bandeja do sistema
2. Selecione "Dispositivos de gravação" ou "Sons"
3. Vá para a aba "Gravação"
4. Clique com o botão direito no espaço vazio
5. Marque "Mostrar dispositivos desabilitados"
6. Encontre "Stereo Mix" ou "Mixagem Estéreo"
7. Clique com o botão direito e selecione "Habilitar"
8. (Opcional) Defina como dispositivo padrão

### Executar como Administrador
Para melhor captura de áudio do sistema, execute a aplicação como administrador.

## 🖥️ Como Usar

1. **Inicie a aplicação**: Execute `run.bat` ou `python voice_talk_ai.py`
2. **Clique em "Iniciar Captura"**: A aplicação começará a capturar áudio
3. **Visualize as traduções**: 
   - Texto original aparece na área superior
   - Tradução em português aparece na área inferior
4. **Controles disponíveis**:
   - **Parar Captura**: Para a captura de áudio
   - **Limpar**: Remove todo o texto das áreas
   - **Minimizar**: Minimiza para a bandeja do sistema

## 📁 Estrutura do Projeto

```
voice-talk-ai/
├── voice_talk_ai.py      # Aplicação principal
├── main.py              # Versão alternativa (microfone)
├── requirements.txt     # Dependências Python
├── install.bat         # Script de instalação
├── run.bat             # Script de execução
├── settings.json       # Configurações (criado automaticamente)
└── readme.md          # Documentação
```

## 🔧 Dependências

- **PyAudio**: Captura de áudio
- **SpeechRecognition**: Reconhecimento de fala
- **googletrans**: Tradução automática
- **pystray**: Ícone na bandeja do sistema
- **Pillow**: Manipulação de imagens
- **numpy**: Processamento de dados de áudio
- **tkinter**: Interface gráfica (incluído no Python)

## 🎯 Casos de Uso

- **Calls internacionais**: Tradução em tempo real durante chamadas
- **Vídeos em inglês**: Legendas automáticas em português
- **Reuniões online**: Acompanhamento de reuniões em inglês
- **Streaming**: Tradução de lives e streams
- **Educação**: Auxílio em aulas e cursos online

## 🔍 Solução de Problemas

### Erro "Não foi possível iniciar a captura de áudio"
- Verifique se o Stereo Mix está habilitado
- Execute a aplicação como administrador
- Verifique se não há outros programas usando o áudio

### Erro de reconhecimento de fala
- Verifique sua conexão com a internet
- Certifique-se de que há áudio sendo reproduzido
- Ajuste o volume do sistema

### Erro de tradução
- Verifique sua conexão com a internet
- O Google Translate pode ter limites de uso

### PyAudio não instala
- Baixe o arquivo .whl correto de https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Instale com: `pip install nome_do_arquivo.whl`
- Ou use conda: `conda install pyaudio`

## ⚠️ Limitações

- Requer conexão à internet para reconhecimento de fala e tradução
- Funciona melhor com áudio claro e sem muito ruído
- Tradução limitada pelo Google Translate
- Reconhecimento otimizado para inglês

## 🔒 Privacidade

- O áudio é processado pelos serviços do Google (Speech Recognition e Translate)
- Nenhum áudio é armazenado localmente
- As configurações são salvas apenas no seu computador

## 🛡️ Segurança

- Execute sempre de fontes confiáveis
- Mantenha as dependências atualizadas
- Use apenas em redes seguras

## 📝 Changelog

### v1.0.0
- Primeira versão
- Captura de áudio do sistema
- Tradução inglês-português
- Interface moderna
- Minimização para bandeja

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Contribuir com código

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Se você encontrar problemas ou tiver dúvidas:
1. Verifique a seção de solução de problemas
2. Verifique se todas as dependências estão instaladas
3. Certifique-se de que o Stereo Mix está habilitado

---

**Desenvolvido com ❤️ para facilitar a comunicação global**