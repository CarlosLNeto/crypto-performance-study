#!/usr/bin/env python3
"""
Chat Web com Assinatura Digital e WebSocket
Implementa comunicação em tempo real com autenticação e integridade
"""

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import json
import uuid
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.x509.oid import NameOID
import hashlib
import time
import psutil
import threading
import csv
from datetime import datetime

# Dados globais para coleta de métricas
chat_metrics = []
metrics_lock = threading.Lock()

def save_chat_metric(operation, username, message_size, time_taken, success=True):
    """Salva métrica de uso real do chat"""
    with metrics_lock:
        metric = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'username': username,
            'message_size': message_size,
            'time': time_taken,
            'success': success,
            'test_type': 'real_chat_usage',
            'scenario': 'real_user'
        }
        chat_metrics.append(metric)
        
        # Salvar em arquivo a cada 10 métricas
        if len(chat_metrics) % 10 == 0:
            save_metrics_to_file()

def save_metrics_to_file():
    """Salva métricas em arquivo CSV"""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, 'real_chat_metrics.csv')
    
    if chat_metrics:
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'operation', 'username', 
                                                 'message_size', 'time', 'success', 
                                                 'test_type', 'scenario'])
            writer.writeheader()
            writer.writerows(chat_metrics)

class CertificateManager:
    """Gerenciador de certificados digitais ad-hoc"""
    
    def __init__(self, cert_dir="certificates"):
        # Garantir que o diretório seja relativo ao diretório da atividade2
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cert_dir = os.path.join(script_dir, cert_dir)
        os.makedirs(self.cert_dir, exist_ok=True)
    
    def generate_certificate(self, username, common_name):
        """Gera certificado X.509 auto-assinado"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "AM"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Manaus"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UEA"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Salvar certificado e chave
        cert_path = os.path.join(self.cert_dir, f"{username}.p12")
        with open(cert_path, "wb") as f:
            f.write(pkcs12.serialize_key_and_certificates(
                b"password", private_key, cert, None,
                serialization.BestAvailableEncryption(b"password")
            ))
        
        return cert, private_key

class MessageSigner:
    """Assinador de mensagens digitais"""
    
    def __init__(self, cert_manager):
        self.cert_manager = cert_manager
        self.performance_data = []
    
    def sign_message(self, username, message):
        """Assina mensagem digitalmente"""
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.virtual_memory().used
        
        cert_path = os.path.join(self.cert_manager.cert_dir, f"{username}.p12")
        
        if not os.path.exists(cert_path):
            return None
        
        with open(cert_path, "rb") as f:
            private_key, cert, _ = pkcs12.load_key_and_certificates(
                f.read(), b"password"
            )
        
        message_bytes = message.encode('utf-8')
        signature = private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        end_time = time.time()
        end_cpu = psutil.cpu_percent()
        end_memory = psutil.virtual_memory().used
        time_taken = end_time - start_time
        
        # Coletar métricas do sistema
        self.performance_data.append({
            'operation': 'sign',
            'time': time_taken,
            'cpu_usage': end_cpu - start_cpu,
            'memory_usage': end_memory - start_memory,
            'message_size': len(message_bytes),
            'timestamp': datetime.now().isoformat()
        })
        
        # Coletar métrica real do chat
        save_chat_metric('sign', username, len(message), time_taken, True)
        
        return {
            'message': message,
            'signature': signature.hex(),
            'certificate': cert.public_bytes(serialization.Encoding.PEM).decode(),
            'timestamp': datetime.now().isoformat(),
            'sender': username
        }
    
    def verify_message(self, signed_message):
        """Verifica assinatura da mensagem"""
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.virtual_memory().used
        
        try:
            cert_pem = signed_message['certificate']
            cert = x509.load_pem_x509_certificate(cert_pem.encode())
            public_key = cert.public_key()
            
            message_bytes = signed_message['message'].encode('utf-8')
            signature = bytes.fromhex(signed_message['signature'])
            
            public_key.verify(
                signature,
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            end_time = time.time()
            end_cpu = psutil.cpu_percent()
            end_memory = psutil.virtual_memory().used
            time_taken = end_time - start_time
            
            # Coletar métricas do sistema
            self.performance_data.append({
                'operation': 'verify',
                'time': time_taken,
                'cpu_usage': end_cpu - start_cpu,
                'memory_usage': end_memory - start_memory,
                'message_size': len(message_bytes),
                'timestamp': datetime.now().isoformat()
            })
            
            # Coletar métrica real do chat
            save_chat_metric('verify', signed_message.get('sender', 'unknown'), 
                           len(signed_message['message']), time_taken, True)
            
            return True
        except Exception as e:
            end_time = time.time()
            time_taken = end_time - start_time
            save_chat_metric('verify', signed_message.get('sender', 'unknown'), 
                           len(signed_message.get('message', '')), time_taken, False)
            return False

# Configuração da aplicação
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(script_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'crypto-chat-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Instâncias globais
cert_manager = CertificateManager()
message_signer = MessageSigner(cert_manager)

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
    """Endpoint para dados de performance"""
    return {
        'performance_data': message_signer.performance_data,
        'stats': {
            'total_operations': len(message_signer.performance_data),
            'avg_sign_time': sum(d['time'] for d in message_signer.performance_data if d['operation'] == 'sign') / max(1, len([d for d in message_signer.performance_data if d['operation'] == 'sign'])),
            'avg_verify_time': sum(d['time'] for d in message_signer.performance_data if d['operation'] == 'verify') / max(1, len([d for d in message_signer.performance_data if d['operation'] == 'verify']))
        }
    }

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
