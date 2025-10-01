#!/usr/bin/env python3
"""
Chat Web com Assinatura Digital e WebSocket
Implementa comunicação em tempo real com autenticação e integridade
Segurança: Sigilo (AES), Integridade (SHA-256), Autenticidade (RSA)
"""

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import uuid
import os

from AESCipher import AESCipher
from CertificateManager import CertificateManager
from MessagesSigner import MessageSigner



# Configuração da aplicação
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(script_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'crypto-chat-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Instâncias globais
cert_manager = CertificateManager()
aes_cipher = AESCipher()
message_signer = MessageSigner(cert_manager, aes_cipher)

# Usuários pré-cadastrados
USERS = {
    'carlos': {'password': '123456', 'name': 'Carlos Lavor Neto'},
    'eric': {'password': '123456', 'name': 'Eric Dias Perin'},
    'alexandro': {'password': '123456', 'name': 'Alexandro Pantoja'}
}

# Estatísticas em tempo real
chat_stats = {
    'messages_sent': 0,
    'messages_verified': 0,
    'active_users': set(),
    'total_signatures': 0,
    'verification_success_rate': 100.0
}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['name'] = USERS[username]['name']
            
            # Gerar certificado se não existir
            cert_path = os.path.join(cert_manager.cert_dir, f"{username}.p12")
            if not os.path.exists(cert_path):
                cert_manager.generate_certificate(username, USERS[username]['name'])
            
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        chat_stats['active_users'].discard(session['username'])
    session.clear()
    return redirect(url_for('login'))

@socketio.on('connect')
def on_connect():
    if 'username' in session:
        join_room('chat')
        chat_stats['active_users'].add(session['username'])
        emit('user_joined', {
            'username': session['username'],
            'name': session['name'],
            'timestamp': datetime.now().isoformat()
        }, room='chat')
        
        # Enviar estatísticas atualizadas
        emit('stats_update', {
            'active_users': len(chat_stats['active_users']),
            'messages_sent': chat_stats['messages_sent'],
            'verification_rate': chat_stats['verification_success_rate']
        }, room='chat')

@socketio.on('disconnect')
def on_disconnect():
    if 'username' in session:
        chat_stats['active_users'].discard(session['username'])
        leave_room('chat')
        emit('user_left', {
            'username': session['username'],
            'timestamp': datetime.now().isoformat()
        }, room='chat')

@socketio.on('send_message')
def handle_message(data):
    if 'username' not in session:
        return
    
    username = session['username']
    message = data['message']
    
    # Assinar mensagem
    signed_message = message_signer.sign_message(username, message)
    
    if signed_message:
        # Verificar assinatura
        is_valid = message_signer.verify_message(signed_message)
        
        # Atualizar estatísticas
        chat_stats['messages_sent'] += 1
        chat_stats['total_signatures'] += 1
        if is_valid:
            chat_stats['messages_verified'] += 1
        
        chat_stats['verification_success_rate'] = (
            chat_stats['messages_verified'] / chat_stats['total_signatures'] * 100
        )
        
        # Enviar mensagem para todos
        emit('new_message', {
            'id': str(uuid.uuid4()),
            'username': username,
            'name': session['name'],
            'message': message,
            'timestamp': signed_message['timestamp'],
            'verified': is_valid,
            'signature_preview': signed_message['signature'][:16] + '...'
        }, room='chat')
        
        # Atualizar estatísticas
        emit('stats_update', {
            'active_users': len(chat_stats['active_users']),
            'messages_sent': chat_stats['messages_sent'],
            'verification_rate': chat_stats['verification_success_rate']
        }, room='chat')

@app.route('/performance')
def performance():
    """Endpoint para dados de performance com detalhamento de operações"""
    all_operations = (
        message_signer.performance_data + 
        aes_cipher.performance_data
    )
    
    # Separar por tipo de operação
    sign_ops = [d for d in all_operations if d['operation'] == 'sign_complete']
    verify_ops = [d for d in all_operations if d['operation'] == 'verify_complete']
    hash_ops = [d for d in all_operations if d['operation'] == 'hash']
    aes_enc_ops = [d for d in all_operations if d['operation'] == 'aes_encrypt']
    aes_dec_ops = [d for d in all_operations if d['operation'] == 'aes_decrypt']
    
    return {
        'performance_data': all_operations,
        'stats': {
            'total_operations': len(all_operations),
            'avg_sign_time': sum(d['time'] for d in sign_ops) / max(1, len(sign_ops)),
            'avg_verify_time': sum(d['time'] for d in verify_ops) / max(1, len(verify_ops)),
            'avg_hash_time': sum(d['time'] for d in hash_ops) / max(1, len(hash_ops)),
            'avg_aes_encrypt_time': sum(d['time'] for d in aes_enc_ops) / max(1, len(aes_enc_ops)),
            'avg_aes_decrypt_time': sum(d['time'] for d in aes_dec_ops) / max(1, len(aes_dec_ops)),
            'security_layers': {
                'sigilo': 'AES-256-CBC',
                'integridade': 'SHA-256',
                'autenticidade': 'RSA-2048 + PSS'
            }
        }
    }

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
