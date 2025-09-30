#!/usr/bin/env python3
"""
Chat Web com Assinatura Digital e WebSocket
Implementa comunicação em tempo real com autenticação e integridade
Segurança: Sigilo (AES), Integridade (SHA-256), Autenticidade (RSA)
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
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
import hashlib
import time
import psutil
import threading
import csv
from datetime import datetime
import base64

# Dados globais para coleta de métricas
chat_metrics = []
metrics_lock = threading.Lock()

def save_chat_metric(operation, username, message, time_taken, success=True):
    """Salva métrica de uso real do chat com informações detalhadas de tamanho"""
    with metrics_lock:
        message_chars = len(message)
        message_bytes = len(message.encode('utf-8'))
        
        metric = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'username': username,
            'message_size_chars': message_chars,
            'message_size_bytes': message_bytes,
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
                                                 'message_size_chars', 'message_size_bytes',
                                                 'time', 'success', 'test_type', 'scenario'])
            writer.writeheader()
            writer.writerows(chat_metrics)

class AESCipher:
    """Gerenciador de cifragem AES-256 para sigilo das mensagens"""
    
    def __init__(self):
        self.performance_data = []
        # Chave simétrica compartilhada (em produção, usar key exchange seguro)
        self.key = os.urandom(32)  # AES-256 (256 bits = 32 bytes)
        print(f"[AES] Chave simétrica gerada: {self.key[:8].hex()}...{self.key[-8:].hex()} (256 bits)")
    
    def encrypt(self, plaintext):
        """Cifra mensagem com AES-256-CBC"""
        print(f"\n[SIGILO - AES-256] Iniciando cifragem")
        print(f"[AES] Mensagem original: '{plaintext}' ({len(plaintext)} chars)")
        
        start_time = time.time()
        
        # Gerar IV aleatório
        iv = os.urandom(16)  # 16 bytes para AES
        print(f"[AES] IV gerado: {iv.hex()} (128 bits)")
        
        # Criar cifrador
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        print(f"[AES] Cifrador criado: AES-256-CBC")
        
        # Padding PKCS7
        plaintext_bytes = plaintext.encode('utf-8')
        padding_length = 16 - (len(plaintext_bytes) % 16)
        padded_plaintext = plaintext_bytes + bytes([padding_length] * padding_length)
        print(f"[AES] Padding PKCS7 aplicado: {len(plaintext_bytes)} → {len(padded_plaintext)} bytes")
        
        # Cifrar
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        print(f"[AES] Mensagem cifrada: {ciphertext[:16].hex()}...{ciphertext[-16:].hex()}")
        
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"[AES] ✅ Cifragem concluída em {time_taken:.6f}s")
        
        # Coletar métricas
        self.performance_data.append({
            'operation': 'aes_encrypt',
            'time': time_taken,
            'message_size': len(plaintext_bytes),
            'timestamp': datetime.now().isoformat()
        })
        
        # Retornar IV + ciphertext em base64
        result = base64.b64encode(iv + ciphertext).decode('utf-8')
        print(f"[AES] Resultado final (base64): {result[:32]}...{result[-32:]}")
        return result
    
    def decrypt(self, encrypted_data):
        """Decifra mensagem AES-256-CBC"""
        print(f"\n[SIGILO - AES-256] Iniciando decifragem")
        print(f"[AES] Dados cifrados (base64): {encrypted_data[:32]}...{encrypted_data[-32:]}")
        
        start_time = time.time()
        
        try:
            # Decodificar base64
            data = base64.b64decode(encrypted_data.encode('utf-8'))
            print(f"[AES] Dados decodificados: {len(data)} bytes")
            
            # Extrair IV e ciphertext
            iv = data[:16]
            ciphertext = data[16:]
            print(f"[AES] IV extraído: {iv.hex()}")
            print(f"[AES] Ciphertext: {ciphertext[:16].hex()}...{ciphertext[-16:].hex()}")
            
            # Criar decifrador
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            print(f"[AES] Decifrador criado com chave: {self.key[:8].hex()}...{self.key[-8:].hex()}")
            
            # Decifrar
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            print(f"[AES] Dados decifrados (com padding): {len(padded_plaintext)} bytes")
            
            # Remover padding PKCS7
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]
            print(f"[AES] Padding removido: {padding_length} bytes")
            
            end_time = time.time()
            time_taken = end_time - start_time
            
            result = plaintext.decode('utf-8')
            print(f"[AES] ✅ Decifragem concluída em {time_taken:.6f}s")
            print(f"[AES] Mensagem recuperada: '{result}' ({len(result)} chars)")
            
            # Coletar métricas
            self.performance_data.append({
                'operation': 'aes_decrypt',
                'time': time_taken,
                'message_size': len(plaintext),
                'timestamp': datetime.now().isoformat()
            })
            
            return result
        except Exception as e:
            print(f"[AES] ❌ Erro na decifragem: {e}")
            return None


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
    """Assinador de mensagens digitais com integridade (SHA-256)"""
    
    def __init__(self, cert_manager, aes_cipher):
        self.cert_manager = cert_manager
        self.aes_cipher = aes_cipher
        self.performance_data = []
    
    def compute_hash(self, message):
        """Calcula hash SHA-256 da mensagem para integridade"""
        print(f"\n[INTEGRIDADE - SHA-256] Calculando hash")
        print(f"[SHA256] Mensagem: '{message}' ({len(message)} chars)")
        
        start_time = time.time()
        
        message_bytes = message.encode('utf-8')
        print(f"[SHA256] Bytes da mensagem: {len(message_bytes)} bytes")
        
        hash_obj = hashlib.sha256(message_bytes)
        hash_digest = hash_obj.hexdigest()
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        print(f"[SHA256] ✅ Hash calculado em {time_taken:.6f}s")
        print(f"[SHA256] Hash SHA-256: {hash_digest}")
        
        self.performance_data.append({
            'operation': 'hash',
            'time': time_taken,
            'message_size': len(message_bytes),
            'timestamp': datetime.now().isoformat()
        })
        
        return hash_digest
    
    def sign_message(self, username, message):
        """
        Processa mensagem com tripla segurança:
        1. SIGILO: Cifra com AES-256
        2. INTEGRIDADE: Hash SHA-256
        3. AUTENTICIDADE: Assinatura RSA
        """
        print(f"\n{'='*80}")
        print(f"[CHAT] {username} está enviando mensagem: '{message}'")
        print(f"{'='*80}")
        
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.virtual_memory().used
        
        cert_path = os.path.join(self.cert_manager.cert_dir, f"{username}.p12")
        print(f"[CERT] Carregando certificado: {cert_path}")
        
        if not os.path.exists(cert_path):
            print(f"[CERT] ❌ Certificado não encontrado para {username}")
            return None
        
        with open(cert_path, "rb") as f:
            private_key, cert, _ = pkcs12.load_key_and_certificates(
                f.read(), b"password"
            )
        
        # Extrair informações do certificado
        subject = cert.subject
        common_name = None
        for attribute in subject:
            if attribute.oid == NameOID.COMMON_NAME:
                common_name = attribute.value
                break
        
        print(f"[CERT] ✅ Certificado carregado para: {common_name}")
        print(f"[CERT] Chave privada RSA: {private_key.key_size} bits")
        
        # 1. INTEGRIDADE: Calcular hash da mensagem original
        message_hash = self.compute_hash(message)
        
        # 2. SIGILO: Cifrar mensagem com AES-256
        encrypted_message = self.aes_cipher.encrypt(message)
        
        # 3. AUTENTICIDADE: Assinar o hash com RSA (não a mensagem cifrada)
        print(f"\n[AUTENTICIDADE - RSA-2048] Assinando hash")
        print(f"[RSA] Usuário: {username} ({common_name})")
        print(f"[RSA] Chave privada: {private_key.key_size} bits")
        print(f"[RSA] Hash a assinar: {message_hash}")
        
        hash_bytes = message_hash.encode('utf-8')
        
        sign_start = time.time()
        signature = private_key.sign(
            hash_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        sign_end = time.time()
        
        print(f"[RSA] ✅ Assinatura criada em {sign_end - sign_start:.6f}s")
        print(f"[RSA] Assinatura: {signature[:16].hex()}...{signature[-16:].hex()} ({len(signature)} bytes)")
        
        end_time = time.time()
        end_cpu = psutil.cpu_percent()
        end_memory = psutil.virtual_memory().used
        time_taken = end_time - start_time
        
        print(f"\n[RESUMO] Tripla segurança aplicada em {time_taken:.6f}s:")
        print(f"  1. ✅ SIGILO: AES-256-CBC")
        print(f"  2. ✅ INTEGRIDADE: SHA-256")
        print(f"  3. ✅ AUTENTICIDADE: RSA-2048 + PSS")
        print(f"{'='*80}")
        
        # Coletar métricas do sistema
        self.performance_data.append({
            'operation': 'sign_complete',
            'time': time_taken,
            'cpu_usage': end_cpu - start_cpu,
            'memory_usage': end_memory - start_memory,
            'message_size': len(message.encode('utf-8')),
            'timestamp': datetime.now().isoformat()
        })
        
        # Coletar métrica real do chat
        save_chat_metric('sign', username, message, time_taken, True)
        
        return {
            'message': message,  # Original para exibição local
            'encrypted_message': encrypted_message,  # Mensagem cifrada
            'message_hash': message_hash,  # Hash para verificação de integridade
            'signature': signature.hex(),  # Assinatura RSA
            'certificate': cert.public_bytes(serialization.Encoding.PEM).decode(),
            'timestamp': datetime.now().isoformat(),
            'sender': username
        }
    
    def verify_message(self, signed_message):
        """
        Verifica tripla segurança:
        1. SIGILO: Decifra com AES-256
        2. INTEGRIDADE: Valida hash SHA-256
        3. AUTENTICIDADE: Verifica assinatura RSA
        """
        sender = signed_message.get('sender', 'desconhecido')
        print(f"\n{'='*80}")
        print(f"[CHAT] Verificando mensagem de {sender}")
        print(f"{'='*80}")
        
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.virtual_memory().used
        
        try:
            cert_pem = signed_message['certificate']
            cert = x509.load_pem_x509_certificate(cert_pem.encode())
            public_key = cert.public_key()
            
            # Extrair informações do certificado
            subject = cert.subject
            common_name = None
            for attribute in subject:
                if attribute.oid == NameOID.COMMON_NAME:
                    common_name = attribute.value
                    break
            
            print(f"[CERT] Certificado do remetente: {common_name}")
            print(f"[CERT] Chave pública RSA: {public_key.key_size} bits")
            
            # 1. SIGILO: Decifrar mensagem AES-256
            encrypted_message = signed_message['encrypted_message']
            decrypted_message = self.aes_cipher.decrypt(encrypted_message)
            
            if decrypted_message is None:
                print(f"[VERIFY] ❌ Falha na decifragem AES")
                return False
            
            # 2. INTEGRIDADE: Verificar hash SHA-256
            print(f"\n[INTEGRIDADE - SHA-256] Verificando integridade")
            computed_hash = self.compute_hash(decrypted_message)
            received_hash = signed_message['message_hash']
            
            print(f"[SHA256] Hash recebido:  {received_hash}")
            print(f"[SHA256] Hash calculado: {computed_hash}")
            
            if computed_hash != received_hash:
                print("[SHA256] ❌ Falha na verificação de integridade (hash)")
                return False
            
            print(f"[SHA256] ✅ Integridade verificada com sucesso")
            
            # 3. AUTENTICIDADE: Verificar assinatura RSA
            print(f"\n[AUTENTICIDADE - RSA-2048] Verificando assinatura")
            print(f"[RSA] Remetente: {sender} ({common_name})")
            print(f"[RSA] Chave pública: {public_key.key_size} bits")
            
            hash_bytes = received_hash.encode('utf-8')
            signature = bytes.fromhex(signed_message['signature'])
            
            print(f"[RSA] Assinatura a verificar: {signature[:16].hex()}...{signature[-16:].hex()}")
            
            verify_start = time.time()
            public_key.verify(
                signature,
                hash_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            verify_end = time.time()
            
            print(f"[RSA] ✅ Assinatura verificada em {verify_end - verify_start:.6f}s")
            
            end_time = time.time()
            end_cpu = psutil.cpu_percent()
            end_memory = psutil.virtual_memory().used
            time_taken = end_time - start_time
            
            print(f"\n[RESUMO] Tripla verificação concluída em {time_taken:.6f}s:")
            print(f"  1. ✅ SIGILO: Mensagem decifrada com AES-256-CBC")
            print(f"  2. ✅ INTEGRIDADE: Hash SHA-256 válido")
            print(f"  3. ✅ AUTENTICIDADE: Assinatura RSA-2048 válida")
            print(f"[VERIFY] ✅ MENSAGEM AUTÊNTICA E ÍNTEGRA")
            print(f"{'='*80}")
            
            # Coletar métricas do sistema
            self.performance_data.append({
                'operation': 'verify_complete',
                'time': time_taken,
                'cpu_usage': end_cpu - start_cpu,
                'memory_usage': end_memory - start_memory,
                'message_size': len(decrypted_message.encode('utf-8')),
                'timestamp': datetime.now().isoformat()
            })
            
            # Coletar métrica real do chat
            save_chat_metric('verify', signed_message.get('sender', 'unknown'), 
                           decrypted_message, time_taken, True)
            
            return True
        except Exception as e:
            print(f"[VERIFY] ❌ Erro na verificação: {e}")
            print(f"[VERIFY] ❌ MENSAGEM REJEITADA")
            print(f"{'='*80}")
            end_time = time.time()
            time_taken = end_time - start_time
            save_chat_metric('verify', signed_message.get('sender', 'unknown'), 
                           signed_message.get('message', ''), time_taken, False)
            return False

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
