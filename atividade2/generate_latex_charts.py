#!/usr/bin/env python3
"""
Gerador de Gráficos das Métricas Reais do Chat para LaTeX
Baseado exclusivamente em dados coletados durante uso real do chat
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_chat_metrics_charts():
    """Gera gráficos das métricas reais coletadas durante uso do chat"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verificar se existem dados reais do chat
    if not os.path.exists('data/real_chat_metrics.csv'):
        print("❌ Dados reais do chat não encontrados!")
        print("💡 Execute primeiro:")
        print("   1. python run_chat.py")
        print("   2. Envie algumas mensagens no chat")
        print("   3. Pare o chat (Ctrl+C)")
        print("   4. Execute este script novamente")
        return
    
    # Carregar dados reais
    df = pd.read_csv('data/real_chat_metrics.csv')
    
    if df.empty:
        print("❌ Arquivo de métricas está vazio!")
        return
    
    print(f"📊 Gerando gráficos com {len(df)} métricas reais do chat...")
    
    # Preparar dados de tempo
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['time_from_start'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
    
    # Configurar estilo para LaTeX
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'serif',
        'figure.figsize': (12, 10),
        'axes.grid': True,
        'grid.alpha': 0.3
    })
    
    sign_data = df[df['operation'] == 'sign']
    verify_data = df[df['operation'] == 'verify']
    
    # 1. Gráfico Principal (4 subgráficos)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Timeline de uso
    
    if not sign_data.empty:
        axes[0,0].scatter(sign_data['time_from_start'], sign_data['time'] * 1000, 
                         alpha=0.7, s=60, c='blue', label='Assinatura')
    if not verify_data.empty:
        axes[0,0].scatter(verify_data['time_from_start'], verify_data['time'] * 1000, 
                         alpha=0.7, s=60, c='red', label='Verificação')
    axes[0,0].set_xlabel('Tempo (s)')
    axes[0,0].set_ylabel('Tempo (ms)')
    axes[0,0].set_title('Timeline de Uso Real do Chat')
    axes[0,0].legend()
    
    # Performance por usuário
    if 'username' in df.columns and len(df['username'].unique()) > 1:
        user_stats = df.groupby(['username', 'operation'])['time'].mean().unstack(fill_value=0) * 1000
        user_stats.plot(kind='bar', ax=axes[0,1], alpha=0.8)
        axes[0,1].set_title('Performance por Usuário')
        axes[0,1].set_ylabel('Tempo Médio (ms)')
        axes[0,1].tick_params(axis='x', rotation=45)
    
    # Distribuição de tempos
    if not sign_data.empty:
        axes[1,0].hist(sign_data['time'] * 1000, bins=20, alpha=0.7, 
                      color='lightblue', edgecolor='navy', label='Assinatura')
    if not verify_data.empty:
        axes[1,0].hist(verify_data['time'] * 1000, bins=20, alpha=0.7, 
                      color='lightcoral', edgecolor='darkred', label='Verificação')
    axes[1,0].set_xlabel('Tempo (ms)')
    axes[1,0].set_ylabel('Frequência')
    axes[1,0].set_title('Distribuição de Tempos')
    axes[1,0].legend()
    
    # Tamanhos de mensagem
    if not sign_data.empty:
        axes[1,1].scatter(sign_data['message_size'], sign_data['time'] * 1000, 
                         alpha=0.7, c='green')
        axes[1,1].set_xlabel('Tamanho da Mensagem')
        axes[1,1].set_ylabel('Tempo de Assinatura (ms)')
        axes[1,1].set_title('Tempo vs Tamanho da Mensagem')
    
    plt.tight_layout()
    plt.savefig('results/chat_performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Gráfico de Comparação
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Box plot
    if not sign_data.empty and not verify_data.empty:
        data = [sign_data['time'] * 1000, verify_data['time'] * 1000]
        bp = axes[0].boxplot(data, labels=['Assinatura', 'Verificação'], patch_artist=True)
        bp['boxes'][0].set_facecolor('lightblue')
        bp['boxes'][1].set_facecolor('lightgreen')
        axes[0].set_ylabel('Tempo (ms)')
        axes[0].set_title('Comparação de Operações')
        axes[0].set_yscale('log')
    
    # Estatísticas
    operations = ['Assinatura', 'Verificação']
    means = [sign_data['time'].mean() * 1000 if not sign_data.empty else 0,
             verify_data['time'].mean() * 1000 if not verify_data.empty else 0]
    
    bars = axes[1].bar(operations, means, alpha=0.8, 
                      color=['skyblue', 'lightgreen'], edgecolor='black')
    axes[1].set_ylabel('Tempo Médio (ms)')
    axes[1].set_title('Performance Média')
    
    # Adicionar valores nas barras
    for bar, mean_val in zip(bars, means):
        if mean_val > 0:
            axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                        f'{mean_val:.2f}ms', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('results/chat_operations_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Gráficos para LaTeX
    create_latex_charts(df)
    
    # 4. Tabela LaTeX
    create_latex_table(df)
    
    print("✅ Gráficos das métricas reais gerados!")
    print("📊 Arquivos criados:")
    print("   - results/chat_performance_analysis.png")
    print("   - results/chat_operations_comparison.png") 
    print("   - results/chat_metrics_latex.png")
    print("   - results/chat_statistics_latex.png")
    print("   - results/chat_metrics_table_latex.tex")

def create_latex_charts(df):
    """Cria gráficos otimizados para LaTeX"""
    sign_data = df[df['operation'] == 'sign']
    verify_data = df[df['operation'] == 'verify']
    
    # Gráfico de métricas para LaTeX
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Repetir os gráficos principais com estilo LaTeX
    # (timestamp já foi processado na função principal)
    
    if not sign_data.empty:
        axes[0,0].plot(sign_data['time_from_start'], sign_data['time'] * 1000, 
                      'o-', markersize=6, linewidth=2, label='Assinatura')
    if not verify_data.empty:
        axes[0,0].plot(verify_data['time_from_start'], verify_data['time'] * 1000, 
                      's-', markersize=6, linewidth=2, label='Verificação')
    axes[0,0].set_title('Timeline do Chat Real')
    axes[0,0].legend()
    
    # Outros gráficos similares...
    plt.tight_layout()
    plt.savefig('results/chat_metrics_latex.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráfico de estatísticas
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    operations = ['Assinatura', 'Verificação']
    means = [sign_data['time'].mean() * 1000 if not sign_data.empty else 0,
             verify_data['time'].mean() * 1000 if not verify_data.empty else 0]
    
    axes[0].bar(operations, means, alpha=0.8, color=['blue', 'red'])
    axes[0].set_title('Tempos Médios Reais')
    axes[0].set_ylabel('Tempo (ms)')
    
    plt.tight_layout()
    plt.savefig('results/chat_statistics_latex.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_latex_table(df):
    """Cria tabela LaTeX com métricas reais"""
    sign_data = df[df['operation'] == 'sign']
    verify_data = df[df['operation'] == 'verify']
    
    latex_code = """\\begin{table}[h]
\\centering
\\caption{Métricas Reais do Sistema de Chat com Assinatura Digital}
\\label{tab:real_chat_metrics}
\\begin{tabular}{|l|c|c|c|}
\\hline
\\textbf{Operação} & \\textbf{Tempo Médio} & \\textbf{Desvio Padrão} & \\textbf{Total} \\\\
& \\textbf{(ms)} & \\textbf{(ms)} & \\textbf{Operações} \\\\
\\hline
"""
    
    if not sign_data.empty:
        latex_code += f"Assinatura & {sign_data['time'].mean()*1000:.2f} & {sign_data['time'].std()*1000:.2f} & {len(sign_data)} \\\\\n"
    
    if not verify_data.empty:
        latex_code += f"Verificação & {verify_data['time'].mean()*1000:.2f} & {verify_data['time'].std()*1000:.2f} & {len(verify_data)} \\\\\n"
    
    latex_code += """\\hline
\\end{tabular}
\\end{table}"""
    
    with open('results/chat_metrics_table_latex.tex', 'w') as f:
        f.write(latex_code)

if __name__ == '__main__':
    print("🔬 Gerador de Gráficos das Métricas Reais do Chat")
    print("=" * 50)
    
    os.makedirs('results', exist_ok=True)
    generate_chat_metrics_charts()
