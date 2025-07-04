import speech_recognition as sr
import time

def test_simple_recognition():
    """Teste simples e direto do reconhecimento"""
    print("=== TESTE SIMPLES DE RECONHECIMENTO ===")
    
    # Configurar reconhecedor
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    
    # Configurar microfone
    microphone = sr.Microphone()
    
    try:
        # Calibrar
        with microphone as source:
            print("Calibrando microfone...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✓ Microfone calibrado")
        
        # Teste de captura
        print("\n🎤 TESTE DE CAPTURA:")
        print("Fale algo em inglês nos próximos 5 segundos...")
        
        with microphone as source:
            print("🔴 ESCUTANDO...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("⏸️ Captura concluída")
        
        # Reconhecer
        print("🧠 Processando...")
        text = recognizer.recognize_google(audio, language='en-US')
        print(f"✅ RECONHECIDO: '{text}'")
        
        return True
        
    except sr.WaitTimeoutError:
        print("❌ Timeout - nenhum áudio detectado")
        return False
    except sr.UnknownValueError:
        print("❌ Não foi possível reconhecer o áudio")
        return False
    except sr.RequestError as e:
        print(f"❌ Erro no serviço: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    test_simple_recognition()
