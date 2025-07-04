import speech_recognition as sr
import pyaudio
import numpy as np
import time

def test_speech_recognition():
    """Teste focado no reconhecimento de voz"""
    print("=== TESTE DE RECONHECIMENTO DE VOZ ===")
    
    # Configurar reconhecedor otimizado
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5
    
    # Configurar PyAudio
    audio = pyaudio.PyAudio()
    
    # Encontrar microfone
    mic_device = None
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"Microfone encontrado: {info['name']}")
            mic_device = i
            break
    
    if mic_device is None:
        print("❌ Nenhum microfone encontrado!")
        return
    
    # Teste de captura
    print("\n🎤 Teste de captura de áudio:")
    print("1. Fale claramente: 'Hello, I am fine and you'")
    print("2. Aguarde 3 segundos...")
    input("Pressione Enter para começar...")
    
    try:
        # Capturar áudio
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
            input_device_index=mic_device
        )
        
        print("🔴 GRAVANDO... (fale agora)")
        
        # Capturar 4 segundos de áudio
        frames = []
        for i in range(0, int(16000 / 1024 * 4)):
            data = stream.read(1024)
            frames.append(data)
        
        print("⏸️ Gravação finalizada")
        
        # Parar stream
        stream.stop_stream()
        stream.close()
        
        # Converter para formato do speech_recognition
        audio_data = b''.join(frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Normalizar
        max_val = np.max(np.abs(audio_array))
        if max_val > 0:
            audio_array = (audio_array / max_val * 32767.0).astype(np.int16)
        
        # Criar AudioData
        audio_sr = sr.AudioData(audio_array.tobytes(), 16000, 2)
        
        # Testar reconhecimento
        print("\n🧠 Processando reconhecimento...")
        
        try:
            # Teste com diferentes configurações
            print("\n--- Teste 1: Configuração padrão ---")
            text1 = recognizer.recognize_google(audio_sr, language='en-US')
            print(f"✓ Reconhecido: '{text1}'")
        except sr.UnknownValueError:
            print("❌ Não conseguiu reconhecer (padrão)")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        try:
            print("\n--- Teste 2: Com show_all ---")
            results = recognizer.recognize_google(audio_sr, language='en-US', show_all=True)
            if results:
                print(f"✓ Alternativas: {results}")
            else:
                print("❌ Nenhum resultado")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        try:
            print("\n--- Teste 3: Com filtro de ruído ---")
            # Aplicar filtro simples
            filtered_audio = audio_array[audio_array > 100]  # Remover ruído baixo
            if len(filtered_audio) > 1000:
                audio_sr_filtered = sr.AudioData(filtered_audio.tobytes(), 16000, 2)
                text3 = recognizer.recognize_google(audio_sr_filtered, language='en-US')
                print(f"✓ Reconhecido (filtrado): '{text3}'")
            else:
                print("❌ Áudio muito baixo após filtro")
        except sr.UnknownValueError:
            print("❌ Não conseguiu reconhecer (filtrado)")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # Análise do áudio
        print(f"\n📊 Análise do áudio:")
        print(f"   - Volume médio: {np.mean(np.abs(audio_array)):.0f}")
        print(f"   - Volume máximo: {np.max(np.abs(audio_array)):.0f}")
        print(f"   - Duração: {len(audio_array) / 16000:.1f}s")
        print(f"   - Amostras: {len(audio_array)}")
        
    except Exception as e:
        print(f"❌ Erro na captura: {e}")
    
    finally:
        audio.terminate()

if __name__ == "__main__":
    test_speech_recognition()
