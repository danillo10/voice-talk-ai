import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading
import time
import queue
from googletrans import Translator
import sys

class SimpleVoiceTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Talk AI - Teste")
        self.root.geometry("600x400")
        
        # Inicializar componentes
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()
        
        # Controle
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Interface
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        title = tk.Label(self.root, text="Voice Talk AI - Teste", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Botão
        self.btn_start = tk.Button(self.root, text="Iniciar Teste", command=self.start_test, 
                                  bg='green', fg='white', font=("Arial", 12), padx=20, pady=10)
        self.btn_start.pack(pady=10)
        
        # Área de texto
        self.text_area = tk.Text(self.root, height=15, width=70, font=("Arial", 10))
        self.text_area.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Status
        self.status_label = tk.Label(self.root, text="Status: Pronto", font=("Arial", 10))
        self.status_label.pack(pady=5)
    
    def start_test(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Iniciando teste...\n")
        
        # Teste 1: Verificar microfone
        self.text_area.insert(tk.END, "1. Testando microfone...\n")
        self.root.update()
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            self.text_area.insert(tk.END, "✓ Microfone OK\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"✗ Erro no microfone: {e}\n")
        
        # Teste 2: Verificar Google Speech
        self.text_area.insert(tk.END, "2. Testando Google Speech Recognition...\n")
        self.root.update()
        
        try:
            # Teste com áudio de exemplo
            self.text_area.insert(tk.END, "   Fale algo em inglês nos próximos 5 segundos...\n")
            self.root.update()
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language='en-US')
                self.text_area.insert(tk.END, f"✓ Reconhecido: {text}\n")
        except sr.WaitTimeoutError:
            self.text_area.insert(tk.END, "✗ Timeout - nenhum áudio detectado\n")
        except sr.UnknownValueError:
            self.text_area.insert(tk.END, "✗ Não foi possível reconhecer o áudio\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"✗ Erro no reconhecimento: {e}\n")
        
        # Teste 3: Verificar tradução
        self.text_area.insert(tk.END, "3. Testando Google Translate...\n")
        self.root.update()
        
        try:
            test_text = "Hello, how are you?"
            translation = self.translator.translate(test_text, src='en', dest='pt')
            self.text_area.insert(tk.END, f"✓ Tradução: '{test_text}' -> '{translation.text}'\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"✗ Erro na tradução: {e}\n")
        
        # Teste 4: Verificar dependências
        self.text_area.insert(tk.END, "4. Verificando dependências...\n")
        self.root.update()
        
        try:
            import pyaudio
            self.text_area.insert(tk.END, "✓ PyAudio instalado\n")
        except ImportError:
            self.text_area.insert(tk.END, "✗ PyAudio não encontrado\n")
        
        try:
            import pystray
            self.text_area.insert(tk.END, "✓ Pystray instalado\n")
        except ImportError:
            self.text_area.insert(tk.END, "✗ Pystray não encontrado\n")
        
        self.text_area.insert(tk.END, "\nTeste concluído!\n")
        self.text_area.insert(tk.END, "Se todos os testes passaram, você pode executar o programa principal.\n")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleVoiceTranslator()
    app.run()
