from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

import os

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