# Configuração do Sistema para Voice Talk AI

## Habilitar Stereo Mix no Windows

### Windows 10/11

1. **Abrir Configurações de Som**:
   - Clique com o botão direito no ícone de som na bandeja do sistema
   - Selecione "Dispositivos de gravação" ou "Sons"

2. **Acessar Dispositivos de Gravação**:
   - Na janela que abrir, clique na aba "Gravação"

3. **Mostrar Dispositivos Desabilitados**:
   - Clique com o botão direito em qualquer espaço vazio na lista
   - Marque "Mostrar dispositivos desabilitados"
   - Marque também "Mostrar dispositivos desconectados"

4. **Habilitar Stereo Mix**:
   - Você deve ver "Stereo Mix" ou "Mixagem Estéreo" na lista
   - Clique com o botão direito sobre ele
   - Selecione "Habilitar"

5. **Definir como Dispositivo Padrão** (Opcional):
   - Clique com o botão direito no "Stereo Mix" habilitado
   - Selecione "Definir como dispositivo padrão"

### Se Stereo Mix não aparecer:

1. **Verificar Driver de Áudio**:
   - Abra o Gerenciador de Dispositivos
   - Expanda "Controladores de som, vídeo e jogos"
   - Clique com o botão direito no seu dispositivo de áudio
   - Selecione "Atualizar driver"

2. **Habilitar no Driver**:
   - Alguns drivers têm suas próprias configurações
   - Procure por "Realtek HD Audio Manager" ou similar no painel de controle
   - Procure por opções de "Stereo Mix" ou "Gravação"

3. **Alternativa - VB-Audio Virtual Cable**:
   - Baixe o VB-Audio Virtual Cable (gratuito)
   - Instale e configure como dispositivo de saída
   - Configure a aplicação para usar este dispositivo

## Executar como Administrador

### Windows 10/11

1. **Localizar o arquivo**:
   - Navegue até a pasta do Voice Talk AI
   - Encontre `run.bat` ou `voice_talk_ai.py`

2. **Executar como Administrador**:
   - Clique com o botão direito no arquivo
   - Selecione "Executar como administrador"
   - Confirme na janela de UAC

3. **Criar Atalho com Privilégios**:
   - Clique com o botão direito no `run.bat`
   - Selecione "Criar atalho"
   - Clique com o botão direito no atalho
   - Selecione "Propriedades"
   - Clique em "Avançado..."
   - Marque "Executar como administrador"

## Configurar Permissões de Microfone

### Windows 10/11

1. **Abrir Configurações**:
   - Pressione Win + I
   - Vá para "Privacidade e segurança"

2. **Permissões de Microfone**:
   - Clique em "Microfone" na barra lateral
   - Certifique-se de que "Acesso ao microfone" está habilitado
   - Certifique-se de que "Permitir que aplicativos acessem seu microfone" está habilitado

## Firewall e Antivírus

### Windows Defender

1. **Adicionar Exceção**:
   - Abra o Windows Defender
   - Vá para "Proteção contra vírus e ameaças"
   - Clique em "Gerenciar configurações" em "Configurações de proteção contra vírus e ameaças"
   - Role para baixo e clique em "Adicionar ou remover exclusões"
   - Clique em "Adicionar uma exclusão"
   - Selecione "Pasta" e adicione a pasta do Voice Talk AI

### Firewall

1. **Permitir através do Firewall**:
   - Abra o Painel de Controle
   - Vá para "Sistema e Segurança" > "Firewall do Windows Defender"
   - Clique em "Permitir um aplicativo ou recurso através do Firewall do Windows Defender"
   - Clique em "Permitir outro aplicativo..."
   - Navegue até o Python.exe e adicione

## Teste de Áudio

### Verificar Captura de Áudio

1. **Abrir Gravador de Som**:
   - Pressione Win + R
   - Digite `soundrecorder` e pressione Enter

2. **Testar Gravação**:
   - Reproduza algo no computador (música, vídeo)
   - Inicie a gravação no Gravador de Som
   - Se você ouvir o áudio reproduzido na gravação, o Stereo Mix está funcionando

### Teste com Voice Talk AI

1. **Reproduzir Áudio em Inglês**:
   - Abra um vídeo no YouTube em inglês
   - Certifique-se de que o volume está audível

2. **Iniciar Captura**:
   - Abra o Voice Talk AI
   - Clique em "Iniciar Captura"
   - Verifique se o texto em inglês aparece na área superior
   - Verifique se a tradução aparece na área inferior

## Solução de Problemas Comuns

### "Stereo Mix não está disponível"
- Atualize os drivers de áudio
- Verifique se sua placa de som suporta Stereo Mix
- Use alternativas como VB-Audio Virtual Cable

### "Erro de permissão"
- Execute como administrador
- Verifique permissões de microfone no Windows
- Desative temporariamente o antivírus para teste

### "Sem reconhecimento de fala"
- Verifique conexão com a internet
- Certifique-se de que há áudio sendo reproduzido
- Ajuste o volume do sistema
- Verifique se o microfone não está silenciado

### "Erro de tradução"
- Verifique conexão com a internet
- Aguarde alguns segundos e tente novamente
- Verifique se não há bloqueios de firewall

## Dicas de Performance

1. **Feche aplicações desnecessárias** para melhor performance
2. **Use conexão estável** para melhor reconhecimento e tradução
3. **Ajuste o volume** para um nível audível mas não muito alto
4. **Minimize ruído de fundo** para melhor reconhecimento
5. **Execute como administrador** para melhor acesso ao áudio do sistema
