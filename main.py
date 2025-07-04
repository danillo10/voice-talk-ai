import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import speech_recognition as sr
from googletrans import Translator
import pyaudio
import wave
import io
import queue
import json
import os
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item


class VoiceTalkAI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.setup_audio()
        self.setup_translation()
        self.setup_system_tray()
        
        # Controle de estado
        self.is_listening = False
        self.is_minimized = False
        self.audio_queue = queue.Queue()
        self.translation_queue = queue.Queue()
        
        # Configurações
        self.settings = self.load_settings()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        self.root.title("Voice Talk AI - Tradutor de Áudio")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Configurar para ficar sempre no topo
        self.root.attributes('-topmost', True)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="Voice Talk AI", 
                              font=("Arial", 24, "bold"),
                              bg='#2b2b2b', 
                              fg='#ffffff')
        title_label.pack(pady=(0, 20))
        
        # Status
        self.status_label = tk.Label(main_frame, 
                                    text="Status: Parado", 
                                    font=("Arial", 12),
                                    bg='#2b2b2b', 
                                    fg='#ff4444')
        self.status_label.pack(pady=(0, 10))
        
        # Botões de controle
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(pady=(0, 20))
        
        self.start_button = tk.Button(button_frame, 
                                     text="Iniciar Captura", 
                                     command=self.start_listening,
                                     bg='#4CAF50', 
                                     fg='white',
                                     font=("Arial", 12, "bold"),
                                     padx=20, 
                                     pady=10)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(button_frame, 
                                    text="Parar Captura", 
                                    command=self.stop_listening,
                                    bg='#f44336', 
                                    fg='white',
                                    font=("Arial", 12, "bold"),
                                    padx=20, 
                                    pady=10,
                                    state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        self.minimize_button = tk.Button(button_frame, 
                                        text="Minimizar", 
                                        command=self.minimize_to_tray,
                                        bg='#2196F3', 
                                        fg='white',
                                        font=("Arial", 12, "bold"),
                                        padx=20, 
                                        pady=10)
        self.minimize_button.pack(side='left', padx=5)
        
        # Área de legendas
        subtitle_frame = tk.Frame(main_frame, bg='#2b2b2b')
        subtitle_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Legenda em inglês
        english_label = tk.Label(subtitle_frame, 
                                text="Inglês:", 
                                font=("Arial", 12, "bold"),
                                bg='#2b2b2b', 
                                fg='#ffffff')
        english_label.pack(anchor='w')
        
        self.english_text = tk.Text(subtitle_frame, 
                                   height=8, 
                                   width=80,
                                   bg='#1e1e1e', 
                                   fg='#ffffff',
                                   font=("Arial", 11),
                                   wrap='word')
        self.english_text.pack(fill='both', expand=True, pady=(5, 10))
        
        # Legenda em português
        portuguese_label = tk.Label(subtitle_frame, 
                                   text="Português:", 
                                   font=("Arial", 12, "bold"),
                                   bg='#2b2b2b', 
                                   fg='#ffffff')
        portuguese_label.pack(anchor='w')
        
        self.portuguese_text = tk.Text(subtitle_frame, 
                                      height=8, 
                                      width=80,
                                      bg='#1e1e1e', 
                                      fg='#00ff00',
                                      font=("Arial", 11),
                                      wrap='word')
        self.portuguese_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Configurar estilo
        style = ttk.Style()
        style.configure('Dark.TFrame', background='#2b2b2b')
        
        # Bind para minimizar ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_audio(self):
        """Configura o sistema de áudio"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Ajustar para ruído ambiente
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
    def setup_translation(self):
        """Configura o tradutor"""
        self.translator = Translator()
        
    def setup_system_tray(self):
        """Configura o ícone da bandeja do sistema"""
        # Criar um ícone simples
        image = Image.new('RGB', (64, 64), color='blue')
        
        menu = pystray.Menu(
            item('Mostrar', self.show_window),
            item('Sair', self.quit_app)
        )
        
        self.icon = pystray.Icon("VoiceTalkAI", image, "Voice Talk AI", menu)
        
    def load_settings(self):
        """Carrega configurações do arquivo"""
        settings_file = "settings.json"
        default_settings = {
            "always_on_top": True,
            "auto_translate": True,
            "language_from": "en",
            "language_to": "pt"
        }
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except:
                return default_settings
        return default_settings
    
    def save_settings(self):
        """Salva configurações no arquivo"""
        with open("settings.json", 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def start_listening(self):
        """Inicia a captura de áudio"""
        if not self.is_listening:
            self.is_listening = True
            self.status_label.config(text="Status: Capturando áudio...", fg='#00ff00')
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            
            # Iniciar thread de captura de áudio
            self.audio_thread = threading.Thread(target=self.audio_capture_loop)
            self.audio_thread.daemon = True
            self.audio_thread.start()
            
            # Iniciar thread de processamento
            self.process_thread = threading.Thread(target=self.process_audio_loop)
            self.process_thread.daemon = True
            self.process_thread.start()
    
    def stop_listening(self):
        """Para a captura de áudio"""
        self.is_listening = False
        self.status_label.config(text="Status: Parado", fg='#ff4444')
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
    
    def audio_capture_loop(self):
        """Loop principal de captura de áudio"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Capturar áudio com timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self.audio_queue.put(audio)
            except sr.WaitTimeoutError:
                # Timeout normal, continuar
                pass
            except Exception as e:
                print(f"Erro na captura de áudio: {e}")
                time.sleep(0.1)
    
    def process_audio_loop(self):
        """Loop de processamento de áudio"""
        while self.is_listening:
            try:
                # Pegar áudio da fila
                audio = self.audio_queue.get(timeout=1)
                
                # Reconhecer fala
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    if text:
                        self.update_english_text(text)
                        
                        # Traduzir
                        try:
                            translation = self.translator.translate(text, src='en', dest='pt')
                            self.update_portuguese_text(translation.text)
                        except Exception as e:
                            print(f"Erro na tradução: {e}")
                            
                except sr.UnknownValueError:
                    # Não conseguiu reconhecer, continuar
                    pass
                except sr.RequestError as e:
                    print(f"Erro no serviço de reconhecimento: {e}")
                    
            except queue.Empty:
                # Fila vazia, continuar
                pass
            except Exception as e:
                print(f"Erro no processamento: {e}")
    
    def update_english_text(self, text):
        """Atualiza o texto em inglês"""
        self.root.after(0, self._update_english_text, text)
    
    def _update_english_text(self, text):
        """Atualiza o texto em inglês (thread-safe)"""
        self.english_text.insert(tk.END, text + "\n")
        self.english_text.see(tk.END)
        
        # Limitar número de linhas
        lines = self.english_text.get("1.0", tk.END).split('\n')
        if len(lines) > 50:
            self.english_text.delete("1.0", "2.0")
    
    def update_portuguese_text(self, text):
        """Atualiza o texto em português"""
        self.root.after(0, self._update_portuguese_text, text)
    
    def _update_portuguese_text(self, text):
        """Atualiza o texto em português (thread-safe)"""
        self.portuguese_text.insert(tk.END, text + "\n")
        self.portuguese_text.see(tk.END)
        
        # Limitar número de linhas
        lines = self.portuguese_text.get("1.0", tk.END).split('\n')
        if len(lines) > 50:
            self.portuguese_text.delete("1.0", "2.0")
    
    def minimize_to_tray(self):
        """Minimiza para a bandeja do sistema"""
        self.root.withdraw()
        self.is_minimized = True
        
        # Iniciar ícone da bandeja em uma thread separada
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def show_window(self, icon=None, item=None):
        """Mostra a janela"""
        if self.is_minimized:
            self.icon.stop()
            self.root.deiconify()
            self.is_minimized = False
    
    def on_closing(self):
        """Chamado quando a janela é fechada"""
        self.minimize_to_tray()
    
    def quit_app(self, icon=None, item=None):
        """Sai da aplicação"""
        self.is_listening = False
        self.save_settings()
        if self.is_minimized:
            self.icon.stop()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()


if __name__ == "__main__":
    # Verificar se as dependências estão instaladas
    try:
        import speech_recognition
        import googletrans
        import pyaudio
        import pystray
        from PIL import Image
    except ImportError as e:
        messagebox.showerror("Erro", f"Dependência não encontrada: {e}\nInstale as dependências executando: pip install -r requirements.txt")
        exit(1)
    
    app = VoiceTalkAI()
    app.run()
