#!/usr/bin/env python3
"""
Chat Web com Assinatura Digital
Frontend para demonstração da aplicação de assinatura digital
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime
import sys

# Adicionar path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from digital_signature_app import DigitalSignatureApp

app = Flask(__name__)
app.secret_key = 'crypto_chat_secret_key_2025'

# Instância global da aplicação de assinatura
signature_app = DigitalSignatureApp()

# Banco de dados simples em memória
users_db = {
    'carlos': {
        'password': generate_password_hash('123456'),
        'name': 'Carlos Lavor Neto',
        'email': 'carlos.neto@uea.edu.br',
        'cert_id': None
    },
    'eric': {
        'password': generate_password_hash('123456'),
        'name': 'Eric Dias Perin',
        'email': 'eric.perin@uea.edu.br',
        'cert_id': None
    },
    'alexandro': {
        'password': generate_password_hash('123456'),
        'name': 'Alexandro Pantoja',
        'email': 'alexandro.pantoja@uea.edu.br',
        'cert_id': None
    }
}

# Armazenamento de mensagens
messages_store = []

@app.route('/')
def index():
    """Página inicial - redireciona para login se não autenticado"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db and check_password_hash(users_db[username]['password'], password):
            session['username'] = username
            
            # Gerar certificado se não existir
            if users_db[username]['cert_id'] is None:
                user_info = signature_app.create_user(
                    users_db[username]['name'],
                    users_db[username]['email']
                )
                users_db[username]['cert_id'] = user_info['cert_id']
            
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Usuário ou senha inválidos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/send_message', methods=['POST'])
def send_message():
    """Enviar mensagem assinada"""
    if 'username' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    data = request.get_json()
    message_text = data.get('message', '').strip()
    recipient = data.get('recipient', '').strip()
    
    if not message_text:
        return jsonify({'error': 'Mensagem não pode estar vazia'}), 400
    
    if not recipient or recipient not in users_db:
        return jsonify({'error': 'Destinatário inválido'}), 400
    
    username = session['username']
    sender_cert_id = users_db[username]['cert_id']
    recipient_email = users_db[recipient]['email']
    
    try:
        # Assinar mensagem
        signed_message = signature_app.send_message(
            sender_cert_id,
            recipient_email,
            message_text
        )
        
        # Adicionar informações extras para o chat
        chat_message = {
            'id': len(messages_store) + 1,
            'sender': username,
            'sender_name': users_db[username]['name'],
            'recipient': recipient,
            'recipient_name': users_db[recipient]['name'],
            'message': message_text,
            'timestamp': signed_message['timestamp'],
            'signature': signed_message['signature'][:50] + '...',  # Truncar para exibição
            'signed_message': signed_message,
            'verified': None  # Será verificado quando solicitado
        }
        
        messages_store.append(chat_message)
        
        # Salvar mensagem em arquivo
        filename = f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{username}_to_{recipient}.json"
        signature_app.save_message_to_file(signed_message, filename)
        
        return jsonify({
            'success': True,
            'message_id': chat_message['id'],
            'timestamp': chat_message['timestamp']
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao enviar mensagem: {str(e)}'}), 500

@app.route('/get_messages')
def get_messages():
    """Obter mensagens do chat"""
    if 'username' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    username = session['username']
    
    # Filtrar mensagens para o usuário atual (enviadas ou recebidas)
    user_messages = [
        msg for msg in messages_store
        if msg['sender'] == username or msg['recipient'] == username
    ]
    
    return jsonify({'messages': user_messages})

@app.route('/verify_message/<int:message_id>')
def verify_message(message_id):
    """Verificar assinatura de uma mensagem"""
    if 'username' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Encontrar mensagem
    message = next((msg for msg in messages_store if msg['id'] == message_id), None)
    
    if not message:
        return jsonify({'error': 'Mensagem não encontrada'}), 404
    
    try:
        # Verificar assinatura
        is_valid, result = signature_app.verify_signature(message['signed_message'])
        
        # Atualizar status de verificação
        message['verified'] = is_valid
        message['verification_result'] = result
        
        return jsonify({
            'valid': is_valid,
            'result': result,
            'message_id': message_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na verificação: {str(e)}'}), 500

@app.route('/get_users')
def get_users():
    """Obter lista de usuários disponíveis"""
    if 'username' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    current_user = session['username']
    available_users = [
        {'username': username, 'name': data['name']}
        for username, data in users_db.items()
        if username != current_user
    ]
    
    return jsonify({'users': available_users})

@app.route('/chat_stats')
def chat_stats():
    """Estatísticas do chat"""
    if 'username' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    username = session['username']
    
    # Calcular estatísticas
    total_messages = len(messages_store)
    user_sent = len([msg for msg in messages_store if msg['sender'] == username])
    user_received = len([msg for msg in messages_store if msg['recipient'] == username])
    verified_messages = len([msg for msg in messages_store if msg.get('verified') == True])
    
    return jsonify({
        'total_messages': total_messages,
        'sent_by_user': user_sent,
        'received_by_user': user_received,
        'verified_messages': verified_messages,
        'total_users': len(users_db),
        'certificates_generated': len([u for u in users_db.values() if u['cert_id'] is not None])
    })

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('atividade2/templates', exist_ok=True)
    os.makedirs('atividade2/static', exist_ok=True)
    
    print("=== CHAT COM ASSINATURA DIGITAL ===")
    print("Usuários disponíveis:")
    print("- carlos / 123456 (Carlos Lavor Neto)")
    print("- eric / 123456 (Eric Dias Perin)")
    print("- alexandro / 123456 (Alexandro Pantoja)")
    print("\nAcesse: http://localhost:8080")
    print("=====================================")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
