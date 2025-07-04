import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import time
import pyaudio
import numpy as np

def test_dual_audio():
    """Testa a captura dual de áudio"""
    print("=== TESTE DE CAPTURA DUAL DE ÁUDIO ===")
    
    # Inicializar PyAudio
    audio = pyaudio.PyAudio()
    
    # Listar dispositivos
    print("\n--- DISPOSITIVOS DISPONÍVEIS ---")
    mic_device = None
    system_device = None
    
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"[{i}] {info['name']} - Canais: {info['maxInputChannels']}")
            
            # Detectar microfone
            if 'microfone' in info['name'].lower() or 'microphone' in info['name'].lower():
                mic_device = i
                print(f"    ↳ MICROFONE DETECTADO")
            
            # Detectar stereo mix
            name_lower = info['name'].lower()
            if any(keyword in name_lower for keyword in ['stereo mix', 'what u hear', 'wave out mix', 'sum']):
                system_device = i
                print(f"    ↳ ÁUDIO DO SISTEMA DETECTADO")
    
    print(f"\n--- CONFIGURAÇÃO ---")
    print(f"Microfone: {mic_device if mic_device is not None else 'PADRÃO'}")
    print(f"Sistema: {system_device if system_device is not None else 'NÃO ENCONTRADO'}")
    
    # Teste de captura
    print(f"\n--- TESTE DE CAPTURA ---")
    
    recognizer = sr.Recognizer()
    
    # Teste 1: Microfone
    print("1. Testando MICROFONE (fale algo em 3 segundos)...")
    try:
        with sr.Microphone(device_index=mic_device) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            
        text = recognizer.recognize_google(audio_data, language='en-US')
        print(f"   ✓ MICROFONE: {text}")
    except sr.WaitTimeoutError:
        print("   ⚠️ MICROFONE: Timeout")
    except sr.UnknownValueError:
        print("   ⚠️ MICROFONE: Não reconhecido")
    except Exception as e:
        print(f"   ✗ MICROFONE: Erro - {e}")
    
    # Teste 2: Sistema (se disponível)
    if system_device is not None:
        print("\n2. Testando ÁUDIO DO SISTEMA...")
        print("   Reproduza algo no computador e aguarde 5 segundos...")
        try:
            # Usar PyAudio diretamente para capturar do sistema
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024,
                input_device_index=system_device
            )
            
            # Capturar por 3 segundos
            frames = []
            for _ in range(int(16000 / 1024 * 3)):
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Converter para AudioData
            audio_bytes = b''.join(frames)
            audio_data = sr.AudioData(audio_bytes, 16000, 2)
            
            text = recognizer.recognize_google(audio_data, language='en-US')
            print(f"   ✓ SISTEMA: {text}")
            
        except sr.UnknownValueError:
            print("   ⚠️ SISTEMA: Não reconhecido (talvez não há áudio tocando)")
        except Exception as e:
            print(f"   ✗ SISTEMA: Erro - {e}")
    else:
        print("\n2. ÁUDIO DO SISTEMA: Não disponível")
        print("   Para habilitar:")
        print("   - Painel de Controle > Som > Gravação")
        print("   - Botão direito > Mostrar dispositivos desabilitados")
        print("   - Habilitar 'Stereo Mix'")
    
    audio.terminate()
    print(f"\n--- RESULTADO ---")
    
    if mic_device is not None:
        print("✓ Microfone disponível para capturar sua voz")
    else:
        print("⚠️ Microfone pode ter problemas")
        
    if system_device is not None:
        print("✓ Áudio do sistema disponível para capturar chamadas")
    else:
        print("⚠️ Configure Stereo Mix para capturar áudio do sistema")

def main():
    print("Voice Talk AI - Teste de Captura Dual")
    print("=" * 50)
    
    # Verificar dependências
    try:
        import pyaudio
        import speech_recognition
        print("✓ Dependências OK")
    except ImportError as e:
        print(f"✗ Erro nas dependências: {e}")
        return
    
    print("\nEste teste verificará:")
    print("1. Dispositivos de áudio disponíveis")
    print("2. Captura do microfone (sua voz)")
    print("3. Captura do sistema (áudio do PC)")
    print()
    
    input("Pressione Enter para continuar...")
    
    test_dual_audio()
    
    print("\n" + "=" * 50)
    print("DICAS:")
    print("• Para calls: Ambos precisam funcionar")
    print("• Microfone: Captura sua voz")
    print("• Sistema: Captura voz do outro lado")
    print("• Se Sistema não funcionar, configure Stereo Mix")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
