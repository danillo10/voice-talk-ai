import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import speech_recognition as sr
from googletrans import Translator
import queue
import json
import os
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import sys


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
        
        # Iniciar automaticamente após 2 segundos
        self.root.after(2000, self.start_listening)
        
    def setup_ui(self):
        """Configura a interface do usuário - Lateral esquerda 15% da tela"""
        self.root.title("Voice Talk AI")
        
        # Calcular dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Definir tamanho: 15% da largura, 80% da altura
        width = int(screen_width * 0.15)
        height = int(screen_height * 0.8)
        
        # Posicionar na lateral esquerda
        x = 0
        y = int(screen_height * 0.1)  # 10% do topo
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg='#1e1e1e')
        
        # Configurar para ficar sempre no topo
        self.root.attributes('-topmost', True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Cabeçalho compacto
        header_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=1)
        header_frame.pack(fill='x', pady=(0, 5))
        
        title_label = tk.Label(header_frame, 
                              text="🎙️ Voice Talk AI", 
                              font=("Segoe UI", 10, "bold"),
                              bg='#2d2d2d', 
                              fg='#00ff88')
        title_label.pack(pady=5)
        
        # Status compacto
        self.status_label = tk.Label(header_frame, 
                                    text="🔴 ATIVO", 
                                    font=("Segoe UI", 8),
                                    bg='#2d2d2d', 
                                    fg='#00ff88')
        self.status_label.pack(pady=(0, 5))
        
        # Botões compactos
        button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        button_frame.pack(fill='x', pady=5)
        
        # Botão minimizar
        self.minimize_button = tk.Button(button_frame, 
                                        text="➖", 
                                        command=self.minimize_to_tray,
                                        bg='#555555', 
                                        fg='white',
                                        font=("Segoe UI", 8),
                                        width=3, 
                                        height=1)
        self.minimize_button.pack(side='right', padx=2)
        
        # Botão limpar
        self.clear_button = tk.Button(button_frame, 
                                     text="🧹", 
                                     command=self.clear_text,
                                     bg='#ff6b6b', 
                                     fg='white',
                                     font=("Segoe UI", 8),
                                     width=3, 
                                     height=1)
        self.clear_button.pack(side='right', padx=2)
        
        # Área de texto - Inglês
        en_label = tk.Label(main_frame, 
                           text="EN:", 
                           font=("Segoe UI", 8, "bold"),
                           bg='#1e1e1e', 
                           fg='#ffffff')
        en_label.pack(anchor='w', pady=(5, 0))
        
        self.english_text = tk.Text(main_frame, 
                                   height=12, 
                                   width=30,
                                   bg='#2d2d2d', 
                                   fg='#ffffff',
                                   font=("Segoe UI", 8),
                                   wrap=tk.WORD,
                                   relief='flat')
        self.english_text.pack(fill='both', expand=True, pady=(0, 5))
        
        # Área de texto - Português
        pt_label = tk.Label(main_frame, 
                           text="PT:", 
                           font=("Segoe UI", 8, "bold"),
                           bg='#1e1e1e', 
                           fg='#00ff88')
        pt_label.pack(anchor='w', pady=(5, 0))
        
        self.portuguese_text = tk.Text(main_frame, 
                                      height=12, 
                                      width=30,
                                      bg='#2d2d2d', 
                                      fg='#00ff88',
                                      font=("Segoe UI", 8),
                                      wrap=tk.WORD,
                                      relief='flat')
        self.portuguese_text.pack(fill='both', expand=True)
        
        # Configurar protocolo de fechamento
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
        """Configura a bandeja do sistema"""
        # Criar ícone simples
        try:
            # Criar uma imagem simples para o ícone
            image = Image.new('RGB', (64, 64), color=(0, 255, 136))
            
            # Menu do sistema
            menu = pystray.Menu(
                item('Mostrar', self.show_window),
                item('Ocultar', self.hide_window),
                item('Sair', self.quit_application)
            )
            
            self.icon = pystray.Icon("VoiceTalkAI", image, "Voice Talk AI", menu)
        except:
            self.icon = None
            
    def start_listening(self):
        """Inicia a captura de áudio"""
        if not self.is_listening:
            self.is_listening = True
            self.status_label.config(text="🔴 ESCUTANDO", fg='#00ff88')
            
            # Iniciar threads
            self.audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
            self.process_thread = threading.Thread(target=self.process_audio_loop, daemon=True)
            
            self.audio_thread.start()
            self.process_thread.start()
            
            print("✓ Captura de áudio iniciada")
            
    def stop_listening(self):
        """Para a captura de áudio"""
        self.is_listening = False
        self.status_label.config(text="⏸️ PAUSADO", fg='#ffaa00')
        
    def restart_listening(self):
        """Reinicia a captura de áudio"""
        self.stop_listening()
        time.sleep(1)
        self.start_listening()
        
    def clear_text(self):
        """Limpa os textos das legendas"""
        self.english_text.delete(1.0, tk.END)
        self.portuguese_text.delete(1.0, tk.END)
        
    def audio_loop(self):
        """Loop de captura de áudio"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Capturar áudio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Adicionar à fila
                    self.audio_queue.put(audio)
                    
            except sr.WaitTimeoutError:
                # Timeout normal, continuar
                pass
            except Exception as e:
                print(f"Erro na captura: {e}")
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
                    if text and len(text.strip()) > 0:
                        timestamp = time.strftime("%H:%M:%S")
                        formatted_text = f"[{timestamp}] {text}"
                        self.update_english_text(formatted_text)
                        
                        # Traduzir
                        try:
                            translation = self.translator.translate(text, src='en', dest='pt')
                            formatted_translation = f"[{timestamp}] {translation.text}"
                            self.update_portuguese_text(formatted_translation)
                        except Exception as e:
                            print(f"Erro na tradução: {e}")
                            
                except sr.UnknownValueError:
                    # Não conseguiu reconhecer, continuar
                    pass
                except sr.RequestError as e:
                    print(f"Erro no serviço: {e}")
                    
            except queue.Empty:
                # Fila vazia, continuar
                pass
            except Exception as e:
                print(f"Erro no processamento: {e}")
                
    def update_english_text(self, text):
        """Atualiza o texto em inglês"""
        self.root.after(0, self._update_english_text, text)
        
    def _update_english_text(self, text):
        """Atualiza o texto em inglês na thread principal"""
        self.english_text.insert(tk.END, text + "\n")
        self.english_text.see(tk.END)
        
    def update_portuguese_text(self, text):
        """Atualiza o texto em português"""
        self.root.after(0, self._update_portuguese_text, text)
        
    def _update_portuguese_text(self, text):
        """Atualiza o texto em português na thread principal"""
        self.portuguese_text.insert(tk.END, text + "\n")
        self.portuguese_text.see(tk.END)
        
    def minimize_to_tray(self):
        """Minimiza para a bandeja do sistema"""
        if self.icon:
            self.root.withdraw()
            self.is_minimized = True
            
            # Executar ícone em thread separada
            def run_icon():
                self.icon.run()
            
            threading.Thread(target=run_icon, daemon=True).start()
        else:
            self.root.iconify()
            
    def show_window(self, icon=None, item=None):
        """Mostra a janela"""
        if self.is_minimized:
            self.root.deiconify()
            self.is_minimized = False
            if self.icon:
                self.icon.stop()
                
    def hide_window(self, icon=None, item=None):
        """Oculta a janela"""
        self.minimize_to_tray()
        
    def quit_application(self, icon=None, item=None):
        """Fecha a aplicação"""
        self.is_listening = False
        if self.icon:
            self.icon.stop()
        self.root.quit()
        sys.exit()
        
    def on_closing(self):
        """Ao fechar a janela"""
        self.minimize_to_tray()
        
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()


def main():
    app = VoiceTalkAI()
    app.run()


if __name__ == "__main__":
    main()
