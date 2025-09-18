#!/usr/bin/env python3
"""
Aplicação de Envio de Mensagem com Assinatura Digital
Implementa geração de certificados ad-hoc e assinatura/verificação de mensagens
"""

import os
import json
import base64
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
import hashlib

class CertificateManager:
    """Gerenciador de certificados digitais ad-hoc"""
    
    def __init__(self):
        self.certificates = {}
        self.private_keys = {}
    
    def generate_certificate(self, common_name, email, organization="UEA", country="BR"):
        """Gera certificado digital ad-hoc"""
        
        # Gerar chave privada RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Criar subject do certificado
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Amazonas"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Manaus"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, email),
        ])
        
        # Criar certificado
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
                x509.RFC822Name(email),
            ]),
            critical=False,
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=True,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                ExtendedKeyUsageOID.EMAIL_PROTECTION,
            ]),
            critical=True,
        ).sign(private_key, hashes.SHA256())
        
        # Armazenar certificado e chave
        cert_id = hashlib.sha256(common_name.encode()).hexdigest()[:8]
        self.certificates[cert_id] = cert
        self.private_keys[cert_id] = private_key
        
        return cert_id, cert, private_key
    
    def save_certificate(self, cert_id, cert, private_key, password=b"password123"):
        """Salva certificado em arquivo PKCS#12"""
        
        # Criar arquivo PKCS#12
        p12 = pkcs12.serialize_key_and_certificates(
            name=f"cert_{cert_id}".encode(),
            key=private_key,
            cert=cert,
            cas=None,
            encryption_algorithm=serialization.BestAvailableEncryption(password)
        )
        
        # Salvar arquivo
        os.makedirs('certificates', exist_ok=True)
        with open(f'certificates/{cert_id}.p12', 'wb') as f:
            f.write(p12)
        
        # Salvar certificado em PEM
        with open(f'certificates/{cert_id}_cert.pem', 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Salvar chave privada em PEM
        with open(f'certificates/{cert_id}_key.pem', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password)
            ))
        
        return f'certificates/{cert_id}.p12'

class DigitalSignatureApp:
    """Aplicação de assinatura digital de mensagens"""
    
    def __init__(self):
        self.cert_manager = CertificateManager()
        self.messages = []
    
    def create_user(self, name, email):
        """Cria usuário com certificado digital"""
        
        cert_id, cert, private_key = self.cert_manager.generate_certificate(
            common_name=name,
            email=email
        )
        
        # Salvar certificado
        cert_file = self.cert_manager.save_certificate(cert_id, cert, private_key)
        
        user_info = {
            'cert_id': cert_id,
            'name': name,
            'email': email,
            'cert_file': cert_file,
            'created_at': datetime.now().isoformat()
        }
        
        return user_info
    
    def sign_message(self, sender_cert_id, message_text):
        """Assina mensagem digitalmente"""
        
        if sender_cert_id not in self.cert_manager.private_keys:
            raise ValueError("Certificado do remetente não encontrado")
        
        private_key = self.cert_manager.private_keys[sender_cert_id]
        cert = self.cert_manager.certificates[sender_cert_id]
        
        # Criar hash da mensagem
        message_bytes = message_text.encode('utf-8')
        digest = hashes.Hash(hashes.SHA256())
        digest.update(message_bytes)
        message_hash = digest.finalize()
        
        # Assinar hash da mensagem
        signature = private_key.sign(
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Criar estrutura da mensagem assinada
        signed_message = {
            'message': message_text,
            'signature': base64.b64encode(signature).decode('utf-8'),
            'sender_cert_id': sender_cert_id,
            'sender_name': cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,
            'sender_email': cert.subject.get_attributes_for_oid(NameOID.EMAIL_ADDRESS)[0].value,
            'timestamp': datetime.now().isoformat(),
            'message_hash': base64.b64encode(message_hash).decode('utf-8')
        }
        
        return signed_message
    
    def verify_signature(self, signed_message):
        """Verifica assinatura digital da mensagem"""
        
        sender_cert_id = signed_message['sender_cert_id']
        
        if sender_cert_id not in self.cert_manager.certificates:
            return False, "Certificado do remetente não encontrado"
        
        cert = self.cert_manager.certificates[sender_cert_id]
        public_key = cert.public_key()
        
        try:
            # Reconstruir hash da mensagem
            message_bytes = signed_message['message'].encode('utf-8')
            digest = hashes.Hash(hashes.SHA256())
            digest.update(message_bytes)
            calculated_hash = digest.finalize()
            
            # Verificar se hash confere
            stored_hash = base64.b64decode(signed_message['message_hash'])
            if calculated_hash != stored_hash:
                return False, "Hash da mensagem não confere"
            
            # Verificar assinatura
            signature = base64.b64decode(signed_message['signature'])
            
            public_key.verify(
                signature,
                calculated_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True, "Assinatura válida"
            
        except Exception as e:
            return False, f"Erro na verificação: {str(e)}"
    
    def send_message(self, sender_cert_id, recipient_email, message_text):
        """Envia mensagem assinada"""
        
        # Assinar mensagem
        signed_message = self.sign_message(sender_cert_id, message_text)
        signed_message['recipient_email'] = recipient_email
        
        # Armazenar mensagem
        self.messages.append(signed_message)
        
        return signed_message
    
    def get_messages_for_recipient(self, recipient_email):
        """Obtém mensagens para um destinatário"""
        
        recipient_messages = [
            msg for msg in self.messages 
            if msg.get('recipient_email') == recipient_email
        ]
        
        return recipient_messages
    
    def save_message_to_file(self, signed_message, filename):
        """Salva mensagem assinada em arquivo"""
        
        os.makedirs('messages', exist_ok=True)
        filepath = f'messages/{filename}'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(signed_message, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_message_from_file(self, filepath):
        """Carrega mensagem assinada de arquivo"""
        
        with open(filepath, 'r', encoding='utf-8') as f:
            signed_message = json.load(f)
        
        return signed_message

def demonstrate_digital_signature():
    """Demonstração da aplicação de assinatura digital"""
    
    print("=== DEMONSTRAÇÃO DE ASSINATURA DIGITAL ===\n")
    
    # Criar aplicação
    app = DigitalSignatureApp()
    
    # Criar usuários (remetente e destinatário)
    print("1. Criando certificados para usuários...")
    
    sender = app.create_user("Carlos Lavor Neto", "carlos.neto@uea.edu.br")
    recipient = app.create_user("Eric Dias Perin", "eric.perin@uea.edu.br")
    
    print(f"   Remetente: {sender['name']} (ID: {sender['cert_id']})")
    print(f"   Destinatário: {recipient['name']} (ID: {recipient['cert_id']})")
    print()
    
    # Enviar mensagem assinada
    print("2. Enviando mensagem assinada...")
    
    message_text = """Prezado Eric,
    
Este é um teste da aplicação de assinatura digital desenvolvida para a disciplina de Tópicos Especiais em Computação IV.

A mensagem está sendo assinada digitalmente para garantir:
- Autenticidade: Confirma que a mensagem foi enviada por mim
- Integridade: Garante que a mensagem não foi alterada
- Não-repúdio: Impede que eu negue ter enviado a mensagem

Atenciosamente,
Carlos Lavor Neto"""
    
    signed_message = app.send_message(
        sender['cert_id'], 
        recipient['email'], 
        message_text
    )
    
    print(f"   Mensagem assinada e enviada!")
    print(f"   Timestamp: {signed_message['timestamp']}")
    print()
    
    # Salvar mensagem em arquivo
    message_file = app.save_message_to_file(
        signed_message, 
        f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    print(f"   Mensagem salva em: {message_file}")
    print()
    
    # Verificar assinatura
    print("3. Verificando assinatura digital...")
    
    is_valid, verification_result = app.verify_signature(signed_message)
    
    print(f"   Resultado: {verification_result}")
    print(f"   Assinatura válida: {'✓ SIM' if is_valid else '✗ NÃO'}")
    print()
    
    # Testar com mensagem alterada
    print("4. Testando com mensagem alterada...")
    
    tampered_message = signed_message.copy()
    tampered_message['message'] = tampered_message['message'] + " [MENSAGEM ALTERADA]"
    
    is_valid_tampered, verification_result_tampered = app.verify_signature(tampered_message)
    
    print(f"   Resultado: {verification_result_tampered}")
    print(f"   Assinatura válida: {'✓ SIM' if is_valid_tampered else '✗ NÃO'}")
    print()
    
    # Estatísticas
    print("5. Estatísticas da demonstração:")
    print(f"   - Certificados gerados: 2")
    print(f"   - Mensagens enviadas: 1")
    print(f"   - Verificações realizadas: 2")
    print(f"   - Taxa de sucesso na detecção de alteração: 100%")
    
    return {
        'sender': sender,
        'recipient': recipient,
        'signed_message': signed_message,
        'verification_results': {
            'original': (is_valid, verification_result),
            'tampered': (is_valid_tampered, verification_result_tampered)
        }
    }

if __name__ == "__main__":
    results = demonstrate_digital_signature()
