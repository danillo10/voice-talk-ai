# Filtros Anti-Ruído - Voice Talk AI

## Problema Resolvido
O sistema estava transcrevendo áudio aleatório e ruído de fundo, gerando transcrições como "Unlinked", "keep pulsing", "see you lahi m Hiliffine" sem o usuário falar.

## Correções Implementadas

### 1. Correção do Erro `energy_threshold`
- **Problema**: O parâmetro `energy_threshold` estava sendo passado incorretamente para a função `listen()`
- **Correção**: Removido o parâmetro inválido da função `listen()`, mantendo apenas a configuração no `recognizer`

### 2. Filtros de Áudio Mais Restritivos
- **Energy Threshold**: Aumentado de 4000 para 6000
- **Volume Threshold**: Aumentado de 300 para 800
- **Duração Mínima**: Aumentada de 0.5s para 1.0s
- **Pause Threshold**: Aumentado de 1.0 para 1.2
- **Phrase Threshold**: Aumentado de 0.5 para 0.8
- **Non-Speaking Duration**: Aumentado de 0.8 para 1.0

### 3. Filtros do Whisper Mais Restritivos
- **Compression Ratio**: Reduzido de 2.4 para 2.2 (mais restritivo)
- **Log Prob Threshold**: Aumentado de -1.0 para -0.8 (mais restritivo)
- **No Speech Threshold**: Aumentado de 0.6 para 0.8 (mais restritivo)

### 4. Filtros de Texto Mais Restritivos
- **Tamanho Mínimo**: Aumentado de 3 para 5 caracteres
- **Palavras Bloqueadas**: Expandida lista de palavras comuns que são ignoradas
- **Verificação de Palavras**: Deve conter pelo menos uma palavra com mais de 2 caracteres

## Configuração Personalizável

O arquivo `config.json` permite ajustar todos os filtros:

```json
{
    "audio_filters": {
        "energy_threshold": 6000,
        "volume_threshold": 800,
        "min_audio_length": 16000,
        "pause_threshold": 1.2,
        "phrase_threshold": 0.8,
        "non_speaking_duration": 1.0
    },
    "whisper_filters": {
        "temperature": 0.0,
        "compression_ratio_threshold": 2.2,
        "logprob_threshold": -0.8,
        "no_speech_threshold": 0.8
    },
    "text_filters": {
        "min_text_length": 5,
        "min_word_length": 2,
        "blocked_words": ["you", "thank you", "thanks", "yeah", "yes", "no", "ok", "okay", "um", "uh", "hmm"]
    }
}
```

## Como Ajustar

### Se o Sistema Não Detecta Sua Fala:
- Diminua `energy_threshold` e `volume_threshold`
- Diminua `no_speech_threshold` e `logprob_threshold`

### Se o Sistema Detecta Muito Ruído:
- Aumente `energy_threshold` e `volume_threshold`
- Aumente `no_speech_threshold` e `compression_ratio_threshold`

## Teste dos Filtros

Execute `test_filters.py` para testar se os filtros estão funcionando corretamente:

```
python test_filters.py
```

## Status Atual

✅ **Erro corrigido**: Parâmetro `energy_threshold` inválido removido
✅ **Filtros aplicados**: Sistema muito mais restritivo contra ruído
✅ **Teste realizado**: Sistema não gera mais transcrições aleatórias
✅ **Configuração**: Arquivo JSON para personalização dos filtros
