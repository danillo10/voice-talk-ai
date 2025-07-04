import winreg
import os
import sys
from pathlib import Path

def add_to_startup():
    """Adiciona o Voice Talk AI na inicialização do Windows"""
    try:
        # Caminho para o arquivo bat
        script_dir = Path(__file__).parent
        bat_file = script_dir / "run_always_active.bat"
        
        if not bat_file.exists():
            print("Erro: run_always_active.bat não encontrado")
            return False
        
        # Chave do registro para inicialização
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        
        # Abrir chave do registro
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            # Adicionar entrada
            winreg.SetValueEx(key, "VoiceTalkAI", 0, winreg.REG_SZ, str(bat_file))
        
        print("✓ Voice Talk AI adicionado à inicialização do Windows")
        print(f"Arquivo: {bat_file}")
        return True
        
    except Exception as e:
        print(f"Erro ao adicionar à inicialização: {e}")
        return False

def remove_from_startup():
    """Remove o Voice Talk AI da inicialização do Windows"""
    try:
        # Chave do registro para inicialização
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        
        # Abrir chave do registro
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            # Remover entrada
            winreg.DeleteValue(key, "VoiceTalkAI")
        
        print("✓ Voice Talk AI removido da inicialização do Windows")
        return True
        
    except FileNotFoundError:
        print("Voice Talk AI não estava na inicialização")
        return True
    except Exception as e:
        print(f"Erro ao remover da inicialização: {e}")
        return False

def check_startup_status():
    """Verifica se o Voice Talk AI está na inicialização"""
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "VoiceTalkAI")
            print(f"✓ Voice Talk AI está na inicialização: {value}")
            return True
            
    except FileNotFoundError:
        print("Voice Talk AI não está na inicialização")
        return False
    except Exception as e:
        print(f"Erro ao verificar inicialização: {e}")
        return False

def main():
    print("=== Voice Talk AI - Configurador de Inicialização ===")
    print()
    
    # Verificar status atual
    is_in_startup = check_startup_status()
    print()
    
    print("Escolha uma opção:")
    print("1. Adicionar à inicialização do Windows")
    print("2. Remover da inicialização do Windows")
    print("3. Verificar status atual")
    print("4. Sair")
    print()
    
    choice = input("Digite sua escolha (1-4): ").strip()
    
    if choice == "1":
        if add_to_startup():
            print("\n✓ Configuração concluída!")
            print("O Voice Talk AI agora iniciará automaticamente com o Windows.")
        else:
            print("\n✗ Falha na configuração")
    
    elif choice == "2":
        if remove_from_startup():
            print("\n✓ Remoção concluída!")
            print("O Voice Talk AI não iniciará mais automaticamente.")
        else:
            print("\n✗ Falha na remoção")
    
    elif choice == "3":
        print("\n=== Status Atual ===")
        check_startup_status()
    
    elif choice == "4":
        print("Saindo...")
        return
    
    else:
        print("Opção inválida")
    
    print()
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
