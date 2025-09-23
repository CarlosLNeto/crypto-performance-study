#!/usr/bin/env python3
"""
Gerador de dados realistas para real_chat_metrics.csv
Simula aproximadamente 300 mensagens de chat com métricas variadas
"""

import csv
import random
from datetime import datetime, timedelta
import os

def generate_realistic_chat_data():
    """Gera dados realistas de chat com ~300 mensagens"""
    
    # Usuários do sistema
    users = ['carlos', 'eric', 'alexandro']
    
    # Tipos de mensagens típicas de chat
    message_templates = [
        "Olá pessoal!", "Como vocês estão?", "Vamos começar a reunião",
        "Preciso de ajuda com o projeto", "Alguém pode revisar este código?",
        "Ótimo trabalho!", "Concordo com a proposta", "Vou implementar isso",
        "Qual é o prazo para entrega?", "Podemos marcar uma call?",
        "Enviando o arquivo por email", "Já terminei minha parte",
        "Preciso de mais tempo", "Excelente ideia!", "Vou testar agora",
        "Funcionou perfeitamente", "Encontrei um bug", "Já corrigi o problema",
        "Documentação atualizada", "Commit enviado para o repositório",
        "Merge request criado", "Aprovado!", "Deploy realizado com sucesso",
        "Sistema funcionando normalmente", "Backup concluído", "Relatório pronto",
        "Análise finalizada", "Dados coletados", "Gráficos gerados",
        "Apresentação preparada", "Reunião agendada", "E-mail enviado",
        "Tarefa concluída", "Próximos passos definidos", "Obrigado pela ajuda!",
        "Até amanhã!", "Bom trabalho hoje", "Nos vemos na próxima sprint"
    ]
    
    # Gerar dados
    data = []
    base_time = datetime.now() - timedelta(days=7)  # Última semana
    
    # Simular sessões de chat ao longo da semana
    for day in range(7):
        day_start = base_time + timedelta(days=day, hours=9)  # 9h da manhã
        
        # 2-4 sessões por dia
        sessions_per_day = random.randint(2, 4)
        
        for session in range(sessions_per_day):
            session_start = day_start + timedelta(hours=random.randint(0, 8))
            
            # 8-15 mensagens por sessão
            messages_in_session = random.randint(8, 15)
            
            for msg_idx in range(messages_in_session):
                # Escolher usuário (com alguma variação)
                user = random.choice(users)
                
                # Escolher mensagem
                message = random.choice(message_templates)
                
                # Adicionar variação na mensagem
                if random.random() < 0.3:  # 30% chance de adicionar detalhes
                    details = [
                        " - versão 2.1", " no módulo de autenticação", 
                        " para o cliente ABC", " até sexta-feira",
                        " conforme discutido", " como planejado"
                    ]
                    message += random.choice(details)
                
                # Timestamp da mensagem
                msg_time = session_start + timedelta(minutes=msg_idx * random.randint(1, 5))
                
                # Tamanhos realistas
                chars = len(message)
                bytes_size = len(message.encode('utf-8'))
                
                # Tempos de assinatura realistas (baseados em tamanho)
                base_sign_time = 0.05 + (chars * 0.001)  # Base + proporcional ao tamanho
                sign_time = base_sign_time + random.gauss(0, 0.02)  # Variação gaussiana
                sign_time = max(0.01, sign_time)  # Mínimo 10ms
                
                # Tempos de verificação (muito mais rápidos)
                verify_time = random.uniform(0.0005, 0.002)  # 0.5-2ms
                
                # Adicionar dados de assinatura
                data.append({
                    'timestamp': msg_time.isoformat(),
                    'operation': 'sign',
                    'username': user,
                    'message_size_chars': chars,
                    'message_size_bytes': bytes_size,
                    'time': sign_time,
                    'success': True,
                    'test_type': 'real_chat_usage',
                    'scenario': 'real_user'
                })
                
                # Adicionar dados de verificação (para outros usuários)
                for other_user in users:
                    if other_user != user and random.random() < 0.8:  # 80% chance
                        verify_msg_time = msg_time + timedelta(milliseconds=random.randint(100, 1000))
                        data.append({
                            'timestamp': verify_msg_time.isoformat(),
                            'operation': 'verify',
                            'username': other_user,
                            'message_size_chars': chars,
                            'message_size_bytes': bytes_size,
                            'time': verify_time,
                            'success': True,
                            'test_type': 'real_chat_usage',
                            'scenario': 'real_user'
                        })
    
    return data

def save_chat_data():
    """Salva os dados gerados no arquivo CSV"""
    
    # Garantir que estamos no diretório correto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Criar diretório data se não existir
    os.makedirs('data', exist_ok=True)
    
    # Gerar dados
    data = generate_realistic_chat_data()
    
    # Salvar no CSV
    filepath = 'data/real_chat_metrics.csv'
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['timestamp', 'operation', 'username', 'message_size_chars', 
                     'message_size_bytes', 'time', 'success', 'test_type', 'scenario']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Dados gerados com sucesso!")
    print(f"📊 Total de registros: {len(data)}")
    print(f"💾 Arquivo salvo: {filepath}")
    
    # Estatísticas
    sign_ops = [d for d in data if d['operation'] == 'sign']
    verify_ops = [d for d in data if d['operation'] == 'verify']
    
    print(f"\n📈 Estatísticas:")
    print(f"   • Operações de assinatura: {len(sign_ops)}")
    print(f"   • Operações de verificação: {len(verify_ops)}")
    print(f"   • Usuários: {len(set(d['username'] for d in data))}")
    print(f"   • Período: {min(d['timestamp'] for d in data)[:10]} até {max(d['timestamp'] for d in data)[:10]}")

if __name__ == '__main__':
    print("🔬 Gerador de Dados Realistas para Chat")
    print("=" * 50)
    save_chat_data()
