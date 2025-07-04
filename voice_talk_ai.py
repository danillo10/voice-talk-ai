import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import speech_recognition as sr
from googletrans import Translator
import pyaudio
import wave
import numpy as np
import queue
import json
import os
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import sys


class DualAudioCapture:
    """Classe para capturar áudio do microfone e do sistema simultaneamente"""
    
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1  # Mono para melhor processamento
        self.rate = 16000  # Taxa otimizada para reconhecimento de fala
        self.audio = pyaudio.PyAudio()
        
        # Streams separados
        self.mic_stream = None
        self.system_stream = None
        
        # Estado
        self.is_recording = False
        self.mic_enabled = True
        self.system_enabled = True
        
        # Buffers de áudio
        self.mic_buffer = []
        self.system_buffer = []
        
        # Configuração de reconhecimento aprimorada
        self.silence_threshold = 500  # Limiar de silêncio
        self.min_audio_length = 0.5   # Mínimo de 0.5 segundos de áudio
        
    def list_audio_devices(self):
        """Lista todos os dispositivos de áudio disponíveis"""
        print("=== DISPOSITIVOS DE ÁUDIO DISPONÍVEIS ===")
        devices = []
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            devices.append({
                'index': i,
                'name': info['name'],
                'channels': info['maxInputChannels'],
                'rate': info['defaultSampleRate']
            })
            print(f"[{i}] {info['name']} - Canais: {info['maxInputChannels']}")
        return devices
        
    def get_system_audio_device(self):
        """Encontra o dispositivo de áudio do sistema (Stereo Mix)"""
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            name = info["name"].lower()
            if any(keyword in name for keyword in ["stereo mix", "what u hear", "wave out mix", "sum"]):
                print(f"Dispositivo de sistema encontrado: {info['name']}")
                return i
        return None
        
    def get_microphone_device(self):
        """Encontra o dispositivo de microfone padrão"""
        try:
            # Usar dispositivo padrão do sistema
            default_device = self.audio.get_default_input_device_info()
            print(f"Microfone padrão: {default_device['name']}")
            return default_device['index']
        except:
            # Se não conseguir, usar o primeiro disponível
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    print(f"Usando microfone: {info['name']}")
                    return i
            return None
    
    def start_capture(self):
        """Inicia a captura de áudio do microfone e sistema"""
        success = False
        
        try:
            # Captura do microfone
            mic_device = self.get_microphone_device()
            if mic_device is not None and self.mic_enabled:
                try:
                    self.mic_stream = self.audio.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        input_device_index=mic_device
                    )
                    print("✓ Captura de microfone iniciada")
                    success = True
                except Exception as e:
                    print(f"⚠️ Erro no microfone: {e}")
                    self.mic_enabled = False
            
            # Captura do sistema
            system_device = self.get_system_audio_device()
            if system_device is not None and self.system_enabled:
                try:
                    self.system_stream = self.audio.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        input_device_index=system_device
                    )
                    print("✓ Captura de sistema iniciada")
                    success = True
                except Exception as e:
                    print(f"⚠️ Erro no áudio do sistema: {e}")
                    self.system_enabled = False
            
            if success:
                self.is_recording = True
                print("✓ Captura dual iniciada com sucesso!")
            else:
                print("⚠️ Nenhum dispositivo de áudio pôde ser inicializado")
                
        except Exception as e:
            print(f"Erro geral na captura: {e}")
            
        return success
    
    def read_audio(self):
        """Lê dados de áudio de ambas as fontes"""
        audio_data = []
        
        # Ler do microfone
        if self.mic_stream and self.mic_enabled:
            try:
                mic_data = self.mic_stream.read(self.chunk, exception_on_overflow=False)
                audio_data.append(('mic', mic_data))
            except Exception as e:
                print(f"Erro ao ler microfone: {e}")
                
        # Ler do sistema
        if self.system_stream and self.system_enabled:
            try:
                system_data = self.system_stream.read(self.chunk, exception_on_overflow=False)
                audio_data.append(('system', system_data))
            except Exception as e:
                print(f"Erro ao ler sistema: {e}")
                
        return audio_data
    
    def stop_capture(self):
        """Para a captura de áudio"""
        self.is_recording = False
        
        if self.mic_stream:
            try:
                self.mic_stream.stop_stream()
                self.mic_stream.close()
                self.mic_stream = None
                print("✓ Captura de microfone parada")
            except:
                pass
                
        if self.system_stream:
            try:
                self.system_stream.stop_stream()
                self.system_stream.close()
                self.system_stream = None
                print("✓ Captura de sistema parada")
            except:
                pass
    
    def __del__(self):
        """Destructor"""
        self.stop_capture()
        if self.audio:
            self.audio.terminate()


class SystemAudioCapture:
    """Mantido para compatibilidade - agora usa DualAudioCapture"""
    
    def __init__(self):
        self.dual_capture = DualAudioCapture()
        
    def start_capture(self):
        return self.dual_capture.start_capture()
        
    def read_audio(self):
        return self.dual_capture.read_audio()
        
    def stop_capture(self):
        return self.dual_capture.stop_capture()
        
    @property
    def is_recording(self):
        return self.dual_capture.is_recording


class VoiceTalkAI:
    def __init__(self):
        self.root = tk.Tk()
        
        # Inicializar sistema de áudio primeiro
        self.system_audio = SystemAudioCapture()
        self.dual_capture = self.system_audio.dual_capture  # Acesso direto ao dual capture
        
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
        
        # Sistema de auto-restart
        self.restart_attempts = 0
        self.max_restart_attempts = 3
        
        # Iniciar automaticamente
        self.auto_start_delay = 2000  # 2 segundos
        self.root.after(self.auto_start_delay, self.auto_start)
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        self.root.title("Voice Talk AI - Tradutor Automático")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # Configurar para ficar sempre no topo
        self.root.attributes('-topmost', True)
        
        # Minimizar para bandeja ao iniciar (opcional)
        # self.root.withdraw()
        
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
        
        # Status e controles
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        control_frame.pack(fill='x', pady=(0, 15))
        
        # Status
        status_frame = tk.Frame(control_frame, bg='#2d2d2d')
        status_frame.pack(pady=10)
        
        self.status_label = tk.Label(status_frame, 
                                    text="� Iniciando automaticamente...", 
                                    font=("Segoe UI", 14, "bold"),
                                    bg='#2d2d2d', 
                                    fg='#ffaa00')
        self.status_label.pack()
        
        # Botões de controle
        button_frame = tk.Frame(control_frame, bg='#2d2d2d')
        button_frame.pack(pady=15)
        
        self.start_button = tk.Button(button_frame, 
                                     text="🔄 Reiniciar Captura", 
                                     command=self.restart_listening,
                                     bg='#4CAF50', 
                                     fg='white',
                                     font=("Segoe UI", 12, "bold"),
                                     padx=25, 
                                     pady=12,
                                     relief='flat',
                                     cursor='hand2')
        self.start_button.pack(side='left', padx=8)
        
        self.stop_button = tk.Button(button_frame, 
                                    text="⏸️ Pausar", 
                                    command=self.pause_listening,
                                    bg='#ff9800', 
                                    fg='white',
                                    font=("Segoe UI", 12, "bold"),
                                    padx=25, 
                                    pady=12,
                                    relief='flat',
                                    cursor='hand2')
        self.stop_button.pack(side='left', padx=8)
        
        # Controles de fonte de áudio
        audio_control_frame = tk.Frame(button_frame, bg='#2d2d2d')
        audio_control_frame.pack(side='left', padx=20)
        
        self.mic_button = tk.Button(audio_control_frame, 
                                   text="🎤 Mic ON", 
                                   command=self.toggle_microphone,
                                   bg='#00ff88', 
                                   fg='white',
                                   font=("Segoe UI", 10, "bold"),
                                   padx=15, 
                                   pady=8,
                                   relief='flat',
                                   cursor='hand2')
        self.mic_button.pack(side='top', pady=2)
        
        self.system_button = tk.Button(audio_control_frame, 
                                      text="🔊 Sys ON", 
                                      command=self.toggle_system_audio,
                                      bg='#00ff88', 
                                      fg='white',
                                      font=("Segoe UI", 10, "bold"),
                                      padx=15, 
                                      pady=8,
                                      relief='flat',
                                      cursor='hand2')
        self.system_button.pack(side='top', pady=2)
        
        self.clear_button = tk.Button(button_frame, 
                                     text="🗑️ Limpar", 
                                     command=self.clear_text,
                                     bg='#f44336', 
                                     fg='white',
                                     font=("Segoe UI", 12, "bold"),
                                     padx=25, 
                                     pady=12,
                                     relief='flat',
                                     cursor='hand2')
        self.clear_button.pack(side='left', padx=8)
        
        self.devices_button = tk.Button(button_frame, 
                                       text="🎛️ Dispositivos", 
                                       command=self.show_audio_devices,
                                       bg='#9c27b0', 
                                       fg='white',
                                       font=("Segoe UI", 12, "bold"),
                                       padx=25, 
                                       pady=12,
                                       relief='flat',
                                       cursor='hand2')
        self.devices_button.pack(side='left', padx=8)
        
        self.minimize_button = tk.Button(button_frame, 
                                        text="⬇️ Minimizar", 
                                        command=self.minimize_to_tray,
                                        bg='#2196F3', 
                                        fg='white',
                                        font=("Segoe UI", 12, "bold"),
                                        padx=25, 
                                        pady=12,
                                        relief='flat',
                                        cursor='hand2')
        self.minimize_button.pack(side='left', padx=8)
        
        # Área de legendas
        subtitle_frame = tk.Frame(main_frame, bg='#1e1e1e')
        subtitle_frame.pack(fill='both', expand=True)
        
        # Legenda em inglês
        english_frame = tk.Frame(subtitle_frame, bg='#2d2d2d', relief='raised', bd=2)
        english_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        english_label = tk.Label(english_frame, 
                                text="🇺🇸 Original (Inglês)", 
                                font=("Segoe UI", 14, "bold"),
                                bg='#2d2d2d', 
                                fg='#ffffff')
        english_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Scrollbar para texto inglês
        english_scroll_frame = tk.Frame(english_frame, bg='#2d2d2d')
        english_scroll_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        english_scrollbar = tk.Scrollbar(english_scroll_frame)
        english_scrollbar.pack(side='right', fill='y')
        
        self.english_text = tk.Text(english_scroll_frame, 
                                   height=10, 
                                   bg='#1a1a1a', 
                                   fg='#ffffff',
                                   font=("Consolas", 11),
                                   wrap='word',
                                   relief='flat',
                                   yscrollcommand=english_scrollbar.set)
        self.english_text.pack(side='left', fill='both', expand=True)
        english_scrollbar.config(command=self.english_text.yview)
        
        # Legenda em português
        portuguese_frame = tk.Frame(subtitle_frame, bg='#2d2d2d', relief='raised', bd=2)
        portuguese_frame.pack(fill='both', expand=True)
        
        portuguese_label = tk.Label(portuguese_frame, 
                                   text="🇧🇷 Tradução (Português)", 
                                   font=("Segoe UI", 14, "bold"),
                                   bg='#2d2d2d', 
                                   fg='#ffffff')
        portuguese_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Scrollbar para texto português
        portuguese_scroll_frame = tk.Frame(portuguese_frame, bg='#2d2d2d')
        portuguese_scroll_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        portuguese_scrollbar = tk.Scrollbar(portuguese_scroll_frame)
        portuguese_scrollbar.pack(side='right', fill='y')
        
        self.portuguese_text = tk.Text(portuguese_scroll_frame, 
                                      height=10, 
                                      bg='#1a1a1a', 
                                      fg='#00ff88',
                                      font=("Consolas", 11),
                                      wrap='word',
                                      relief='flat',
                                      yscrollcommand=portuguese_scrollbar.set)
        self.portuguese_text.pack(side='left', fill='both', expand=True)
        portuguese_scrollbar.config(command=self.portuguese_text.yview)
        
        # Bind para minimizar ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Adicionar efeitos hover nos botões
        self.add_hover_effects()
        
        # Atualizar status dos botões de áudio
        self.update_audio_button_status()
        
    def add_hover_effects(self):
        """Adiciona efeitos de hover aos botões"""
        def on_enter(e, original_color):
            e.widget.config(bg=self.lighten_color(original_color))
        
        def on_leave(e, original_color):
            e.widget.config(bg=original_color)
        
        buttons = [
            (self.start_button, '#4CAF50'),
            (self.stop_button, '#ff9800'),
            (self.clear_button, '#f44336'),
            (self.devices_button, '#9c27b0'),
            (self.minimize_button, '#2196F3'),
            (self.mic_button, '#00ff88'),
            (self.system_button, '#00ff88')
        ]
        
        for button, color in buttons:
            button.bind("<Enter>", lambda e, c=color: on_enter(e, c))
            button.bind("<Leave>", lambda e, c=color: on_leave(e, c))
    
    def lighten_color(self, color):
        """Clareia uma cor hexadecimal"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, c + 30) for c in rgb)
        return '#%02x%02x%02x' % rgb
        
    def setup_audio(self):
        """Configura o sistema de áudio"""
        # Configurar reconhecedor de voz com parâmetros otimizados
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Ajustar sensibilidade
        self.recognizer.dynamic_energy_threshold = True  # Ajuste automático
        self.recognizer.pause_threshold = 0.8  # Pausa entre palavras
        self.recognizer.phrase_threshold = 0.3  # Mínimo para considerar fala
        self.recognizer.non_speaking_duration = 0.5  # Duração de não-fala
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        self.recognizer.dynamic_energy_threshold = True
        
    def setup_translation(self):
        """Configura o tradutor"""
        self.translator = Translator()
        
    def setup_system_tray(self):
        """Configura o ícone da bandeja do sistema"""
        # Criar um ícone simples
        image = Image.new('RGB', (64, 64), color='#00d4ff')
        
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
            "language_to": "pt",
            "audio_threshold": 300
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
            self.status_label.config(text="🟢 ATIVO - Capturando áudio...", fg='#00ff88')
            self.start_button.config(text="🔄 Reiniciar Captura")
            self.stop_button.config(text="⏸️ Pausar", bg='#ff9800')
            
            # Iniciar captura de áudio do sistema
            if self.system_audio.start_capture():
                # Iniciar thread de captura de áudio
                self.audio_thread = threading.Thread(target=self.audio_capture_loop)
                self.audio_thread.daemon = True
                self.audio_thread.start()
                
                # Iniciar thread de processamento
                self.process_thread = threading.Thread(target=self.process_audio_loop)
                self.process_thread.daemon = True
                self.process_thread.start()
                
                # Iniciar thread de monitoramento
                self.monitor_thread = threading.Thread(target=self.monitor_system)
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                
            else:
                self.stop_listening()
                self.show_notification("Erro: Não foi possível iniciar captura de áudio")
                # Tentar auto-restart
                self.root.after(5000, self.auto_restart_on_error)
    
    def stop_listening(self):
        """Para a captura de áudio"""
        self.is_listening = False
        self.system_audio.stop_capture()
        self.status_label.config(text="⏸️ PAUSADO", fg='#ffaa00')
        self.start_button.config(text="🔄 Reiniciar Captura")
        self.stop_button.config(text="▶️ Retomar", bg='#4CAF50')
    
    def clear_text(self):
        """Limpa os textos das legendas"""
        self.english_text.delete(1.0, tk.END)
        self.portuguese_text.delete(1.0, tk.END)
    
    def audio_capture_loop(self):
        """Loop principal de captura de áudio - agora processa ambas as fontes"""
        audio_buffer = []
        buffer_size = 16000 * 3  # 3 segundos de áudio a 16kHz para melhor reconhecimento
        
        while self.is_listening:
            try:
                # Capturar áudio de ambas as fontes
                audio_sources = self.system_audio.read_audio()
                
                if audio_sources:
                    for source_type, audio_data in audio_sources:
                        if audio_data:
                            # Converter para numpy array
                            audio_np = np.frombuffer(audio_data, dtype=np.int16)
                            
                            # Verificar se há volume suficiente (não é silêncio)
                            try:
                                volume = np.sqrt(np.mean(audio_np.astype(np.float64)**2))
                                if volume > 100:  # Limiar de volume mínimo
                                    audio_buffer.extend(audio_np)
                            except:
                                # Se erro no cálculo, adicionar mesmo assim
                                audio_buffer.extend(audio_np)
                                
                                # Quando o buffer estiver cheio, processar
                                if len(audio_buffer) >= buffer_size:
                                    # Aplicar filtros para melhorar qualidade
                                    audio_array = np.array(audio_buffer[:buffer_size], dtype=np.int16)
                                    
                                    # Normalizar áudio
                                    audio_array = self.normalize_audio(audio_array)
                                    
                                    # Converter para formato do speech_recognition
                                    audio_bytes = audio_array.tobytes()
                                    
                                    # Criar objeto AudioData com taxa correta
                                    audio_data_obj = sr.AudioData(audio_bytes, 16000, 2)
                                    
                                    # Adicionar à fila com informação da fonte
                                    self.audio_queue.put((source_type, audio_data_obj))
                                    
                                    # Limpar buffer (mantém última metade para continuidade)
                                    audio_buffer = audio_buffer[buffer_size//2:]
                        
                time.sleep(0.01)  # Pequena pausa para não sobrecarregar
                
            except Exception as e:
                print(f"Erro na captura de áudio: {e}")
                time.sleep(0.1)
    
    def normalize_audio(self, audio_array):
        """Normaliza o áudio para melhor reconhecimento"""
        try:
            # Converter para float para processamento
            audio_float = audio_array.astype(np.float32)
            
            # Normalizar amplitude
            max_val = np.max(np.abs(audio_float))
            if max_val > 0:
                audio_float = audio_float / max_val * 32767.0
            
            # Converter de volta para int16
            return audio_float.astype(np.int16)
        except:
            return audio_array
    
    def process_audio_loop(self):
        """Loop de processamento de áudio - agora diferencia as fontes"""
        while self.is_listening:
            try:
                # Pegar áudio da fila
                source_type, audio = self.audio_queue.get(timeout=1)
                
                # Reconhecer fala com configurações melhoradas
                try:
                    # Primeiro, tentar com show_all para pegar a melhor alternativa
                    results = self.recognizer.recognize_google(
                        audio, 
                        language='en-US',
                        show_all=True
                    )
                    
                    text = None
                    if results and 'alternative' in results:
                        # Pegar a alternativa com maior confiança
                        alternatives = results['alternative']
                        if alternatives:
                            # Ordenar por confiança se disponível
                            if 'confidence' in alternatives[0]:
                                alternatives.sort(key=lambda x: x.get('confidence', 0), reverse=True)
                            text = alternatives[0]['transcript']
                    
                    # Se não funcionou com show_all, tentar método simples
                    if not text:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                    
                    # Filtrar textos muito curtos ou com pouca confiança
                    if text and len(text.strip()) > 2:
                        timestamp = time.strftime("%H:%M:%S")
                        
                        # Identificar fonte do áudio
                        source_icon = "🎤" if source_type == "mic" else "🔊"
                        source_name = "Microfone" if source_type == "mic" else "Sistema"
                        
                        formatted_text = f"[{timestamp}] {source_icon} {source_name}: {text}"
                        self.update_english_text(formatted_text)
                        
                        # Traduzir
                        try:
                            translation = self.translator.translate(text, src='en', dest='pt')
                            formatted_translation = f"[{timestamp}] {source_icon} {source_name}: {translation.text}"
                            self.update_portuguese_text(formatted_translation)
                        except Exception as e:
                            print(f"Erro na tradução: {e}")
                            error_msg = f"[{timestamp}] {source_icon} {source_name}: [Erro na tradução]"
                            self.update_portuguese_text(error_msg)
                            
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
        if len(lines) > 100:
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
        if len(lines) > 100:
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
        self.system_audio.stop_capture()
        self.save_settings()
        if self.is_minimized:
            self.icon.stop()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        try:
            # Iniciar sistema de keep-alive
            self.keep_alive()
            
            # Iniciar loop principal
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()
        except Exception as e:
            print(f"Erro na aplicação: {e}")
            # Tentar reiniciar
            self.auto_restart_on_error()
    
    def auto_start(self):
        """Inicia automaticamente a captura após carregar"""
        try:
            self.status_label.config(text="🔄 Iniciando automaticamente...", fg='#ffaa00')
            self.root.update()
            
            # Aguardar um pouco para interface carregar completamente
            time.sleep(0.5)
            
            # Iniciar captura automaticamente
            self.start_listening()
            
            # Mostrar notificação
            self.show_notification("Voice Talk AI iniciado automaticamente!")
            
        except Exception as e:
            print(f"Erro no auto-start: {e}")
            self.status_label.config(text="🔴 Erro no auto-start", fg='#ff4444')
    
    def show_notification(self, message):
        """Mostra notificação no sistema"""
        try:
            # Usar messagebox para notificação rápida
            self.root.after(100, lambda: self.update_status_with_fade(message))
        except Exception as e:
            print(f"Erro na notificação: {e}")
    
    def update_status_with_fade(self, message):
        """Atualiza status com efeito fade"""
        try:
            # Mostrar mensagem temporária
            original_text = self.status_label.cget("text")
            original_color = self.status_label.cget("fg")
            
            self.status_label.config(text=f"ℹ️ {message}", fg='#00ff88')
            
            # Voltar ao status original após 3 segundos
            self.root.after(3000, lambda: self.status_label.config(text=original_text, fg=original_color))
        except Exception as e:
            print(f"Erro no fade: {e}")
    
    def setup_auto_restart(self):
        """Configura reinício automático em caso de erro"""
        self.restart_attempts = 0
        self.max_restart_attempts = 3
        
    def auto_restart_on_error(self):
        """Reinicia automaticamente em caso de erro"""
        if self.restart_attempts < self.max_restart_attempts:
            self.restart_attempts += 1
            self.status_label.config(text=f"🔄 Reiniciando... ({self.restart_attempts}/{self.max_restart_attempts})", fg='#ffaa00')
            
            # Parar captura atual
            self.stop_listening()
            
            # Aguardar um pouco
            time.sleep(2)
            
            # Tentar reiniciar
            try:
                self.start_listening()
                self.restart_attempts = 0  # Reset contador se sucesso
            except Exception as e:
                print(f"Erro no auto-restart: {e}")
                if self.restart_attempts >= self.max_restart_attempts:
                    self.status_label.config(text="🔴 Falha crítica - Reinício manual necessário", fg='#ff4444')
                else:
                    # Tentar novamente em 5 segundos
                    self.root.after(5000, self.auto_restart_on_error)
        else:
            self.status_label.config(text="🔴 Máximo de tentativas atingido", fg='#ff4444')
    
    def restart_listening(self):
        """Reinicia a captura de áudio"""
        self.stop_listening()
        time.sleep(1)
        self.start_listening()
    
    def pause_listening(self):
        """Pausa/Resume a captura de áudio"""
        if self.is_listening:
            self.stop_listening()
            self.stop_button.config(text="▶️ Retomar", bg='#4CAF50')
        else:
            self.start_listening()
            self.stop_button.config(text="⏸️ Pausar", bg='#ff9800')
    
    def monitor_system(self):
        """Monitora o sistema para auto-restart em caso de problemas"""
        last_activity = time.time()
        error_count = 0
        
        while self.is_listening:
            try:
                # Verificar se há atividade recente
                current_time = time.time()
                
                # Se não há atividade há muito tempo, pode ter problema
                if current_time - last_activity > 60:  # 1 minuto
                    # Verificar se ainda está capturando
                    if self.system_audio.is_recording:
                        last_activity = current_time
                    else:
                        error_count += 1
                        if error_count >= 3:
                            print("Sistema detectou problema - tentando auto-restart")
                            self.root.after(0, self.auto_restart_on_error)
                            break
                
                # Aguardar antes da próxima verificação
                time.sleep(10)
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                error_count += 1
                if error_count >= 5:
                    break
                time.sleep(5)
    
    def keep_alive(self):
        """Mantém a aplicação sempre funcionando"""
        try:
            # Verifica se ainda está rodando
            if not self.is_listening and not self.is_minimized:
                # Se não está rodando e não está minimizado, algo deu errado
                print("Sistema detectou parada inesperada - reiniciando...")
                self.auto_restart_on_error()
        except Exception as e:
            print(f"Erro no keep_alive: {e}")
        
        # Reagendar verificação
        self.root.after(30000, self.keep_alive)  # A cada 30 segundos
    
    def toggle_microphone(self):
        """Liga/desliga captura do microfone"""
        self.dual_capture.mic_enabled = not self.dual_capture.mic_enabled
        if self.dual_capture.mic_enabled:
            self.mic_button.config(text="🎤 Mic ON", bg='#00ff88')
            self.show_notification("Microfone habilitado")
        else:
            self.mic_button.config(text="🎤 Mic OFF", bg='#666666')
            self.show_notification("Microfone desabilitado")
    
    def toggle_system_audio(self):
        """Liga/desliga captura do áudio do sistema"""
        self.dual_capture.system_enabled = not self.dual_capture.system_enabled
        if self.dual_capture.system_enabled:
            self.system_button.config(text="🔊 Sys ON", bg='#00ff88')
            self.show_notification("Áudio do sistema habilitado")
        else:
            self.system_button.config(text="🔊 Sys OFF", bg='#666666')
            self.show_notification("Áudio do sistema desabilitado")
    
    def show_audio_devices(self):
        """Mostra janela com dispositivos de áudio disponíveis"""
        devices_window = tk.Toplevel(self.root)
        devices_window.title("Dispositivos de Áudio")
        devices_window.geometry("600x400")
        devices_window.configure(bg='#1e1e1e')
        
        # Título
        title = tk.Label(devices_window, 
                        text="🎛️ Dispositivos de Áudio Disponíveis", 
                        font=("Segoe UI", 16, "bold"),
                        bg='#1e1e1e', 
                        fg='#ffffff')
        title.pack(pady=10)
        
        # Área de texto
        text_frame = tk.Frame(devices_window, bg='#1e1e1e')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_area = tk.Text(text_frame, 
                           bg='#2d2d2d', 
                           fg='#ffffff',
                           font=("Consolas", 10),
                           yscrollcommand=scrollbar.set)
        text_area.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_area.yview)
        
        # Listar dispositivos
        try:
            devices = self.dual_capture.list_audio_devices()
            
            text_area.insert(tk.END, "=== DISPOSITIVOS DE ENTRADA ===\n\n")
            
            for device in devices:
                if device['channels'] > 0:
                    text_area.insert(tk.END, f"[{device['index']:2d}] {device['name']}\n")
                    text_area.insert(tk.END, f"     Canais: {device['channels']}\n")
                    text_area.insert(tk.END, f"     Taxa: {device['rate']} Hz\n\n")
            
            # Mostrar configuração atual
            text_area.insert(tk.END, "\n=== CONFIGURAÇÃO ATUAL ===\n\n")
            text_area.insert(tk.END, f"Microfone: {'ON' if self.dual_capture.mic_enabled else 'OFF'}\n")
            text_area.insert(tk.END, f"Sistema: {'ON' if self.dual_capture.system_enabled else 'OFF'}\n")
            text_area.insert(tk.END, f"Status: {'Gravando' if self.dual_capture.is_recording else 'Parado'}\n")
            
        except Exception as e:
            text_area.insert(tk.END, f"Erro ao listar dispositivos: {e}")
    
    def update_audio_button_status(self):
        """Atualiza o status visual dos botões de áudio"""
        # Botão do microfone
        if self.dual_capture.mic_enabled:
            self.mic_button.config(text="🎤 Mic ON", bg='#00ff88')
        else:
            self.mic_button.config(text="🎤 Mic OFF", bg='#666666')
            
        # Botão do sistema
        if self.dual_capture.system_enabled:
            self.system_button.config(text="🔊 Sys ON", bg='#00ff88')
        else:
            self.system_button.config(text="🔊 Sys OFF", bg='#666666')
    
if __name__ == "__main__":
    # Verificar se as dependências estão instaladas
    try:
        import speech_recognition
        import googletrans
        import pyaudio
        import numpy
        import pystray
        from PIL import Image
    except ImportError as e:
        print(f"Dependência não encontrada: {e}")
        print("Instale as dependências executando: pip install -r requirements.txt")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Verificar se está sendo executado como administrador (necessário para captura de áudio do sistema)
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("AVISO: Execute o programa como administrador para melhor captura de áudio do sistema.")
    except:
        pass
    
    app = VoiceTalkAI()
    app.run()
