#!/usr/bin/env python3
"""
Script para executar o Chat Web com Assinatura Digital
"""

import sys
import os

# Garantir que estamos no diretório correto
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

sys.path.append(os.path.join(script_dir, 'src'))

# Criar diretórios necessários no diretório da atividade2
os.makedirs('certificates', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('results', exist_ok=True)

from chat_app import app, socketio

if __name__ == '__main__':
    print("🔐 Chat Seguro com Assinatura Digital e WebSocket")
    print("=" * 60)
    print("🚀 Funcionalidades:")
    print("   • Comunicação em tempo real via WebSocket")
    print("   • Assinatura digital automática (RSA-PSS + SHA-256)")
    print("   • Verificação de integridade em tempo real")
    print("   • Certificados X.509 gerados automaticamente")
    print("   • Interface responsiva e moderna")
    print("   • Estatísticas de uso em tempo real")
    print()
    print("👥 Usuários disponíveis:")
    print("   • carlos / 123456 (Carlos Lavor Neto)")
    print("   • eric / 123456 (Eric Dias Perin)")
    print("   • alexandro / 123456 (Alexandro Pantoja)")
    print()
    print("🌐 Acesse: http://localhost:8081")
    print("=" * 60)
    
    try:
        socketio.run(app, host='0.0.0.0', port=8081, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n👋 Chat encerrado pelo usuário")
        # Salvar métricas finais
        from chat_app import save_metrics_to_file
        save_metrics_to_file()
        print("📊 Métricas do chat salvas em data/real_chat_metrics.csv")
        print("\n👋 Chat encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar o chat: {e}")
        print("💡 Certifique-se de que as dependências estão instaladas:")
        print("   pip install flask flask-socketio cryptography")
