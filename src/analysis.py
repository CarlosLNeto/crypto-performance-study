#!/usr/bin/env python3
"""
Módulo de Análise e Visualização dos Resultados
Gera gráficos e análises estatísticas dos benchmarks
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os

# Configuração do matplotlib para português
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

class CryptoAnalysis:
    def __init__(self, results_df):
        self.df = results_df
        self.output_dir = 'results/graficos'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configurar estilo dos gráficos
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    def format_data_size(self, size_bytes):
        """Formata tamanho dos dados para exibição"""
        if size_bytes >= 1048576:
            return f"{size_bytes/1048576:.0f}MB"
        elif size_bytes >= 1024:
            return f"{size_bytes/1024:.0f}KB"
        else:
            return f"{size_bytes}B"
    
    def create_performance_comparison(self):
        """Cria gráficos de comparação de performance"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Comparação de Performance dos Algoritmos de Criptografia', fontsize=16, fontweight='bold')
        
        # Preparar dados
        df_plot = self.df.copy()
        df_plot['data_size_label'] = df_plot['data_size'].apply(self.format_data_size)
        df_plot['algorithm_key'] = df_plot['algorithm'] + ' (' + df_plot['key_size'].astype(str) + ' bits)'
        
        # 1. Tempo de Criptografia
        ax1 = axes[0, 0]
        pivot_encrypt = df_plot.pivot_table(values='encrypt_time_mean', 
                                          index='data_size_label', 
                                          columns='algorithm_key', 
                                          aggfunc='mean')
        pivot_encrypt.plot(kind='bar', ax=ax1, width=0.8)
        ax1.set_title('Tempo Médio de Criptografia', fontweight='bold')
        ax1.set_xlabel('Tamanho dos Dados')
        ax1.set_ylabel('Tempo (segundos)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Tempo de Descriptografia
        ax2 = axes[0, 1]
        pivot_decrypt = df_plot.pivot_table(values='decrypt_time_mean', 
                                          index='data_size_label', 
                                          columns='algorithm_key', 
                                          aggfunc='mean')
        pivot_decrypt.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('Tempo Médio de Descriptografia', fontweight='bold')
        ax2.set_xlabel('Tamanho dos Dados')
        ax2.set_ylabel('Tempo (segundos)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Uso de CPU
        ax3 = axes[1, 0]
        pivot_cpu = df_plot.pivot_table(values='encrypt_cpu_mean', 
                                       index='data_size_label', 
                                       columns='algorithm_key', 
                                       aggfunc='mean')
        pivot_cpu.plot(kind='bar', ax=ax3, width=0.8)
        ax3.set_title('Uso Médio de CPU (Criptografia)', fontweight='bold')
        ax3.set_xlabel('Tamanho dos Dados')
        ax3.set_ylabel('CPU (%)')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Uso de Memória
        ax4 = axes[1, 1]
        pivot_memory = df_plot.pivot_table(values='encrypt_memory_mean', 
                                         index='data_size_label', 
                                         columns='algorithm_key', 
                                         aggfunc='mean')
        pivot_memory.plot(kind='bar', ax=ax4, width=0.8)
        ax4.set_title('Uso Médio de Memória (Criptografia)', fontweight='bold')
        ax4.set_xlabel('Tamanho dos Dados')
        ax4.set_ylabel('Memória (MB)')
        ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_throughput_analysis(self):
        """Cria análise de throughput"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Análise de Throughput (MB/s)', fontsize=16, fontweight='bold')
        
        df_plot = self.df.copy()
        df_plot['algorithm_key'] = df_plot['algorithm'] + ' (' + df_plot['key_size'].astype(str) + ' bits)'
        
        # Throughput de Criptografia
        sns.boxplot(data=df_plot, x='algorithm', y='throughput_encrypt', hue='key_size', ax=ax1)
        ax1.set_title('Throughput de Criptografia', fontweight='bold')
        ax1.set_xlabel('Algoritmo')
        ax1.set_ylabel('Throughput (MB/s)')
        ax1.legend(title='Tamanho da Chave (bits)')
        
        # Throughput de Descriptografia
        sns.boxplot(data=df_plot, x='algorithm', y='throughput_decrypt', hue='key_size', ax=ax2)
        ax2.set_title('Throughput de Descriptografia', fontweight='bold')
        ax2.set_xlabel('Algoritmo')
        ax2.set_ylabel('Throughput (MB/s)')
        ax2.legend(title='Tamanho da Chave (bits)')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/throughput_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_scalability_analysis(self):
        """Cria análise de escalabilidade"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Escalabilidade por Tamanho de Dados', fontsize=16, fontweight='bold')
        
        algorithms = self.df['algorithm'].unique()
        colors = sns.color_palette("husl", len(algorithms))
        
        for i, algorithm in enumerate(algorithms):
            alg_data = self.df[self.df['algorithm'] == algorithm]
            
            # Tempo vs Tamanho dos Dados
            ax1 = axes[0, 0]
            for key_size in alg_data['key_size'].unique():
                key_data = alg_data[alg_data['key_size'] == key_size]
                ax1.plot(key_data['data_size'], key_data['encrypt_time_mean'], 
                        marker='o', label=f'{algorithm} {key_size}bits', alpha=0.7)
            
            # CPU vs Tamanho dos Dados
            ax2 = axes[0, 1]
            for key_size in alg_data['key_size'].unique():
                key_data = alg_data[alg_data['key_size'] == key_size]
                ax2.plot(key_data['data_size'], key_data['encrypt_cpu_mean'], 
                        marker='s', label=f'{algorithm} {key_size}bits', alpha=0.7)
            
            # Memória vs Tamanho dos Dados
            ax3 = axes[1, 0]
            for key_size in alg_data['key_size'].unique():
                key_data = alg_data[alg_data['key_size'] == key_size]
                ax3.plot(key_data['data_size'], key_data['encrypt_memory_mean'], 
                        marker='^', label=f'{algorithm} {key_size}bits', alpha=0.7)
            
            # Throughput vs Tamanho dos Dados
            ax4 = axes[1, 1]
            for key_size in alg_data['key_size'].unique():
                key_data = alg_data[alg_data['key_size'] == key_size]
                ax4.plot(key_data['data_size'], key_data['throughput_encrypt'], 
                        marker='d', label=f'{algorithm} {key_size}bits', alpha=0.7)
        
        # Configurar eixos
        ax1.set_title('Tempo de Criptografia vs Tamanho dos Dados')
        ax1.set_xlabel('Tamanho dos Dados (bytes)')
        ax1.set_ylabel('Tempo (segundos)')
        ax1.set_xscale('log')
        ax1.legend()
        
        ax2.set_title('Uso de CPU vs Tamanho dos Dados')
        ax2.set_xlabel('Tamanho dos Dados (bytes)')
        ax2.set_ylabel('CPU (%)')
        ax2.set_xscale('log')
        ax2.legend()
        
        ax3.set_title('Uso de Memória vs Tamanho dos Dados')
        ax3.set_xlabel('Tamanho dos Dados (bytes)')
        ax3.set_ylabel('Memória (MB)')
        ax3.set_xscale('log')
        ax3.legend()
        
        ax4.set_title('Throughput vs Tamanho dos Dados')
        ax4.set_xlabel('Tamanho dos Dados (bytes)')
        ax4.set_ylabel('Throughput (MB/s)')
        ax4.set_xscale('log')
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/scalability_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_statistical_analysis(self):
        """Cria análise estatística detalhada"""
        # Análise de variância (ANOVA)
        algorithms = self.df['algorithm'].unique()
        
        # ANOVA para tempo de criptografia
        groups_encrypt = [self.df[self.df['algorithm'] == alg]['encrypt_time_mean'].values 
                         for alg in algorithms]
        f_stat_encrypt, p_value_encrypt = stats.f_oneway(*groups_encrypt)
        
        # ANOVA para uso de CPU
        groups_cpu = [self.df[self.df['algorithm'] == alg]['encrypt_cpu_mean'].values 
                     for alg in algorithms]
        f_stat_cpu, p_value_cpu = stats.f_oneway(*groups_cpu)
        
        # ANOVA para uso de memória
        groups_memory = [self.df[self.df['algorithm'] == alg]['encrypt_memory_mean'].values 
                        for alg in algorithms]
        f_stat_memory, p_value_memory = stats.f_oneway(*groups_memory)
        
        # Criar relatório estatístico
        stats_report = f"""
ANÁLISE ESTATÍSTICA DOS ALGORITMOS DE CRIPTOGRAFIA

1. ANÁLISE DE VARIÂNCIA (ANOVA)
   
   Tempo de Criptografia:
   - F-statistic: {f_stat_encrypt:.4f}
   - P-value: {p_value_encrypt:.6f}
   - Significância: {'Sim' if p_value_encrypt < 0.05 else 'Não'} (α = 0.05)
   
   Uso de CPU:
   - F-statistic: {f_stat_cpu:.4f}
   - P-value: {p_value_cpu:.6f}
   - Significância: {'Sim' if p_value_cpu < 0.05 else 'Não'} (α = 0.05)
   
   Uso de Memória:
   - F-statistic: {f_stat_memory:.4f}
   - P-value: {p_value_memory:.6f}
   - Significância: {'Sim' if p_value_memory < 0.05 else 'Não'} (α = 0.05)

2. ESTATÍSTICAS DESCRITIVAS POR ALGORITMO
"""
        
        for algorithm in algorithms:
            alg_data = self.df[self.df['algorithm'] == algorithm]
            stats_report += f"""
   {algorithm}:
   - Tempo médio de criptografia: {alg_data['encrypt_time_mean'].mean():.6f}s (±{alg_data['encrypt_time_mean'].std():.6f})
   - CPU médio: {alg_data['encrypt_cpu_mean'].mean():.2f}% (±{alg_data['encrypt_cpu_mean'].std():.2f})
   - Memória média: {alg_data['encrypt_memory_mean'].mean():.2f}MB (±{alg_data['encrypt_memory_mean'].std():.2f})
   - Throughput médio: {alg_data['throughput_encrypt'].mean():.2f}MB/s (±{alg_data['throughput_encrypt'].std():.2f})
"""
        
        # Salvar relatório
        with open(f'{self.output_dir}/statistical_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(stats_report)
        
        return stats_report
    
    def create_heatmap_correlation(self):
        """Cria heatmap de correlação entre métricas"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Selecionar colunas numéricas para correlação
        numeric_cols = ['encrypt_time_mean', 'decrypt_time_mean', 'encrypt_cpu_mean', 
                       'decrypt_cpu_mean', 'encrypt_memory_mean', 'decrypt_memory_mean',
                       'throughput_encrypt', 'throughput_decrypt', 'data_size', 'key_size']
        
        correlation_matrix = self.df[numeric_cols].corr()
        
        # Criar heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, ax=ax, fmt='.3f')
        ax.set_title('Matriz de Correlação entre Métricas de Performance', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_summary_table(self):
        """Gera tabela resumo dos resultados"""
        summary = self.df.groupby(['algorithm', 'key_size']).agg({
            'encrypt_time_mean': ['mean', 'std'],
            'encrypt_cpu_mean': ['mean', 'std'],
            'encrypt_memory_mean': ['mean', 'std'],
            'throughput_encrypt': ['mean', 'std']
        }).round(6)
        
        # Salvar tabela
        summary.to_csv(f'{self.output_dir}/summary_table.csv')
        
        return summary
    
    def run_complete_analysis(self):
        """Executa análise completa"""
        print("Gerando análises e gráficos...")
        
        self.create_performance_comparison()
        print("✓ Gráficos de comparação de performance")
        
        self.create_throughput_analysis()
        print("✓ Análise de throughput")
        
        self.create_scalability_analysis()
        print("✓ Análise de escalabilidade")
        
        self.create_heatmap_correlation()
        print("✓ Heatmap de correlação")
        
        stats_report = self.create_statistical_analysis()
        print("✓ Análise estatística")
        
        summary = self.generate_summary_table()
        print("✓ Tabela resumo")
        
        print(f"\nTodos os gráficos e análises foram salvos em '{self.output_dir}/'")
        
        return {
            'statistical_report': stats_report,
            'summary_table': summary
        }

def main():
    # Carregar resultados
    try:
        df = pd.read_csv('data/benchmark_results.csv')
        print(f"Carregados {len(df)} resultados do benchmark")
    except FileNotFoundError:
        print("Arquivo 'data/benchmark_results.csv' não encontrado. Execute primeiro o benchmark.")
        return
    
    # Executar análise
    analysis = CryptoAnalysis(df)
    results = analysis.run_complete_analysis()
    
    return results

if __name__ == "__main__":
    main()
