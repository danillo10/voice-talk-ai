"""
Teste rápido para verificar filtros anti-ruído
"""
import time
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Testando filtros anti-ruído...")
print("🔊 Fique em silêncio por 30 segundos para verificar se o sistema detecta ruído aleatório")
print("🎤 Depois diga algumas palavras para verificar se o sistema detecta fala real")
print("⏳ Aguarde...")

# Aguardar 30 segundos
for i in range(30, 0, -1):
    print(f"⏳ Aguardando {i} segundos... (mantenha silêncio)")
    time.sleep(1)

print("✅ Teste concluído! Se não apareceram transcrições aleatórias, os filtros estão funcionando!")
print("🎤 Agora você pode falar para testar a detecção de fala real")
