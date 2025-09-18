# Estudo Completo de Criptografia Aplicada

## Descrição

Este projeto apresenta um estudo abrangente sobre criptografia aplicada, dividido em duas atividades independentes:

**Atividade 1:** Análise comparativa detalhada do desempenho computacional dos algoritmos de criptografia simétrica **AES**, **Blowfish** e **Twofish**.

**Atividade 2:** Desenvolvimento de uma aplicação prática de envio de mensagens com **assinatura digital** e certificados ad-hoc.

## Autores

- **Carlos Lavor Neto**
- **Eric Dias Perin**
- **Alexandro Pantoja**

**Disciplina:** Tópicos Especiais em Computação IV  
**Instituição:** Universidade do Estado do Amazonas (UEA)

## Estrutura do Projeto

```
crypto-performance-study/
├── atividade1/                     # ATIVIDADE 1: Algoritmos Simétricos
│   ├── src/
│   │   ├── crypto_benchmark.py     # Benchmark dos algoritmos
│   │   ├── analysis.py             # Análises e gráficos
│   │   └── run_study.py           # Script original
│   ├── data/
│   │   └── benchmark_results.csv   # Resultados dos testes
│   ├── results/
│   │   ├── performance_comparison.png
│   │   ├── throughput_analysis.png
│   │   ├── scalability_analysis.png
│   │   ├── correlation_heatmap.png
│   │   └── summary_table.csv
│   └── run_atividade1.py          # Script executável
│
├── atividade2/                     # ATIVIDADE 2: Assinatura Digital
│   ├── src/
│   │   ├── digital_signature_app.py    # Aplicação principal
│   │   └── signature_analysis.py       # Análise de performance
│   ├── data/
│   │   └── signature_performance_results.csv
│   ├── results/
│   │   ├── signature_performance_analysis.png
│   │   └── signature_operations_comparison.png
│   ├── certificates/               # Certificados gerados
│   ├── messages/                   # Mensagens assinadas
│   └── run_atividade2.py          # Script executável
│
├── src/                            # Scripts integrados
│   └── run_complete_study.py      # Execução completa
├── relatorio_latex_abnt.tex       # Relatório técnico integrado
├── requirements.txt
└── README.md
```

## Execução das Atividades

### Pré-requisitos
```bash
pip install -r requirements.txt
```

### Atividade 1: Análise de Algoritmos Simétricos
```bash
python atividade1/run_atividade1.py
```

**Resultados gerados:**
- Benchmark de performance (AES, Blowfish, Twofish)
- 4 gráficos comparativos
- Análises estatísticas (ANOVA)
- Dados em CSV

### Atividade 2: Aplicação de Assinatura Digital
```bash
python atividade2/run_atividade2.py
```

**Resultados gerados:**
- Certificados X.509 ad-hoc
- Mensagens assinadas digitalmente
- 2 gráficos de performance
- Análise de operações criptográficas

### Execução Completa (Ambas as Atividades)
```bash
python src/run_complete_study.py
```

## Características das Atividades

### Atividade 1: Algoritmos de Criptografia Simétrica

**Algoritmos Analisados:**
- AES (128, 192, 256 bits)
- Blowfish (128, 256 bits)
- Twofish (128, 192, 256 bits)

**Métricas Coletadas:**
- Tempo de execução
- Uso de CPU e memória
- Throughput (MB/s)
- Análises estatísticas

**Resultados Principais:**
- AES: Melhor throughput (277.80 MB/s)
- Blowfish: Menor consumo de recursos
- Twofish: Performance intermediária

### Atividade 2: Aplicação de Assinatura Digital

**Funcionalidades:**
- Geração de certificados X.509 ad-hoc
- Assinatura digital (RSA-PSS + SHA-256)
- Verificação de integridade
- Detecção de alterações (100% eficaz)

**Características Técnicas:**
- RSA 2048 bits
- Certificados auto-assinados
- Armazenamento PKCS#12
- Formato JSON para mensagens

## Visualizações Geradas

### Atividade 1 (4 gráficos):
- Comparação de performance geral
- Análise de throughput
- Escalabilidade por tamanho
- Matriz de correlação

### Atividade 2 (2 gráficos):
- Performance das operações
- Comparação assinatura vs verificação

## Documentação

- **Relatório LaTeX Integrado**: Documento completo em formato ABNT
- **6 Visualizações PNG**: Gráficos profissionais
- **Dados Estruturados**: Tabelas CSV com estatísticas
- **Código Documentado**: Implementação completa

## Aplicações Práticas

### Atividade 1: Seleção de Algoritmos
- **AES**: Aplicações gerais (equilíbrio segurança/performance)
- **Blowfish**: Sistemas com restrições de recursos
- **Twofish**: Aplicações que priorizam segurança máxima

### Atividade 2: Sistema de Autenticação
- Comunicações seguras sem PKI complexa
- Verificação de integridade de documentos
- Autenticação de remetentes

## Repositório

**Link:** https://github.com/CarlosLNeto/crypto-performance-study.git

## Licença

Projeto desenvolvido para fins acadêmicos e educacionais.

---

**Universidade do Estado do Amazonas**  
**Escola Superior de Tecnologia**  
**Curso de Engenharia de Computação**  
**2025**
