#!/usr/bin/env python3
"""
Script Principal - Estudo Completo de Desempenho de Algoritmos de Criptografia
Executa benchmark, análises e gera relatório final
"""

import sys
import os
import time
from datetime import datetime

def print_header():
    """Imprime cabeçalho do estudo"""
    print("="*80)
    print("ESTUDO DE DESEMPENHO COMPUTACIONAL DE ALGORITMOS DE CRIPTOGRAFIA")
    print("Algoritmos: AES, Blowfish, Twofish")
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

def run_benchmark():
    """Executa o benchmark dos algoritmos"""
    print("FASE 1: EXECUTANDO BENCHMARK")
    print("-" * 40)
    
    try:
        from crypto_benchmark import main as benchmark_main
        
        start_time = time.time()
        results_df = benchmark_main()
        end_time = time.time()
        
        print(f"✓ Benchmark concluído em {end_time - start_time:.2f} segundos")
        print(f"✓ {len(results_df)} testes realizados")
        return True
        
    except Exception as e:
        print(f"✗ Erro no benchmark: {e}")
        return False

def run_analysis():
    """Executa as análises e gera gráficos"""
    print("\nFASE 2: EXECUTANDO ANÁLISES")
    print("-" * 40)
    
    try:
        from analysis import main as analysis_main
        
        start_time = time.time()
        analysis_results = analysis_main()
        end_time = time.time()
        
        print(f"✓ Análises concluídas em {end_time - start_time:.2f} segundos")
        return True
        
    except Exception as e:
        print(f"✗ Erro na análise: {e}")
        return False

def generate_report():
    """Gera o relatório final"""
    print("\nFASE 3: GERANDO RELATÓRIO")
    print("-" * 40)
    
    try:
        from report_generator import main as report_main
        
        start_time = time.time()
        report_main()
        end_time = time.time()
        
        print(f"✓ Relatório gerado em {end_time - start_time:.2f} segundos")
        return True
        
    except Exception as e:
        print(f"✗ Erro na geração do relatório: {e}")
        return False

def show_results_summary():
    """Mostra resumo dos resultados gerados"""
    print("\nRESULTADOS GERADOS:")
    print("-" * 40)
    
    files_to_check = [
        ('benchmark_results.csv', 'Dados brutos do benchmark'),
        ('graficos/performance_comparison.png', 'Gráficos de comparação de performance'),
        ('graficos/throughput_analysis.png', 'Análise de throughput'),
        ('graficos/scalability_analysis.png', 'Análise de escalabilidade'),
        ('graficos/correlation_heatmap.png', 'Heatmap de correlação'),
        ('graficos/statistical_analysis.txt', 'Análise estatística detalhada'),
        ('graficos/summary_table.csv', 'Tabela resumo'),
        ('relatorio_tecnico_abnt.txt', 'Relatório técnico completo (ABNT)')
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
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
    
    # Executar benchmark
    if not run_benchmark():
        print("Falha no benchmark. Abortando estudo.")
        sys.exit(1)
    
    # Executar análises
    if not run_analysis():
        print("Falha na análise. Abortando estudo.")
        sys.exit(1)
    
    # Gerar relatório
    if not generate_report():
        print("Falha na geração do relatório. Abortando estudo.")
        sys.exit(1)
    
    # Mostrar resumo
    show_results_summary()
    
    print("\n" + "="*80)
    print("ESTUDO CONCLUÍDO COM SUCESSO!")
    print(f"Término: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80)
    
    print("\nPróximos passos:")
    print("1. Revise o relatório técnico: relatorio_tecnico_abnt.txt")
    print("2. Examine os gráficos na pasta: graficos/")
    print("3. Analise os dados brutos: benchmark_results.csv")
    print("4. Consulte a análise estatística: graficos/statistical_analysis.txt")

if __name__ == "__main__":
    main()
