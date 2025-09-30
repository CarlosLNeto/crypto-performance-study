#!/usr/bin/env python3
"""
Script para gerar PDF da apresentação HTML
Usa Chrome headless para garantir compatibilidade em macOS
"""

import os
import sys
import subprocess

def generate_pdf_with_chrome():
    """Gera PDF usando Chrome em modo headless"""
    html_file = 'apresentacao_profissional_abnt.html'
    pdf_file = 'ApresentacaoAtividade1Topicos4.pdf'
    html_path = os.path.abspath(html_file)
    pdf_path = os.path.abspath(pdf_file)

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    if not os.path.exists(chrome_path):
        print("❌ Google Chrome não encontrado em /Applications/")
        return False
    
    if not os.path.exists(html_file):
        print(f"❌ Arquivo HTML não encontrado: {html_file}")
        return False
    
    print("🔄 Gerando PDF com Google Chrome...")
    
    cmd = [
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--print-to-pdf=' + pdf_path,
        '--no-pdf-header-footer',
        f'file://{html_path}'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if os.path.exists(pdf_path):
            size_kb = os.path.getsize(pdf_path) / 1024
            print(f"✅ PDF gerado com sucesso: {pdf_file}")
            print(f"   Tamanho: {size_kb:.1f} KB")
            return True
        else:
            print("❌ PDF não foi gerado")
            if result.stderr:
                print(f"Erro: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout ao gerar PDF")
        return False
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        return False

if __name__ == '__main__':
    success = generate_pdf_with_chrome()
    sys.exit(0 if success else 1)

