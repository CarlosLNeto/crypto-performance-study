#!/usr/bin/env python3
"""
Gerador de Gráficos das 3 Camadas de Segurança
Demonstra: Sigilo (AES), Integridade (SHA-256), Autenticidade (RSA)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def create_security_architecture_diagram():
    """Cria diagrama vertical simplificado da arquitetura de segurança"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Título
    fig.suptitle('Arquitetura de Segurança - Atividade 2\nTripla Camada de Proteção', 
                 fontsize=16, fontweight='bold', y=0.96)
    
    # Cores para cada camada
    color_sigilo = '#3498db'      # Azul
    color_integridade = '#2ecc71' # Verde
    color_autenticidade = '#e74c3c' # Vermelho
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Layout vertical centralizado
    x_center = 5
    box_width = 6
    box_height = 1.8  # Aumentado para acomodar linha de chave
    y_spacing = 1.2
    
    # MENSAGEM ORIGINAL (topo)
    y_pos = 10.5
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=2, edgecolor='black', 
                                  facecolor='white')
    ax.add_patch(rect)
    ax.text(x_center, y_pos, 'MENSAGEM ORIGINAL', fontsize=12, ha='center', 
            fontweight='bold')
    ax.text(x_center, y_pos - 0.4, '"Olá, mundo!"', fontsize=10, ha='center', 
            style='italic')
    
    # SETA 1
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # CAMADA 1: INTEGRIDADE
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=3, edgecolor=color_integridade, 
                                  facecolor=color_integridade, alpha=0.2)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.35, '1. INTEGRIDADE', fontsize=11, ha='center', 
            fontweight='bold', color=color_integridade)
    ax.text(x_center, y_pos - 0.0, 'Hash SHA-256', fontsize=10, ha='center')
    ax.text(x_center, y_pos - 0.35, 'Detecta alterações', fontsize=9, ha='center', 
            style='italic')
    ax.text(x_center, y_pos - 0.6, '► Sem chave', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # SETA 2
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # CAMADA 2: SIGILO
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=3, edgecolor=color_sigilo, 
                                  facecolor=color_sigilo, alpha=0.2)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.35, '2. SIGILO', fontsize=11, ha='center', 
            fontweight='bold', color=color_sigilo)
    ax.text(x_center, y_pos - 0.0, 'Cifragem AES-256', fontsize=10, ha='center')
    ax.text(x_center, y_pos - 0.35, 'Protege conteúdo', fontsize=9, ha='center', 
            style='italic')
    ax.text(x_center, y_pos - 0.6, '► Chave Simétrica (256 bits)', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # SETA 3
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # CAMADA 3: AUTENTICIDADE
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=3, edgecolor=color_autenticidade, 
                                  facecolor=color_autenticidade, alpha=0.2)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.35, '3. AUTENTICIDADE', fontsize=11, ha='center', 
            fontweight='bold', color=color_autenticidade)
    ax.text(x_center, y_pos - 0.0, 'Assinatura RSA-2048', fontsize=10, ha='center')
    ax.text(x_center, y_pos - 0.35, 'Prova identidade', fontsize=9, ha='center', 
            style='italic')
    ax.text(x_center, y_pos - 0.6, '► Chave Privada do Remetente', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # SETA 4
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # MENSAGEM PROTEGIDA (base)
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=2, edgecolor='black', 
                                  facecolor='gold', alpha=0.3)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.2, 'MENSAGEM PROTEGIDA', fontsize=12, ha='center', 
            fontweight='bold')
    ax.text(x_center, y_pos - 0.3, 'Cifrada + Hash + Assinatura', fontsize=10, 
            ha='center', style='italic')
    
    plt.tight_layout()
    
    # Salvar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    output_path = os.path.join(results_dir, 'security_architecture.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Diagrama de arquitetura salvo: {output_path}")
    plt.close()

def create_security_layers_comparison():
    """Cria gráfico comparativo das operações por camada de segurança"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Comparação de Performance por Camada de Segurança', 
                 fontsize=14, fontweight='bold')
    
    # Dados simulados (serão substituídos por dados reais)
    layers = ['Hash\nSHA-256\n(Integridade)', 'AES-256\nCifragem\n(Sigilo)', 
              'AES-256\nDecifragem\n(Sigilo)', 'RSA-2048\nAssinatura\n(Autenticidade)', 
              'RSA-2048\nVerificação\n(Autenticidade)']
    
    times = [0.0001, 0.002, 0.002, 0.005, 0.003]  # ms
    colors = ['#2ecc71', '#3498db', '#3498db', '#e74c3c', '#e74c3c']
    
    # Gráfico 1: Tempo de Operação
    bars1 = ax1.bar(range(len(layers)), [t*1000 for t in times], color=colors, 
                    edgecolor='black', linewidth=1.5, alpha=0.7)
    ax1.set_xticks(range(len(layers)))
    ax1.set_xticklabels(layers, fontsize=9, rotation=0)
    ax1.set_ylabel('Tempo (milissegundos)', fontsize=11, fontweight='bold')
    ax1.set_title('Tempo Médio de Processamento', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}ms',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Gráfico 2: Overhead Acumulado
    cumulative_time = np.cumsum(times) * 1000
    operations = ['1. Hash', '2. +AES Cifrar', '3. +RSA Assinar', 
                  '4. +RSA Verificar', '5. +AES Decifrar']
    
    bars2 = ax2.bar(range(len(operations)), cumulative_time[:5], 
                    color=['#2ecc71', '#3498db', '#e74c3c', '#e74c3c', '#3498db'],
                    edgecolor='black', linewidth=1.5, alpha=0.7)
    ax2.set_xticks(range(len(operations)))
    ax2.set_xticklabels(operations, fontsize=9, rotation=45, ha='right')
    ax2.set_ylabel('Tempo Acumulado (ms)', fontsize=11, fontweight='bold')
    ax2.set_title('Overhead Acumulado do Processo Completo', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}ms',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    
    # Salvar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    output_path = os.path.join(results_dir, 'security_layers_performance.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico de performance salvo: {output_path}")
    plt.close()



def create_receiver_architecture_diagram():
    """Cria diagrama vertical da arquitetura de segurança - Lado do Receptor"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Título
    fig.suptitle('Arquitetura de Segurança - Receptor\nProcesso de Verificação e Decifragem', 
                 fontsize=16, fontweight='bold', y=0.96)
    
    # Cores para cada camada
    color_sigilo = '#3498db'      # Azul
    color_integridade = '#2ecc71' # Verde
    color_autenticidade = '#e74c3c' # Vermelho
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Layout vertical centralizado
    x_center = 5
    box_width = 6
    box_height = 1.8  # Aumentado para acomodar linha de chave
    y_spacing = 1.2
    
    # MENSAGEM PROTEGIDA (topo)
    y_pos = 10.5
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=2, edgecolor='black', 
                                  facecolor='gold', alpha=0.3)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.2, 'MENSAGEM PROTEGIDA', fontsize=12, ha='center', 
            fontweight='bold')
    ax.text(x_center, y_pos - 0.3, 'Cifrada + Hash + Assinatura', fontsize=10, 
            ha='center', style='italic')
    
    # SETA 1
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # CAMADA 1: VERIFICAR AUTENTICIDADE
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=3, edgecolor=color_autenticidade, 
                                  facecolor=color_autenticidade, alpha=0.2)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.35, '1. VERIFICAR AUTENTICIDADE', fontsize=11, ha='center', 
            fontweight='bold', color=color_autenticidade)
    ax.text(x_center, y_pos - 0.0, 'Verificação RSA-2048', fontsize=10, ha='center')
    ax.text(x_center, y_pos - 0.35, 'Confirma remetente', fontsize=9, ha='center', 
            style='italic')
    ax.text(x_center, y_pos - 0.6, '► Chave Pública do Remetente', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # SETA 2
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # CAMADA 2: DECIFRAR SIGILO
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=3, edgecolor=color_sigilo, 
                                  facecolor=color_sigilo, alpha=0.2)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.35, '2. DECIFRAR SIGILO', fontsize=11, ha='center', 
            fontweight='bold', color=color_sigilo)
    ax.text(x_center, y_pos - 0.0, 'Decifragem AES-256', fontsize=10, ha='center')
    ax.text(x_center, y_pos - 0.35, 'Recupera conteúdo', fontsize=9, ha='center', 
            style='italic')
    ax.text(x_center, y_pos - 0.6, '► Chave Simétrica (256 bits)', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # SETA 3
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # CAMADA 3: VERIFICAR INTEGRIDADE
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=3, edgecolor=color_integridade, 
                                  facecolor=color_integridade, alpha=0.2)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.35, '3. VERIFICAR INTEGRIDADE', fontsize=11, ha='center', 
            fontweight='bold', color=color_integridade)
    ax.text(x_center, y_pos - 0.0, 'Comparação Hash SHA-256', fontsize=10, ha='center')
    ax.text(x_center, y_pos - 0.35, 'Confirma não-alteração', fontsize=9, ha='center', 
            style='italic')
    ax.text(x_center, y_pos - 0.6, '► Sem chave', fontsize=8, ha='center', 
            style='italic', color='gray')
    
    # SETA 4
    y_pos -= (box_height/2 + 0.3)
    ax.arrow(x_center, y_pos, 0, -0.5, head_width=0.3, head_length=0.15, 
             fc='black', ec='black', linewidth=2)
    y_pos -= 0.5
    
    # MENSAGEM ORIGINAL RECUPERADA (base)
    y_pos -= (box_height/2 + 0.3)
    rect = patches.FancyBboxPatch((x_center - box_width/2, y_pos - box_height/2), 
                                  box_width, box_height,
                                  boxstyle="round,pad=0.1", 
                                  linewidth=2, edgecolor='black', 
                                  facecolor='lightgreen', alpha=0.3)
    ax.add_patch(rect)
    ax.text(x_center, y_pos + 0.2, 'MENSAGEM ORIGINAL RECUPERADA', fontsize=12, ha='center', 
            fontweight='bold')
    ax.text(x_center, y_pos - 0.3, '"Olá, mundo!" ✓ Verificada', fontsize=10, 
            ha='center', style='italic')
    
    plt.tight_layout()
    
    # Salvar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    output_path = os.path.join(results_dir, 'security_architecture_receiver.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Diagrama de arquitetura do receptor salvo: {output_path}")
    plt.close()

def create_percentage_distribution_chart():
    """Cria gráfico de pizza 2D separado para melhor visualização"""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    fig.suptitle('Distribuição Percentual do Tempo de Processamento\npor Camada de Segurança', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # Cores consistentes
    color_sigilo = '#3498db'
    color_integridade = '#2ecc71'
    color_autenticidade = '#e74c3c'
    
    # Dados
    layers = ['Integridade\n(SHA-256)', 'Sigilo\n(AES-256)', 'Autenticidade\n(RSA-2048)']
    layer_times = [0.1, 4.0, 8.0]  # Hash, Cifrar+Decifrar, Assinar+Verificar
    layer_colors = [color_integridade, color_sigilo, color_autenticidade]
    
    total_time = sum(layer_times)
    percentages = [(t/total_time)*100 for t in layer_times]
    
    # Gráfico de pizza 2D com explosão (sem shadow para manter 2D puro)
    explode = (0.05, 0.05, 0.05)
    wedges, texts, autotexts = ax.pie(percentages, labels=layers, colors=layer_colors,
                                        autopct='%1.1f%%', startangle=90,
                                        explode=explode,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 2.5})
    
    # Ajustar tamanho do texto de porcentagem
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    # Adicionar legenda com valores absolutos
    legend_labels = [f'{layer.replace(chr(10), " ")}: {time}ms ({pct:.1f}%)' 
                    for layer, time, pct in zip(layers, layer_times, percentages)]
    ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1.0, 1.0), 
              fontsize=11, frameon=True)
    
    # Garantir aspecto circular (importante para manter 2D perfeito)
    ax.axis('equal')
    
    plt.tight_layout()
    
    # Salvar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    output_path = os.path.join(results_dir, 'percentage_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gráfico de distribuição percentual (2D) salvo: {output_path}")
    plt.close()

def create_comprehensive_security_comparison_v2():
    """Cria gráfico comparativo completo das 3 camadas de segurança - SEM pizza"""
    
    fig = plt.figure(figsize=(18, 6))
    gs = fig.add_gridspec(1, 3, hspace=0.35, wspace=0.3)
    
    fig.suptitle('Análise Comparativa das 3 Camadas de Segurança\nSigilo (AES-256) + Integridade (SHA-256) + Autenticidade (RSA-2048)', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Cores consistentes
    color_sigilo = '#3498db'
    color_integridade = '#2ecc71'
    color_autenticidade = '#e74c3c'
    
    # Dados simulados baseados em métricas típicas
    operations = ['Hash\nSHA-256', 'Cifrar\nAES-256', 'Assinar\nRSA-2048', 
                  'Verificar\nRSA-2048', 'Decifrar\nAES-256']
    times = [0.1, 2.0, 5.0, 3.0, 2.0]  # ms
    colors_ops = [color_integridade, color_sigilo, color_autenticidade, 
                  color_autenticidade, color_sigilo]
    
    # 1. Tempo por Operação
    ax1 = fig.add_subplot(gs[0])
    bars = ax1.bar(range(len(operations)), times, color=colors_ops, 
                   edgecolor='black', linewidth=2, alpha=0.7)
    ax1.set_xticks(range(len(operations)))
    ax1.set_xticklabels(operations, fontsize=10, fontweight='bold')
    ax1.set_ylabel('Tempo (ms)', fontsize=11, fontweight='bold')
    ax1.set_title('Tempo por Operação', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, time) in enumerate(zip(bars, times)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{time}ms',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 2. Distribuição por Camada
    ax2 = fig.add_subplot(gs[1])
    layers = ['Integridade\n(SHA-256)', 'Sigilo\n(AES-256)', 'Autenticidade\n(RSA-2048)']
    layer_times = [0.1, 4.0, 8.0]  # Hash, Cifrar+Decifrar, Assinar+Verificar
    layer_colors = [color_integridade, color_sigilo, color_autenticidade]
    
    bars = ax2.bar(range(len(layers)), layer_times, color=layer_colors,
                   edgecolor='black', linewidth=2, alpha=0.7)
    ax2.set_xticks(range(len(layers)))
    ax2.set_xticklabels(layers, fontsize=10, fontweight='bold')
    ax2.set_ylabel('Tempo Total (ms)', fontsize=11, fontweight='bold')
    ax2.set_title('Tempo Total por Camada de Segurança', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, time) in enumerate(zip(bars, layer_times)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{time}ms',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 3. Overhead Acumulado
    ax3 = fig.add_subplot(gs[2])
    cumulative = np.cumsum(times)
    stages = ['Hash', '+Cifrar', '+Assinar', '+Verificar', '+Decifrar']
    
    bars = ax3.bar(range(len(stages)), cumulative, color=colors_ops,
                   edgecolor='black', linewidth=2, alpha=0.7)
    ax3.set_xticks(range(len(stages)))
    ax3.set_xticklabels(stages, fontsize=10, fontweight='bold', rotation=0)
    ax3.set_ylabel('Tempo Acumulado (ms)', fontsize=11, fontweight='bold')
    ax3.set_title('Overhead Acumulado do Processo Completo', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, cum) in enumerate(zip(bars, cumulative)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{cum:.1f}ms',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    
    # Salvar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    output_path = os.path.join(results_dir, 'comprehensive_security_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Análise comparativa completa salva: {output_path}")
    plt.close()

if __name__ == '__main__':
    print("=" * 80)
    print("Gerando Gráficos da Arquitetura de Segurança - Atividade 2")
    print("=" * 80)
    print()
    
    create_security_architecture_diagram()
    create_receiver_architecture_diagram()
    create_security_layers_comparison()
    create_comprehensive_security_comparison_v2()
    create_percentage_distribution_chart()
    
    print()
    print("=" * 80)
    print("✓ Todos os gráficos foram gerados com sucesso!")
    print("=" * 80)
