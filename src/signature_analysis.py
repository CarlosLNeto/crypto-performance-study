#!/usr/bin/env python3
"""
Análise de Performance da Aplicação de Assinatura Digital
Coleta métricas de tempo, CPU e memória para operações criptográficas
"""

import time
import psutil
import gc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from digital_signature_app import DigitalSignatureApp
import os

class SignaturePerformanceAnalyzer:
    """Analisador de performance para assinatura digital"""
    
    def __init__(self):
        self.app = DigitalSignatureApp()
        self.results = []
        self.iterations = 50
        
    def measure_certificate_generation(self):
        """Mede performance da geração de certificados"""
        
        print("Medindo performance da geração de certificados...")
        
        times = []
        cpu_usage = []
        memory_usage = []
        
        process = psutil.Process()
        
        for i in range(self.iterations):
            gc.collect()
            
            # Medição inicial
            start_memory = process.memory_info().rss / 1024 / 1024
            start_time = time.perf_counter()
            start_cpu = process.cpu_percent()
            
            # Gerar certificado
            user = self.app.create_user(f"User{i}", f"user{i}@test.com")
            
            # Medição final
            end_time = time.perf_counter()
            end_cpu = process.cpu_percent()
            end_memory = process.memory_info().rss / 1024 / 1024
            
            times.append(end_time - start_time)
            cpu_usage.append(max(end_cpu - start_cpu, 0))
            memory_usage.append(end_memory - start_memory)
        
        return {
            'operation': 'certificate_generation',
            'time_mean': np.mean(times),
            'time_std': np.std(times),
            'cpu_mean': np.mean(cpu_usage),
            'cpu_std': np.std(cpu_usage),
            'memory_mean': np.mean(memory_usage),
            'memory_std': np.std(memory_usage),
            'iterations': self.iterations
        }
    
    def measure_message_signing(self, message_sizes=[100, 500, 1000, 5000, 10000]):
        """Mede performance da assinatura de mensagens"""
        
        print("Medindo performance da assinatura de mensagens...")
        
        # Criar usuário para testes
        user = self.app.create_user("TestSigner", "signer@test.com")
        cert_id = user['cert_id']
        
        results = []
        
        for size in message_sizes:
            print(f"  Testando mensagens de {size} caracteres...")
            
            # Gerar mensagem de teste
            test_message = "A" * size
            
            times = []
            cpu_usage = []
            memory_usage = []
            
            process = psutil.Process()
            
            for i in range(self.iterations):
                gc.collect()
                
                # Medição inicial
                start_memory = process.memory_info().rss / 1024 / 1024
                start_time = time.perf_counter()
                start_cpu = process.cpu_percent()
                
                # Assinar mensagem
                signed_msg = self.app.sign_message(cert_id, test_message)
                
                # Medição final
                end_time = time.perf_counter()
                end_cpu = process.cpu_percent()
                end_memory = process.memory_info().rss / 1024 / 1024
                
                times.append(end_time - start_time)
                cpu_usage.append(max(end_cpu - start_cpu, 0))
                memory_usage.append(end_memory - start_memory)
            
            results.append({
                'operation': 'message_signing',
                'message_size': size,
                'time_mean': np.mean(times),
                'time_std': np.std(times),
                'cpu_mean': np.mean(cpu_usage),
                'cpu_std': np.std(cpu_usage),
                'memory_mean': np.mean(memory_usage),
                'memory_std': np.std(memory_usage),
                'throughput': size / np.mean(times),  # chars/second
                'iterations': self.iterations
            })
        
        return results
    
    def measure_signature_verification(self, message_sizes=[100, 500, 1000, 5000, 10000]):
        """Mede performance da verificação de assinaturas"""
        
        print("Medindo performance da verificação de assinaturas...")
        
        # Criar usuário para testes
        user = self.app.create_user("TestVerifier", "verifier@test.com")
        cert_id = user['cert_id']
        
        results = []
        
        for size in message_sizes:
            print(f"  Testando verificação de mensagens de {size} caracteres...")
            
            # Gerar e assinar mensagem de teste
            test_message = "B" * size
            signed_message = self.app.sign_message(cert_id, test_message)
            
            times = []
            cpu_usage = []
            memory_usage = []
            
            process = psutil.Process()
            
            for i in range(self.iterations):
                gc.collect()
                
                # Medição inicial
                start_memory = process.memory_info().rss / 1024 / 1024
                start_time = time.perf_counter()
                start_cpu = process.cpu_percent()
                
                # Verificar assinatura
                is_valid, result = self.app.verify_signature(signed_message)
                
                # Medição final
                end_time = time.perf_counter()
                end_cpu = process.cpu_percent()
                end_memory = process.memory_info().rss / 1024 / 1024
                
                times.append(end_time - start_time)
                cpu_usage.append(max(end_cpu - start_cpu, 0))
                memory_usage.append(end_memory - start_memory)
            
            results.append({
                'operation': 'signature_verification',
                'message_size': size,
                'time_mean': np.mean(times),
                'time_std': np.std(times),
                'cpu_mean': np.mean(cpu_usage),
                'cpu_std': np.std(cpu_usage),
                'memory_mean': np.mean(memory_usage),
                'memory_std': np.std(memory_usage),
                'throughput': size / np.mean(times),  # chars/second
                'iterations': self.iterations
            })
        
        return results
    
    def run_complete_analysis(self):
        """Executa análise completa de performance"""
        
        print("=== ANÁLISE DE PERFORMANCE - ASSINATURA DIGITAL ===\n")
        
        # Análise de geração de certificados
        cert_results = self.measure_certificate_generation()
        self.results.append(cert_results)
        
        # Análise de assinatura de mensagens
        signing_results = self.measure_message_signing()
        self.results.extend(signing_results)
        
        # Análise de verificação de assinaturas
        verification_results = self.measure_signature_verification()
        self.results.extend(verification_results)
        
        # Converter para DataFrame
        df = pd.DataFrame(self.results)
        
        # Salvar resultados
        df.to_csv('data/signature_performance_results.csv', index=False)
        print(f"Resultados salvos em 'data/signature_performance_results.csv'")
        
        return df
    
    def create_performance_visualizations(self, df):
        """Cria visualizações de performance"""
        
        print("Gerando visualizações de performance...")
        
        # Configurar estilo
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 1. Gráfico de tempo por operação
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análise de Performance - Assinatura Digital', fontsize=16, fontweight='bold')
        
        # Filtrar dados por operação
        signing_data = df[df['operation'] == 'message_signing']
        verification_data = df[df['operation'] == 'signature_verification']
        
        # Tempo de assinatura vs tamanho da mensagem
        ax1 = axes[0, 0]
        if not signing_data.empty:
            ax1.plot(signing_data['message_size'], signing_data['time_mean'], 
                    marker='o', linewidth=2, label='Assinatura')
            ax1.fill_between(signing_data['message_size'], 
                           signing_data['time_mean'] - signing_data['time_std'],
                           signing_data['time_mean'] + signing_data['time_std'], 
                           alpha=0.3)
        ax1.set_xlabel('Tamanho da Mensagem (caracteres)')
        ax1.set_ylabel('Tempo (segundos)')
        ax1.set_title('Tempo de Assinatura vs Tamanho da Mensagem')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Tempo de verificação vs tamanho da mensagem
        ax2 = axes[0, 1]
        if not verification_data.empty:
            ax2.plot(verification_data['message_size'], verification_data['time_mean'], 
                    marker='s', linewidth=2, label='Verificação', color='orange')
            ax2.fill_between(verification_data['message_size'], 
                           verification_data['time_mean'] - verification_data['time_std'],
                           verification_data['time_mean'] + verification_data['time_std'], 
                           alpha=0.3, color='orange')
        ax2.set_xlabel('Tamanho da Mensagem (caracteres)')
        ax2.set_ylabel('Tempo (segundos)')
        ax2.set_title('Tempo de Verificação vs Tamanho da Mensagem')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Throughput comparativo
        ax3 = axes[1, 0]
        if not signing_data.empty and not verification_data.empty:
            ax3.plot(signing_data['message_size'], signing_data['throughput'], 
                    marker='o', linewidth=2, label='Assinatura')
            ax3.plot(verification_data['message_size'], verification_data['throughput'], 
                    marker='s', linewidth=2, label='Verificação')
        ax3.set_xlabel('Tamanho da Mensagem (caracteres)')
        ax3.set_ylabel('Throughput (chars/segundo)')
        ax3.set_title('Throughput: Assinatura vs Verificação')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Uso de CPU por operação
        ax4 = axes[1, 1]
        operations = df['operation'].unique()
        cpu_means = [df[df['operation'] == op]['cpu_mean'].mean() for op in operations]
        
        bars = ax4.bar(range(len(operations)), cpu_means, 
                      color=['skyblue', 'lightcoral', 'lightgreen'][:len(operations)])
        ax4.set_xlabel('Operação')
        ax4.set_ylabel('CPU Médio (%)')
        ax4.set_title('Uso Médio de CPU por Operação')
        ax4.set_xticks(range(len(operations)))
        ax4.set_xticklabels([op.replace('_', '\n') for op in operations], rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, cpu_means):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{value:.2f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('results/graficos/signature_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Gráfico de comparação de operações
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Comparação de Performance: Assinatura vs Verificação', fontsize=16, fontweight='bold')
        
        # Boxplot de tempos
        if not signing_data.empty and not verification_data.empty:
            data_for_box = []
            labels_for_box = []
            
            for _, row in signing_data.iterrows():
                data_for_box.extend([row['time_mean']] * 10)  # Simular distribuição
                labels_for_box.extend([f"Assinatura\n{row['message_size']} chars"] * 10)
            
            for _, row in verification_data.iterrows():
                data_for_box.extend([row['time_mean']] * 10)
                labels_for_box.extend([f"Verificação\n{row['message_size']} chars"] * 10)
            
            # Criar DataFrame para seaborn
            box_df = pd.DataFrame({
                'Tempo': data_for_box,
                'Operação': labels_for_box
            })
            
            sns.boxplot(data=box_df, x='Operação', y='Tempo', ax=ax1)
            ax1.set_title('Distribuição de Tempos por Operação')
            ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico de memória
        memory_data = df[df['operation'].isin(['message_signing', 'signature_verification'])]
        if not memory_data.empty:
            for operation in memory_data['operation'].unique():
                op_data = memory_data[memory_data['operation'] == operation]
                ax2.plot(op_data['message_size'], op_data['memory_mean'], 
                        marker='o', linewidth=2, label=operation.replace('_', ' ').title())
        
        ax2.set_xlabel('Tamanho da Mensagem (caracteres)')
        ax2.set_ylabel('Uso de Memória (MB)')
        ax2.set_title('Uso de Memória vs Tamanho da Mensagem')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('results/graficos/signature_operations_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Visualizações salvas em results/graficos/")

def main():
    """Função principal"""
    
    # Criar analisador
    analyzer = SignaturePerformanceAnalyzer()
    
    # Executar análise completa
    df = analyzer.run_complete_analysis()
    
    # Criar visualizações
    analyzer.create_performance_visualizations(df)
    
    # Mostrar estatísticas resumidas
    print("\n=== RESUMO DOS RESULTADOS ===")
    
    cert_gen = df[df['operation'] == 'certificate_generation']
    if not cert_gen.empty:
        print(f"Geração de Certificados:")
        print(f"  - Tempo médio: {cert_gen['time_mean'].iloc[0]:.4f}s")
        print(f"  - CPU médio: {cert_gen['cpu_mean'].iloc[0]:.2f}%")
    
    signing = df[df['operation'] == 'message_signing']
    if not signing.empty:
        print(f"Assinatura de Mensagens:")
        print(f"  - Tempo médio: {signing['time_mean'].mean():.4f}s")
        print(f"  - Throughput médio: {signing['throughput'].mean():.0f} chars/s")
    
    verification = df[df['operation'] == 'signature_verification']
    if not verification.empty:
        print(f"Verificação de Assinaturas:")
        print(f"  - Tempo médio: {verification['time_mean'].mean():.4f}s")
        print(f"  - Throughput médio: {verification['throughput'].mean():.0f} chars/s")
    
    return df

if __name__ == "__main__":
    results_df = main()
