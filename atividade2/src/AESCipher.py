from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import time
import base64
import os

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