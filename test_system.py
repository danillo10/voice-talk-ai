import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading
import time
import queue
from googletrans import Translator
import sys

def test_microphone():
    """Testa se o microfone está funcionando"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Ajustando para ruído ambiente...")
            r.adjust_for_ambient_noise(source)
            print("Microfone OK!")
            return True
    except Exception as e:
        print(f"Erro no microfone: {e}")
        return False

def test_speech_recognition():
    """Testa o reconhecimento de fala"""
    try:
        r = sr.Recognizer()
        # Teste com áudio de exemplo
        print("Testando reconhecimento de fala...")
        print("Fale algo em inglês nos próximos 5 segundos...")
        
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='en-US')
            print(f"Reconhecido: {text}")
            return text
    except sr.WaitTimeoutError:
        print("Timeout - nenhum áudio detectado")
        return None
    except sr.UnknownValueError:
        print("Não foi possível reconhecer o áudio")
        return None
    except Exception as e:
        print(f"Erro no reconhecimento: {e}")
        return None

def test_translation():
    """Testa a tradução"""
    try:
        translator = Translator()
        test_text = "Hello, how are you today?"
        translation = translator.translate(test_text, src='en', dest='pt')
        print(f"Tradução: '{test_text}' -> '{translation.text}'")
        return True
    except Exception as e:
        print(f"Erro na tradução: {e}")
        return False

def test_dependencies():
    """Testa todas as dependências"""
    print("=== TESTE DE DEPENDÊNCIAS ===")
    
    # Teste PyAudio
    try:
        import pyaudio
        print("✓ PyAudio instalado")
    except ImportError:
        print("✗ PyAudio não encontrado")
        return False
    
    # Teste SpeechRecognition
    try:
        import speech_recognition
        print("✓ SpeechRecognition instalado")
    except ImportError:
        print("✗ SpeechRecognition não encontrado")
        return False
    
    # Teste googletrans
    try:
        import googletrans
        print("✓ googletrans instalado")
    except ImportError:
        print("✗ googletrans não encontrado")
        return False
    
    # Teste pystray
    try:
        import pystray
        print("✓ pystray instalado")
    except ImportError:
        print("✗ pystray não encontrado")
    
    return True

def main():
    print("Voice Talk AI - Teste de Sistema")
    print("=" * 40)
    
    # Teste 1: Dependências
    if not test_dependencies():
        print("\nERRO: Dependências não instaladas corretamente")
        print("Execute: pip install -r requirements.txt")
        return
    
    print("\n=== TESTE FUNCIONAL ===")
    
    # Teste 2: Microfone
    if not test_microphone():
        print("ERRO: Problema com o microfone")
        return
    
    # Teste 3: Reconhecimento de fala
    print("\n=== TESTE DE RECONHECIMENTO ===")
    recognized_text = test_speech_recognition()
    
    # Teste 4: Tradução
    print("\n=== TESTE DE TRADUÇÃO ===")
    if test_translation():
        print("✓ Tradução funcionando")
    else:
        print("✗ Problema na tradução")
    
    # Se reconheceu algo, traduzir
    if recognized_text:
        try:
            translator = Translator()
            translation = translator.translate(recognized_text, src='en', dest='pt')
            print(f"\nSUA FRASE TRADUZIDA:")
            print(f"Inglês: {recognized_text}")
            print(f"Português: {translation.text}")
        except Exception as e:
            print(f"Erro ao traduzir sua frase: {e}")
    
    print("\n=== RESULTADO ===")
    if recognized_text:
        print("✓ SISTEMA FUNCIONANDO CORRETAMENTE!")
        print("\nVocê pode executar:")
        print("- python voice_talk_ai.py (aplicação completa)")
        print("- python main.py (aplicação simples)")
    else:
        print("✗ Sistema com problemas")
        print("Verifique:")
        print("- Conexão com internet")
        print("- Microfone funcionando")
        print("- Fale claramente em inglês")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        input("\nPressione Enter para sair...")
