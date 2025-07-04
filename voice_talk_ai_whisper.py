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
import whisper
import numpy as np
import io
import wave
import tempfile


class VoiceTalkAI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.setup_audio()
        self.setup_translation()
        self.setup_whisper()
        self.setup_openai()
        self.setup_system_tray()
        
        # Controle de estado
        self.is_listening = False
        self.is_minimized = False
        self.audio_queue = queue.Queue()
        self.translation_queue = queue.Queue()
        
        # Iniciar automaticamente após 3 segundos (tempo para carregar Whisper)
        self.root.after(3000, self.start_listening)
        
    def setup_ui(self):
        """Configura a interface do usuário - Lateral esquerda 15% da tela"""
        self.root.title("Voice Talk AI - Whisper")
        
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
                                    text="🔄 Carregando Whisper...", 
                                    font=("Segoe UI", 8),
                                    bg='#2d2d2d', 
                                    fg='#ffaa00')
        self.status_label.pack(pady=(0, 5))
        
        # Modelo AI
        self.model_label = tk.Label(header_frame, 
                                   text="🤖 Whisper AI", 
                                   font=("Segoe UI", 7),
                                   bg='#2d2d2d', 
                                   fg='#00aaff')
        self.model_label.pack(pady=(0, 5))
        
        # Botões compactos
        button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        button_frame.pack(fill='x', pady=5)
        
        # Seletor de modelo
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(button_frame, 
                                  textvariable=self.model_var,
                                  values=["tiny", "base", "small", "medium"],
                                  state="readonly",
                                  font=("Segoe UI", 7),
                                  width=8)
        model_combo.pack(side='left', padx=2)
        model_combo.bind('<<ComboboxSelected>>', self.change_model)
        
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
                           text="EN (Whisper):", 
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
                           text="PT (Tradução):", 
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
        """Configura o sistema de áudio com filtros aprimorados"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configurações equilibradas - detectar fala mas evitar ruído
        self.recognizer.energy_threshold = 1500  # Meio termo
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0  # Pausa média
        self.recognizer.phrase_threshold = 0.5  # Threshold médio
        self.recognizer.non_speaking_duration = 0.8  # Duração média
        
        # Ajustar para ruído ambiente na inicialização
        print("🎤 Calibrando microfone para ruído ambiente...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"✓ Energy threshold: {self.recognizer.energy_threshold}")
        
    def setup_translation(self):
        """Configura o tradutor"""
        self.translator = Translator()
        
    def setup_whisper(self):
        """Configura o modelo Whisper"""
        def load_whisper():
            try:
                self.status_label.config(text="🔄 Carregando Whisper...")
                
                # Suprimir warnings do Whisper
                import warnings
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
                
                # Carregar modelo com configurações otimizadas para CPU
                self.whisper_model = whisper.load_model("base", device="cpu")
                self.status_label.config(text="✅ Whisper carregado!", fg='#00ff88')
                print("✓ Whisper model loaded successfully")
            except Exception as e:
                print(f"❌ Erro ao carregar Whisper: {e}")
                self.whisper_model = None
                self.status_label.config(text="❌ Erro no Whisper", fg='#ff6b6b')
        
        # Carregar em thread separada
        threading.Thread(target=load_whisper, daemon=True).start()
        
    def change_model(self, event=None):
        """Muda o modelo Whisper"""
        if hasattr(self, 'whisper_model'):
            def reload_model():
                try:
                    model_name = self.model_var.get()
                    self.status_label.config(text=f"🔄 Carregando {model_name}...")
                    
                    # Suprimir warnings
                    import warnings
                    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
                    
                    # Carregar modelo otimizado para CPU
                    self.whisper_model = whisper.load_model(model_name, device="cpu")
                    self.status_label.config(text=f"✅ {model_name} carregado!", fg='#00ff88')
                    print(f"✓ Whisper model changed to {model_name}")
                except Exception as e:
                    print(f"❌ Erro ao trocar modelo: {e}")
                    self.status_label.config(text="❌ Erro no modelo", fg='#ff6b6b')
            
            threading.Thread(target=reload_model, daemon=True).start()
        
    def setup_openai(self):
        """Configura correção de texto local"""
        try:
            print("🤖 Sistema de correção de texto configurado")
        except Exception as e:
            print(f"❌ Erro ao configurar correção: {e}")
    
    def correct_text_with_ai(self, text):
        """Corrige texto usando IA local (sem API externa)"""
        try:
            # Correções básicas locais
            corrected = text.strip()
            
            # Capitalizar primeira letra
            if corrected:
                corrected = corrected[0].upper() + corrected[1:]
            
            # Correções comuns de transcrição
            corrections = {
                'i m': "I'm",
                'i ll': "I'll",
                'i d': "I'd",
                'i ve': "I've",
                'cant': "can't",
                'wont': "won't",
                'dont': "don't",
                'isnt': "isn't",
                'wasnt': "wasn't",
                'werent': "weren't",
                'shouldnt': "shouldn't",
                'wouldnt': "wouldn't",
                'couldnt': "couldn't",
                'u': 'you',
                'ur': 'your',
                'r': 'are',
                'thats': "that's",
                'whats': "what's",
                'hows': "how's",
                'wheres': "where's",
                'theres': "there's",
                'theyre': "they're"
            }
            
            words = corrected.split()
            corrected_words = []
            
            for i, word in enumerate(words):
                word_lower = word.lower()
                if word_lower in corrections:
                    corrected_words.append(corrections[word_lower])
                else:
                    corrected_words.append(word)
            
            corrected = ' '.join(corrected_words)
            
            # Adicionar ponto final se não tiver pontuação
            if corrected and corrected[-1] not in '.!?':
                corrected += '.'
            
            return corrected
            
        except Exception as e:
            print(f"Erro na correção: {e}")
            return text

    def setup_system_tray(self):
        """Configura a bandeja do sistema"""
        try:
            image = Image.new('RGB', (64, 64), color=(0, 255, 136))
            menu = pystray.Menu(
                item('Mostrar', self.show_window),
                item('Ocultar', self.hide_window),
                item('Sair', self.quit_application)
            )
            self.icon = pystray.Icon("VoiceTalkAI", image, "Voice Talk AI Whisper", menu)
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
            
            print("✓ Captura de áudio iniciada com Whisper")
            
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
        """Loop de captura de áudio com filtro de silêncio"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Ajustar para ruído ambiente periodicamente
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Capturar áudio com timeout maior
                    audio = self.recognizer.listen(
                        source, 
                        timeout=2,  # Timeout maior
                        phrase_time_limit=6  # Limite de frase maior
                    )
                    
                    # Verificar se o áudio tem volume suficiente
                    audio_data = audio.get_wav_data()
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    volume = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
                    
                    # Só processar se tiver volume significativo
                    if volume > 400:  # Limiar médio para equilibrar
                        self.audio_queue.put(audio)
                    
            except sr.WaitTimeoutError:
                # Timeout normal, continuar
                pass
            except Exception as e:
                print(f"Erro na captura: {e}")
                time.sleep(0.1)
                
    def process_audio_loop(self):
        """Loop de processamento de áudio com Whisper"""
        while self.is_listening:
            try:
                # Pegar áudio da fila
                audio = self.audio_queue.get(timeout=1)
                
                # Processar com Whisper se disponível
                if hasattr(self, 'whisper_model') and self.whisper_model:
                    try:
                        text = self.transcribe_with_whisper(audio)
                    except Exception as e:
                        print(f"Erro Whisper: {e}")
                        # Fallback para Google
                        text = self.transcribe_with_google(audio)
                else:
                    # Usar Google se Whisper não estiver disponível
                    text = self.transcribe_with_google(audio)
                
                if text and len(text.strip()) > 0:
                    # Aplicar correção de texto com IA
                    corrected_text = self.correct_text_with_ai(text)
                    
                    timestamp = time.strftime("%H:%M:%S")
                    formatted_text = f"[{timestamp}] {corrected_text}"
                    self.update_english_text(formatted_text)
                    
                    # Traduzir o texto corrigido
                    try:
                        translation = self.translator.translate(corrected_text, src='en', dest='pt')
                        formatted_translation = f"[{timestamp}] {translation.text}"
                        self.update_portuguese_text(formatted_translation)
                    except Exception as e:
                        print(f"Erro na tradução: {e}")
                        
            except queue.Empty:
                # Fila vazia, continuar
                pass
            except Exception as e:
                print(f"Erro no processamento: {e}")
                
    def transcribe_with_whisper(self, audio):
        """Transcreve áudio usando Whisper com filtros"""
        try:
            # Suprimir warnings
            import warnings
            warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
            
            # Converter AudioData para formato que Whisper aceita
            audio_data = audio.get_wav_data()
            
            # Verificar se o áudio não é muito curto
            if len(audio_data) < 8000:  # Menos de 0.5 segundos
                return None
            
            # Salvar temporariamente
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name
            
            # Transcrever com Whisper (configurações equilibradas)
            result = self.whisper_model.transcribe(
                tmp_file_path, 
                language='en',
                fp16=False,
                verbose=False,
                temperature=0.0,  # Reduz alucinações
                compression_ratio_threshold=2.3,  # Meio termo
                logprob_threshold=-0.9,  # Meio termo
                no_speech_threshold=0.7  # Meio termo
            )
            
            # Remover arquivo temporário
            os.unlink(tmp_file_path)
            
            text = result['text'].strip()
            
            # Filtrar textos muito curtos ou suspeitos
            if len(text) < 3 or text.lower() in ['', 'you', 'um', 'uh']:
                return None
                
            # Verificar se contém pelo menos uma palavra real
            words = text.split()
            if not words or len(words) < 2:
                return None
                
            return text
            
        except Exception as e:
            print(f"Erro Whisper: {e}")
            raise
            
    def transcribe_with_google(self, audio):
        """Transcreve áudio usando Google (fallback)"""
        try:
            return self.recognizer.recognize_google(audio, language='en-US')
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Erro Google: {e}")
            return None
                
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
    print("🚀 Iniciando Voice Talk AI com Whisper...")
    print("📥 Carregando modelo de IA...")
    app = VoiceTalkAI()
    app.run()


if __name__ == "__main__":
    main()
