import os
import sys
import subprocess
import time
import threading
from pathlib import Path

class VoiceTaskManager:
    def __init__(self):
        self.process = None
        self.is_running = False
        self.restart_count = 0
        self.max_restarts = 10
        
    def start_voice_app(self):
        """Inicia a aplicação Voice Talk AI"""
        try:
            script_dir = Path(__file__).parent
            voice_script = script_dir / "voice_talk_ai.py"
            
            if not voice_script.exists():
                print(f"Erro: {voice_script} não encontrado")
                return False
            
            print("Iniciando Voice Talk AI...")
            self.process = subprocess.Popen([
                sys.executable, str(voice_script)
            ], cwd=str(script_dir))
            
            self.is_running = True
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar aplicação: {e}")
            return False
    
    def monitor_process(self):
        """Monitora o processo e reinicia se necessário"""
        while self.restart_count < self.max_restarts:
            try:
                if self.process and self.is_running:
                    # Verificar se o processo ainda está rodando
                    if self.process.poll() is not None:
                        print(f"Processo parou (código: {self.process.returncode})")
                        self.is_running = False
                        
                        # Aguardar antes de reiniciar
                        print("Aguardando 5 segundos antes de reiniciar...")
                        time.sleep(5)
                        
                        # Reiniciar
                        if self.restart_count < self.max_restarts:
                            self.restart_count += 1
                            print(f"Reiniciando... (tentativa {self.restart_count}/{self.max_restarts})")
                            
                            if self.start_voice_app():
                                print("Aplicação reiniciada com sucesso!")
                            else:
                                print("Falha ao reiniciar aplicação")
                                break
                        else:
                            print("Máximo de reinicializações atingido")
                            break
                
                # Aguardar antes da próxima verificação
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\nParando gerenciador...")
                self.stop()
                break
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                time.sleep(5)
    
    def stop(self):
        """Para a aplicação"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
        self.is_running = False
    
    def run(self):
        """Executa o gerenciador"""
        print("=== Voice Talk AI - Gerenciador Sempre Ativo ===")
        print("Pressione Ctrl+C para parar")
        print()
        
        # Iniciar aplicação
        if self.start_voice_app():
            print("Aplicação iniciada com sucesso!")
            print("Monitorando processo...")
            
            # Iniciar monitoramento
            monitor_thread = threading.Thread(target=self.monitor_process)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            try:
                # Manter o gerenciador rodando
                while self.is_running or self.restart_count < self.max_restarts:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nParando...")
            finally:
                self.stop()
        else:
            print("Falha ao iniciar aplicação")

if __name__ == "__main__":
    manager = VoiceTaskManager()
    try:
        manager.run()
    except Exception as e:
        print(f"Erro crítico: {e}")
    finally:
        print("Gerenciador finalizado")
        input("Pressione Enter para sair...")
