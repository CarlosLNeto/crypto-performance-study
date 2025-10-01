import threading
import csv
import os
from datetime import datetime

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