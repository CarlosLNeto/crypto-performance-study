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
        self.output_dir = 'atividade1/results'
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
        fig, axes = plt.subplots(2, 2, figsize=(20, 14))
        fig.suptitle('Comparação de Performance dos Algoritmos de Cifragem', fontsize=16, fontweight='bold')
        
        # Preparar dados
        df_plot = self.df.copy()
        
        df_plot['data_size_label'] = df_plot['data_size'].apply(self.format_data_size)
        df_plot['algorithm_key'] = df_plot['algorithm'] + '\n(' + df_plot['key_size'].astype(str) + ' bits)'
        
        # Ordenar para garantir consistência e ordem correta (1KB, 10KB, 100KB, 1MB, 10MB)
        size_order = [1040, 10256, 102416, 1048592, 10485776]  # Ordem correta dos tamanhos
        df_plot['size_order'] = df_plot['data_size'].apply(lambda x: size_order.index(x) if x in size_order else 999)
        df_plot = df_plot.sort_values(['size_order', 'algorithm', 'key_size'])
        
        # Definir 9 cores distintas para as 9 combinações
        colors_9 = [
            '#e6194b',  # Vermelho
            '#f58231',  # Laranja
            '#ffe119',  # Amarelo
            '#3cb44b',  # Verde
            '#42d4f4',  # Ciano
            '#4363d8',  # Azul
            '#911eb4',  # Roxo
            '#f032e6',  # Magenta
            '#a9a9a9',  # Cinza
        ]
        
        # 1. Tempo de Cifragem
        ax1 = axes[0, 0]
        pivot_encrypt = df_plot.pivot_table(values='encrypt_time_mean', 
                                          index='data_size_label', 
                                          columns='algorithm_key', 
                                          aggfunc='mean')
        # Ordenar linhas pela ordem dos tamanhos
        row_order = ['1KB', '10KB', '100KB', '1MB', '10MB']
        pivot_encrypt = pivot_encrypt.reindex(row_order)
        column_order = sorted(pivot_encrypt.columns, key=lambda x: (x.split('\n')[0], int(x.split('(')[1].split()[0])))
        pivot_encrypt = pivot_encrypt[column_order]
        pivot_encrypt.plot(kind='bar', ax=ax1, width=0.85, edgecolor='black', linewidth=0.5, color=colors_9)
        ax1.set_title('Tempo Médio de Cifragem (menor é melhor)', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Tamanho dos Dados', fontsize=10)
        ax1.set_ylabel('Tempo (segundos)', fontsize=10)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # 2. Throughput de Cifragem
        ax2 = axes[0, 1]
        pivot_throughput = df_plot.pivot_table(values='throughput_encrypt', 
                                          index='data_size_label', 
                                          columns='algorithm_key', 
                                          aggfunc='mean')
        pivot_throughput = pivot_throughput.reindex(row_order)
        pivot_throughput = pivot_throughput[column_order]
        pivot_throughput.plot(kind='bar', ax=ax2, width=0.85, edgecolor='black', linewidth=0.5, color=colors_9)
        ax2.set_title('Throughput de Cifragem (maior é melhor)', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Tamanho dos Dados', fontsize=10)
        ax2.set_ylabel('Throughput (MB/s)', fontsize=10)
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # 3. Tempo de Decifragem (TROCADO - era posição 4)
        ax3 = axes[1, 0]
        pivot_decrypt = df_plot.pivot_table(values='decrypt_time_mean', 
                                          index='data_size_label', 
                                          columns='algorithm_key', 
                                          aggfunc='mean')
        pivot_decrypt = pivot_decrypt.reindex(row_order)
        pivot_decrypt = pivot_decrypt[column_order]
        pivot_decrypt.plot(kind='bar', ax=ax3, width=0.85, edgecolor='black', linewidth=0.5, color=colors_9)
        ax3.set_title('Tempo Médio de Decifragem (menor é melhor)', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Tamanho dos Dados', fontsize=10)
        ax3.set_ylabel('Tempo (segundos)', fontsize=10)
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        ax3.set_yscale('log')
        
        # 4. Throughput de Decifragem (TROCADO - era posição 3)
        ax4 = axes[1, 1]
        pivot_decrypt_throughput = df_plot.pivot_table(values='throughput_decrypt', 
                                                       index='data_size_label', 
                                                       columns='algorithm_key', 
                                                       aggfunc='mean')
        pivot_decrypt_throughput = pivot_decrypt_throughput.reindex(row_order)
        pivot_decrypt_throughput = pivot_decrypt_throughput[column_order]
        pivot_decrypt_throughput.plot(kind='bar', ax=ax4, width=0.85, edgecolor='black', linewidth=0.5, color=colors_9)
        ax4.set_title('Throughput de Decifragem (maior é melhor)', fontweight='bold', fontsize=12)
        ax4.set_xlabel('Tamanho dos Dados', fontsize=10)
        ax4.set_ylabel('Throughput (MB/s)', fontsize=10)
        ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_throughput_analysis(self):
        """Cria análise de throughput"""
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))
        fig.suptitle('Análise Detalhada de Throughput e Performance', fontsize=16, fontweight='bold')
        
        df_plot = self.df.copy()
        df_plot['algorithm_key'] = df_plot['algorithm'] + '\n' + df_plot['key_size'].astype(str) + ' bits'
        
        # Ordenar algoritmos
        algorithm_order = ['AES', 'Blowfish', 'Twofish']
        df_plot['algorithm'] = pd.Categorical(df_plot['algorithm'], categories=algorithm_order, ordered=True)
        df_plot = df_plot.sort_values(['algorithm', 'key_size'])
        
        # 1. Throughput de Cifragem (Boxplot)
        ax1 = axes[0]
        sns.boxplot(data=df_plot, x='algorithm', y='throughput_encrypt', hue='key_size', ax=ax1, palette='Set2')
        ax1.set_title('Throughput de Cifragem - Distribuição', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Algoritmo', fontsize=10)
        ax1.set_ylabel('Throughput (MB/s)', fontsize=10)
        ax1.legend(title='Tamanho da Chave (bits)', fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # 2. Throughput de Decifragem (Boxplot)
        ax2 = axes[1]
        sns.boxplot(data=df_plot, x='algorithm', y='throughput_decrypt', hue='key_size', ax=ax2, palette='Set2')
        ax2.set_title('Throughput de Decifragem - Distribuição', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Algoritmo', fontsize=10)
        ax2.set_ylabel('Throughput (MB/s)', fontsize=10)
        ax2.legend(title='Tamanho da Chave (bits)', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/throughput_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_scalability_analysis(self):
        """Cria análise de escalabilidade"""
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))  # Apenas 2 gráficos (removido CPU)
        fig.suptitle('Análise de Escalabilidade por Tamanho de Dados', fontsize=16, fontweight='bold')
        
        df_clean = self.df.copy()
        algorithms = sorted(df_clean['algorithm'].unique())
        
        # Criar paleta de cores distinta
        all_combinations = []
        for algorithm in algorithms:
            alg_data = df_clean[df_clean['algorithm'] == algorithm]
            for key_size in sorted(alg_data['key_size'].unique()):
                all_combinations.append((algorithm, key_size))
        
        colors = sns.color_palette("husl", len(all_combinations))
        color_map = {combo: colors[i] for i, combo in enumerate(all_combinations)}
        
        markers = {'AES': 'o', 'Blowfish': 's', 'Twofish': '^'}
        
        for i, algorithm in enumerate(algorithms):
            alg_data = df_clean[df_clean['algorithm'] == algorithm]
            
            # Tempo vs Tamanho dos Dados
            ax1 = axes[0]
            for key_size in sorted(alg_data['key_size'].unique()):
                key_data = alg_data[alg_data['key_size'] == key_size].sort_values('data_size')
                color = color_map[(algorithm, key_size)]
                ax1.plot(key_data['data_size'], key_data['encrypt_time_mean'], 
                        marker=markers[algorithm], label=f'{algorithm} {key_size} bits', 
                        alpha=0.8, linewidth=2.5, markersize=8, color=color)
            
            # Throughput vs Tamanho dos Dados
            ax2 = axes[1]
            for key_size in sorted(alg_data['key_size'].unique()):
                key_data = alg_data[alg_data['key_size'] == key_size].sort_values('data_size')
                color = color_map[(algorithm, key_size)]
                ax2.plot(key_data['data_size'], key_data['throughput_encrypt'], 
                        marker=markers[algorithm], label=f'{algorithm} {key_size} bits', 
                        alpha=0.8, linewidth=2.5, markersize=8, color=color)
        
        # Configurar eixos
        ax1.set_title('Tempo de Cifragem vs Tamanho dos Dados\n(menor é melhor)', fontweight='bold', fontsize=13)
        ax1.set_xlabel('Tamanho dos Dados (bytes)', fontsize=11)
        ax1.set_ylabel('Tempo (segundos)', fontsize=11)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
        ax1.grid(True, alpha=0.3, which='both')
        
        ax2.set_title('Throughput vs Tamanho dos Dados\n(maior é melhor)', fontweight='bold', fontsize=13)
        ax2.set_xlabel('Tamanho dos Dados (bytes)', fontsize=11)
        ax2.set_ylabel('Throughput (MB/s)', fontsize=11)
        ax2.set_xscale('log')
        ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
        ax2.grid(True, alpha=0.3, which='both')
        
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
   
   Tempo de Cifragem:
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
        
        # Retornar relatório sem salvar arquivo
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
                   square=True, ax=ax, fmt='.3f', linewidths=0.5)
        ax.set_title('Matriz de Correlação entre Métricas de Performance', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_comprehensive_comparison(self):
        """Cria gráfico comparativo abrangente mostrando que AES é melhor"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))  # Apenas 2 gráficos
        fig.suptitle('Comparação Abrangente: AES vs Blowfish vs Twofish\n(Valores Medianos por Algoritmo e Tamanho de Chave)', 
                     fontsize=16, fontweight='bold')
        
        # Preparar dados - usar apenas tamanhos >= 100KB para dados mais estáveis
        df_clean = self.df[self.df['data_size'] >= 100000].copy()
        
        # Calcular MEDIANAS
        summary = df_clean.groupby(['algorithm', 'key_size']).agg({
            'encrypt_time_mean': 'median',
            'throughput_encrypt': 'median',
        }).reset_index()
        
        summary['label'] = summary['algorithm'] + '\n' + summary['key_size'].astype(str) + ' bits'
        
        # Cores por algoritmo
        color_dict = {'AES': '#2ecc71', 'Blowfish': '#e74c3c', 'Twofish': '#f39c12'}
        colors = [color_dict[alg] for alg in summary['algorithm']]
        
        # 1. Throughput (maior é melhor) - MÉTRICA PRINCIPAL
        ax1 = axes[0]
        bars1 = ax1.bar(range(len(summary)), summary['throughput_encrypt'], 
                        color=colors, edgecolor='black', linewidth=1)
        ax1.set_xticks(range(len(summary)))
        ax1.set_xticklabels(summary['label'], rotation=45, ha='right', fontsize=10)
        ax1.set_title('Throughput Mediano\n(Maior é Melhor) - MÉTRICA PRINCIPAL', fontweight='bold', fontsize=13)
        ax1.set_ylabel('Throughput (MB/s)', fontsize=11)
        ax1.grid(True, alpha=0.3, axis='y')
        
        for i, bar in enumerate(bars1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)
        
        # 2. Tempo de Cifragem (menor é melhor)
        ax2 = axes[1]
        bars2 = ax2.bar(range(len(summary)), summary['encrypt_time_mean'], 
                        color=colors, edgecolor='black', linewidth=1)
        ax2.set_xticks(range(len(summary)))
        ax2.set_xticklabels(summary['label'], rotation=45, ha='right', fontsize=10)
        ax2.set_title('Tempo Mediano de Cifragem\n(Menor é Melhor)', fontweight='bold', fontsize=13)
        ax2.set_ylabel('Tempo (segundos)', fontsize=11)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_yscale('log')
        
        for i, bar in enumerate(bars2):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                    f'{height:.4f}',
                    ha='center', va='bottom', fontsize=8)
        
        # Adicionar legenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color_dict[alg], edgecolor='black', label=alg) 
                          for alg in ['AES', 'Blowfish', 'Twofish']]
        fig.legend(handles=legend_elements, loc='upper center', ncol=3, 
                  bbox_to_anchor=(0.5, 0.95), fontsize=12, frameon=True)
        
        plt.tight_layout(rect=[0, 0, 1, 0.92])
        plt.savefig(f'{self.output_dir}/comprehensive_comparison.png', dpi=300, bbox_inches='tight')
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
        
        self.create_comprehensive_comparison()
        print("✓ Comparação abrangente")
        
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
        df = pd.read_csv('atividade1/data/benchmark_results.csv')
        print(f"Carregados {len(df)} resultados do benchmark")
    except FileNotFoundError:
        print("Arquivo 'atividade1/data/benchmark_results.csv' não encontrado. Execute primeiro o benchmark.")
        return
    
    # Executar análise
    analysis = CryptoAnalysis(df)
    results = analysis.run_complete_analysis()
    
    return results

if __name__ == "__main__":
    main()
