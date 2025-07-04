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
        """Configura a interface do usuário"""
        self.root.title("Voice Talk AI - Tradutor Automático")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # Configurar para ficar sempre no topo
        self.root.attributes('-topmost', True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 15))
        
        title_label = tk.Label(header_frame, 
                              text="🎙️ Voice Talk AI - ATIVO", 
                              font=("Segoe UI", 28, "bold"),
                              bg='#2d2d2d', 
                              fg='#00ff88')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Tradutor Automático - Sempre Ativo", 
                                 font=("Segoe UI", 14),
                                 bg='#2d2d2d', 
                                 fg='#cccccc')
        subtitle_label.pack(pady=(0, 15))
        
        # Status
        self.status_label = tk.Label(header_frame, 
                                    text="🔄 Iniciando automaticamente...", 
                                    font=("Segoe UI", 14, "bold"),
                                    bg='#2d2d2d', 
                                    fg='#ffaa00')
        self.status_label.pack(pady=(0, 15))
        
        # Botões de controle
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        control_frame.pack(fill='x', pady=(0, 15))
        
        button_frame = tk.Frame(control_frame, bg='#2d2d2d')
        button_frame.pack(pady=15)
        
        self.start_button = tk.Button(button_frame, 
                                     text="🔄 Reiniciar", 
                                     command=self.restart_listening,
                                     bg='#4CAF50', 
                                     fg='white',
                                     font=("Segoe UI", 12, "bold"),
                                     padx=25, pady=12,
                                     relief='flat',
                                     cursor='hand2')
        self.start_button.pack(side='left', padx=8)
        
        self.stop_button = tk.Button(button_frame, 
                                    text="⏸️ Pausar", 
                                    command=self.stop_listening,
                                    bg='#f44336', 
                                    fg='white',
                                    font=("Segoe UI", 12, "bold"),
                                    padx=25, pady=12,
                                    relief='flat',
                                    cursor='hand2')
        self.stop_button.pack(side='left', padx=8)
        
        self.clear_button = tk.Button(button_frame, 
                                     text="🧹 Limpar", 
                                     command=self.clear_text,
                                     bg='#ff9800', 
                                     fg='white',
                                     font=("Segoe UI", 12, "bold"),
                                     padx=25, pady=12,
                                     relief='flat',
                                     cursor='hand2')
        self.clear_button.pack(side='left', padx=8)
        
        self.minimize_button = tk.Button(button_frame, 
                                        text="➖ Minimizar", 
                                        command=self.minimize_to_tray,
                                        bg='#9c27b0', 
                                        fg='white',
                                        font=("Segoe UI", 12, "bold"),
                                        padx=25, pady=12,
                                        relief='flat',
                                        cursor='hand2')
        self.minimize_button.pack(side='left', padx=8)
        
        # Área de texto para inglês
        english_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        english_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        english_label = tk.Label(english_frame, 
                                text="🇺🇸 INGLÊS (Original)", 
                                font=("Segoe UI", 16, "bold"),
                                bg='#2d2d2d', 
                                fg='#4CAF50')
        english_label.pack(pady=(10, 5))
        
        self.english_text = tk.Text(english_frame, 
                                   height=10, 
                                   font=("Segoe UI", 12),
                                   bg='#1e1e1e', 
                                   fg='#ffffff',
                                   wrap='word',
                                   padx=15, 
                                   pady=15)
        self.english_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar para inglês
        english_scrollbar = ttk.Scrollbar(english_frame, orient="vertical", command=self.english_text.yview)
        self.english_text.configure(yscrollcommand=english_scrollbar.set)
        
        # Área de texto para português
        portuguese_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        portuguese_frame.pack(fill='both', expand=True)
        
        portuguese_label = tk.Label(portuguese_frame, 
                                   text="🇧🇷 PORTUGUÊS (Tradução)", 
                                   font=("Segoe UI", 16, "bold"),
                                   bg='#2d2d2d', 
                                   fg='#2196F3')
        portuguese_label.pack(pady=(10, 5))
        
        self.portuguese_text = tk.Text(portuguese_frame, 
                                      height=10, 
                                      font=("Segoe UI", 12),
                                      bg='#1e1e1e', 
                                      fg='#ffffff',
                                      wrap='word',
                                      padx=15, 
                                      pady=15)
        self.portuguese_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar para português
        portuguese_scrollbar = ttk.Scrollbar(portuguese_frame, orient="vertical", command=self.portuguese_text.yview)
        self.portuguese_text.configure(yscrollcommand=portuguese_scrollbar.set)
        
        # Configurar fechar janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_audio(self):
        """Configura o sistema de áudio"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                print("Calibrando microfone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✓ Microfone calibrado")
        except Exception as e:
            print(f"Erro ao configurar microfone: {e}")
            messagebox.showerror("Erro", f"Erro ao configurar microfone: {e}")
        
    def setup_translation(self):
        """Configura o sistema de tradução"""
        try:
            self.translator = Translator()
            print("✓ Tradutor configurado")
        except Exception as e:
            print(f"Erro ao configurar tradutor: {e}")
            messagebox.showerror("Erro", f"Erro ao configurar tradutor: {e}")
        
    def setup_system_tray(self):
        """Configura ícone da bandeja do sistema"""
        try:
            # Criar ícone simples
            image = Image.new('RGB', (64, 64), color='green')
            
            menu = (
                item('Mostrar', self.show_window),
                item('Pausar/Retomar', self.toggle_listening),
                item('Sair', self.quit_application)
            )
            
            self.tray_icon = pystray.Icon("VoiceTalkAI", image, "Voice Talk AI", menu)
        except Exception as e:
            print(f"Erro ao configurar bandeja: {e}")
            
    def start_listening(self):
        """Inicia a captura de áudio"""
        if not self.is_listening:
            self.is_listening = True
            self.status_label.config(text="🔴 ESCUTANDO...", fg='#ff4444')
            self.start_button.config(text="🔄 Reiniciar")
            self.stop_button.config(text="⏸️ Pausar", bg='#f44336')
            
            # Iniciar threads
            self.audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
            self.audio_thread.start()
            
            self.process_thread = threading.Thread(target=self.process_audio_loop, daemon=True)
            self.process_thread.start()
            
            print("✓ Captura iniciada")
            
    def stop_listening(self):
        """Para a captura de áudio"""
        self.is_listening = False
        self.status_label.config(text="⏸️ PAUSADO", fg='#ffaa00')
        self.start_button.config(text="🔄 Reiniciar")
        self.stop_button.config(text="▶️ Retomar", bg='#4CAF50')
        print("⏸️ Captura pausada")
        
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
                    print("🎤 Escutando...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self.audio_queue.put(audio)
                    
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"Erro na captura: {e}")
                time.sleep(1)
                
    def process_audio_loop(self):
        """Loop de processamento de áudio"""
        while self.is_listening:
            try:
                audio = self.audio_queue.get(timeout=1)
                
                # Reconhecer fala
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    if text and len(text.strip()) > 0:
                        timestamp = time.strftime("%H:%M:%S")
                        formatted_text = f"[{timestamp}] {text}"
                        self.update_english_text(formatted_text)
                        print(f"Reconhecido: {text}")
                        
                        # Traduzir
                        try:
                            translation = self.translator.translate(text, src='en', dest='pt')
                            formatted_translation = f"[{timestamp}] {translation.text}"
                            self.update_portuguese_text(formatted_translation)
                            print(f"Traduzido: {translation.text}")
                        except Exception as e:
                            print(f"Erro na tradução: {e}")
                            
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Erro no serviço: {e}")
                    
            except queue.Empty:
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
        self.root.withdraw()
        self.is_minimized = True
        try:
            self.tray_icon.run_detached()
        except:
            pass
            
    def show_window(self):
        """Mostra a janela"""
        self.root.deiconify()
        self.root.lift()
        self.is_minimized = False
        
    def toggle_listening(self):
        """Alterna entre pausar e retomar"""
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
            
    def on_closing(self):
        """Evento de fechamento da janela"""
        self.minimize_to_tray()
        
    def quit_application(self):
        """Fecha a aplicação"""
        self.is_listening = False
        self.root.quit()
        
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nEncerrando aplicação...")
        finally:
            self.is_listening = False


if __name__ == "__main__":
    print("🎙️ Voice Talk AI - Versão Simplificada")
    print("Iniciando aplicação...")
    
    app = VoiceTalkAI()
    app.run()
