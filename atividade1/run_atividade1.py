#!/usr/bin/env python3
"""
ATIVIDADE 1: Análise de Desempenho de Algoritmos de Criptografia Simétrica
Executa benchmark e análises dos algoritmos AES, Blowfish e Twofish
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import time

def print_header():
    print("="*70)
    print("ATIVIDADE 1: ANÁLISE DE ALGORITMOS DE CRIPTOGRAFIA SIMÉTRICA")
    print("Algoritmos: AES, Blowfish, Twofish")
    print("="*70)
    print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

def run_atividade1():
    print_header()
    
    try:
        # Executar benchmark
        print("1. Executando benchmark dos algoritmos...")
        from atividade1.src.crypto_benchmark import main as benchmark_main
        
        start_time = time.time()
        results_df = benchmark_main()
        end_time = time.time()
        
        print(f"✓ Benchmark concluído em {end_time - start_time:.2f} segundos")
        
        # Executar análises
        print("\n2. Gerando análises e gráficos...")
        from atividade1.src.analysis import main as analysis_main
        
        start_time = time.time()
        analysis_results = analysis_main()
        end_time = time.time()
        
        print(f"✓ Análises concluídas em {end_time - start_time:.2f} segundos")
        
        print("\n" + "="*70)
        print("ATIVIDADE 1 CONCLUÍDA COM SUCESSO!")
        print("="*70)
        
        print("\nArquivos gerados:")
        print("- atividade1/data/benchmark_results.csv")
        print("- atividade1/results/performance_comparison.png")
        print("- atividade1/results/throughput_analysis.png")
        print("- atividade1/results/scalability_analysis.png")
        print("- atividade1/results/correlation_heatmap.png")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro na Atividade 1: {e}")
        return False

if __name__ == "__main__":
    run_atividade1()
