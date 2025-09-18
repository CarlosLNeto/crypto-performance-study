#!/usr/bin/env python3
"""
Script para executar o Chat Web com Assinatura Digital
"""

import sys
import os

# Adicionar path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("="*60)
    print("CHAT WEB COM ASSINATURA DIGITAL - ATIVIDADE 2")
    print("="*60)
    print()
    print("🔐 Sistema de Chat Seguro com:")
    print("   • Autenticação de usuários")
    print("   • Certificados X.509 ad-hoc")
    print("   • Assinatura digital RSA-PSS + SHA-256")
    print("   • Verificação de integridade em tempo real")
    print()
    print("👥 Usuários disponíveis:")
    print("   • carlos / 123456 (Carlos Lavor Neto)")
    print("   • eric / 123456 (Eric Dias Perin)")
    print("   • alexandro / 123456 (Alexandro Pantoja)")
    print()
    print("🌐 Acesse: http://localhost:8080")
    print("="*60)
    print()
    
    try:
        # Importar e executar a aplicação Flask
        from atividade2.src.chat_app import app
        app.run(debug=True, host='0.0.0.0', port=8080)
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

if __name__ == "__main__":
    main()
