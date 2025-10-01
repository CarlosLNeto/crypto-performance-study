from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
import hashlib
import time
import psutil
from cryptography import x509
import os
from utils import save_chat_metric

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