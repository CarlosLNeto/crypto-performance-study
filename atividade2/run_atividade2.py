#!/usr/bin/env python3
"""
ATIVIDADE 2: Aplicação de Assinatura Digital
Desenvolve aplicação de envio de mensagens com certificados ad-hoc
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import time

def print_header():
    print("="*70)
    print("ATIVIDADE 2: APLICAÇÃO DE ASSINATURA DIGITAL")
    print("Certificados ad-hoc e verificação de integridade")
    print("="*70)
    print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

def run_atividade2():
    print_header()
    
    try:
        # Executar demonstração
        print("1. Executando demonstração da aplicação...")
        from atividade2.src.digital_signature_app import demonstrate_digital_signature
        
        start_time = time.time()
        demo_results = demonstrate_digital_signature()
        end_time = time.time()
        
        print(f"✓ Demonstração concluída em {end_time - start_time:.2f} segundos")
        
        # Executar análise de performance
        print("\n2. Analisando performance das operações...")
        from atividade2.src.signature_analysis import main as analysis_main
        
        start_time = time.time()
        perf_results = analysis_main()
        end_time = time.time()
        
        print(f"✓ Análise concluída em {end_time - start_time:.2f} segundos")
        
        print("\n" + "="*70)
        print("ATIVIDADE 2 CONCLUÍDA COM SUCESSO!")
        print("="*70)
        
        print("\nArquivos gerados:")
        print("- atividade2/certificates/ (certificados digitais)")
        print("- atividade2/messages/ (mensagens assinadas)")
        print("- atividade2/data/signature_performance_results.csv")
        print("- atividade2/results/signature_performance_analysis.png")
        print("- atividade2/results/signature_operations_comparison.png")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro na Atividade 2: {e}")
        return False

if __name__ == "__main__":
    run_atividade2()
