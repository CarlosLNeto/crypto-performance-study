#!/usr/bin/env python3
"""
Script Principal - Estudo Completo Integrado
Executa ambas as partes: análise de algoritmos + aplicação de assinatura digital
"""

import sys
import os
import time
from datetime import datetime

def print_header():
    """Imprime cabeçalho do estudo completo"""
    print("="*80)
    print("ESTUDO COMPLETO DE CRIPTOGRAFIA APLICADA")
    print("Parte I: Análise de Algoritmos Simétricos")
    print("Parte II: Aplicação de Assinatura Digital")
    print("="*80)
    print(f"Início do estudo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("Verificando dependências...")
    
    required_packages = [
        'cryptography', 'Crypto', 'matplotlib', 'seaborn', 
        'pandas', 'numpy', 'psutil', 'scipy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - NÃO ENCONTRADO")
    
    if missing_packages:
        print(f"\nPacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✓ Todas as dependências estão instaladas\n")
    return True

def run_part1_symmetric_analysis():
    """Executa Parte I: Análise de algoritmos simétricos"""
    print("PARTE I: ANÁLISE DE ALGORITMOS SIMÉTRICOS")
    print("="*50)
    
    try:
        # Benchmark de algoritmos
        print("1. Executando benchmark de algoritmos...")
        from src.crypto_benchmark import main as benchmark_main
        
        start_time = time.time()
        results_df = benchmark_main()
        end_time = time.time()
        
        print(f"✓ Benchmark concluído em {end_time - start_time:.2f} segundos")
        print(f"✓ {len(results_df)} testes realizados")
        
        # Análises e gráficos
        print("\n2. Gerando análises e gráficos...")
        from src.analysis import main as analysis_main
        
        start_time = time.time()
        analysis_results = analysis_main()
        end_time = time.time()
        
        print(f"✓ Análises concluídas em {end_time - start_time:.2f} segundos")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro na Parte I: {e}")
        return False

def run_part2_digital_signature():
    """Executa Parte II: Aplicação de assinatura digital"""
    print("\nPARTE II: APLICAÇÃO DE ASSINATURA DIGITAL")
    print("="*50)
    
    try:
        # Demonstração da aplicação
        print("1. Executando demonstração da aplicação...")
        from src.digital_signature_app import demonstrate_digital_signature
        
        start_time = time.time()
        demo_results = demonstrate_digital_signature()
        end_time = time.time()
        
        print(f"✓ Demonstração concluída em {end_time - start_time:.2f} segundos")
        
        # Análise de performance
        print("\n2. Analisando performance das operações...")
        from src.signature_analysis import main as signature_analysis_main
        
        start_time = time.time()
        perf_results = signature_analysis_main()
        end_time = time.time()
        
        print(f"✓ Análise de performance concluída em {end_time - start_time:.2f} segundos")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro na Parte II: {e}")
        return False

def show_results_summary():
    """Mostra resumo dos resultados gerados"""
    print("\nRESULTADOS GERADOS:")
    print("="*50)
    
    files_to_check = [
        # Parte I - Algoritmos Simétricos
        ('data/benchmark_results.csv', 'Dados de benchmark - algoritmos simétricos'),
        ('results/graficos/performance_comparison.png', 'Comparação de performance'),
        ('results/graficos/throughput_analysis.png', 'Análise de throughput'),
        ('results/graficos/scalability_analysis.png', 'Análise de escalabilidade'),
        ('results/graficos/correlation_heatmap.png', 'Heatmap de correlação'),
        ('results/graficos/summary_table.csv', 'Tabela resumo - simétricos'),
        
        # Parte II - Assinatura Digital
        ('data/signature_performance_results.csv', 'Dados de performance - assinatura digital'),
        ('results/graficos/signature_performance_analysis.png', 'Performance - assinatura digital'),
        ('results/graficos/signature_operations_comparison.png', 'Comparação - operações de assinatura'),
        ('certificates/', 'Certificados digitais gerados'),
        ('messages/', 'Mensagens assinadas'),
        
        # Documentação
        ('docs/relatorio_latex_abnt.tex', 'Relatório técnico integrado (LaTeX)')
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            if os.path.isdir(filename):
                count = len([f for f in os.listdir(filename) if os.path.isfile(os.path.join(filename, f))])
                print(f"✓ {filename} ({count} arquivos) - {description}")
            else:
                size = os.path.getsize(filename)
                print(f"✓ {filename} ({size:,} bytes) - {description}")
        else:
            print(f"✗ {filename} - NÃO ENCONTRADO")

def main():
    """Função principal"""
    print_header()
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Executar Parte I
    if not run_part1_symmetric_analysis():
        print("Falha na Parte I. Continuando com Parte II...")
    
    # Executar Parte II
    if not run_part2_digital_signature():
        print("Falha na Parte II.")
    
    # Mostrar resumo
    show_results_summary()
    
    print("\n" + "="*80)
    print("ESTUDO COMPLETO CONCLUÍDO!")
    print(f"Término: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80)
    
    print("\nPróximos passos:")
    print("1. Compile o relatório LaTeX integrado: docs/relatorio_latex_abnt.tex")
    print("2. Examine todos os gráficos na pasta: results/graficos/")
    print("3. Analise os dados de ambas as partes: data/")
    print("4. Verifique os certificados e mensagens geradas")
    print("5. Use todas as imagens PNG no Overleaf junto com o LaTeX")

if __name__ == "__main__":
    main()
