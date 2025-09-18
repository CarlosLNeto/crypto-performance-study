# Estudo Completo de Criptografia Aplicada

## Descrição

Este projeto apresenta um estudo abrangente sobre criptografia aplicada, dividido em duas partes complementares:

**Parte I:** Análise comparativa detalhada do desempenho computacional dos algoritmos de criptografia simétrica **AES**, **Blowfish** e **Twofish**, analisando métricas de CPU, memória, tempo de execução e throughput.

**Parte II:** Desenvolvimento de uma aplicação prática de envio de mensagens com **assinatura digital**, implementando geração de certificados ad-hoc e mecanismos de verificação de autenticidade, integridade e não-repúdio.

## Autores

- **Carlos Lavor Neto**
- **Eric Dias Perin**
- **Alexandro Pantoja**

**Disciplina:** Tópicos Especiais em Computação IV  
**Instituição:** Universidade do Estado do Amazonas (UEA)

## Estrutura do Projeto

```
crypto-performance-study/
├── src/                            # Código fonte
│   ├── crypto_benchmark.py         # Benchmark algoritmos simétricos
│   ├── analysis.py                 # Análises e visualizações - Parte I
│   ├── digital_signature_app.py    # Aplicação de assinatura digital
│   ├── signature_analysis.py       # Análise de performance - Parte II
│   ├── report_generator.py         # Gerador de relatório
│   ├── run_study.py               # Script Parte I
│   └── run_complete_study.py      # Script completo integrado
├── data/                           # Dados gerados
│   ├── benchmark_results.csv       # Resultados - algoritmos simétricos
│   └── signature_performance_results.csv  # Resultados - assinatura digital
├── results/                        # Resultados e gráficos
│   └── graficos/                  # Todas as visualizações
├── certificates/                   # Certificados digitais gerados
├── messages/                       # Mensagens assinadas
├── docs/                          # Documentação
│   └── relatorio_latex_abnt.tex   # Relatório integrado em LaTeX
├── requirements.txt               # Dependências Python
└── README.md                     # Este arquivo
```

## Características do Estudo

### Parte I: Algoritmos de Criptografia Simétrica

**Algoritmos Analisados:**
- **AES (Advanced Encryption Standard)**: 128, 192, 256 bits
- **Blowfish**: 128, 256 bits  
- **Twofish**: 128, 192, 256 bits

**Métricas Coletadas:**
- Tempo de execução (criptografia e descriptografia)
- Uso de CPU (percentual)
- Consumo de memória (MB)
- Throughput (MB/s)
- Análises estatísticas (média, desvio padrão, ANOVA)

**Tamanhos de Dados Testados:**
- 1 KB a 10 MB (5 tamanhos diferentes)

### Parte II: Aplicação de Assinatura Digital

**Funcionalidades Implementadas:**
- Geração de certificados X.509 ad-hoc
- Assinatura digital com RSA-PSS e SHA-256
- Verificação de assinaturas e integridade
- Detecção de alterações em mensagens
- Armazenamento seguro de certificados (PKCS#12)

**Métricas de Performance:**
- Tempo de geração de certificados
- Performance de assinatura por tamanho de mensagem
- Performance de verificação
- Throughput de operações criptográficas

## Instalação e Execução

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Executar Estudo Completo (Ambas as Partes)
```bash
python src/run_complete_study.py
```

### Execução Individual das Partes

```bash
# Apenas Parte I (Algoritmos Simétricos)
python src/run_study.py

# Apenas demonstração da Parte II
python src/digital_signature_app.py

# Apenas análise de performance da Parte II
python src/signature_analysis.py
```

## Resultados Principais

### Parte I: Performance de Algoritmos Simétricos
- **AES**: Melhor throughput médio (277.80 MB/s)
- **Blowfish**: Menor consumo de recursos (155.48 MB/s)
- **Twofish**: Performance intermediária (228.19 MB/s)
- **40 configurações testadas** com 100 iterações cada
- **Análise ANOVA** confirma diferenças não significativas (p > 0.05)

### Parte II: Aplicação de Assinatura Digital
- **100% de eficácia** na detecção de alterações
- **Certificados X.509** auto-assinados funcionais
- **RSA-PSS com SHA-256** para máxima segurança
- **Performance escalável** para diferentes tamanhos de mensagem

## Metodologia

### Parte I: Benchmarks de Algoritmos
- **100 iterações por teste** para confiabilidade estatística
- **Ambiente controlado** com limpeza de memória entre testes
- **Dados aleatórios** criptograficamente seguros
- **Medições precisas** de tempo, CPU e memória

### Parte II: Desenvolvimento da Aplicação
- **Certificados ad-hoc** eliminando necessidade de PKI
- **Padrões criptográficos** modernos (RSA-2048, SHA-256, PSS)
- **Testes de integridade** com detecção de alterações
- **Análise de performance** das operações criptográficas

## Visualizações Geradas

### Parte I (6 gráficos):
- Comparação geral de performance
- Análise de throughput
- Escalabilidade por tamanho de dados
- Matriz de correlação entre métricas

### Parte II (2 gráficos):
- Performance das operações de assinatura digital
- Comparação entre assinatura e verificação

## Documentação

- **Relatório LaTeX Integrado**: Documento completo em formato ABNT
- **8 Visualizações PNG**: Gráficos profissionais para inclusão no relatório
- **Dados Estruturados**: Tabelas CSV com estatísticas detalhadas
- **Código Documentado**: Implementação completa com comentários

## Aplicações Práticas

### Seleção de Algoritmos Simétricos
- **AES**: Aplicações gerais com equilíbrio segurança/performance
- **Blowfish**: Sistemas com restrições de recursos
- **Twofish**: Aplicações que priorizam segurança máxima

### Sistema de Assinatura Digital
- **Comunicações seguras** sem infraestrutura PKI complexa
- **Verificação de integridade** de documentos e mensagens
- **Autenticação** de remetentes em sistemas controlados

## Licença

Este projeto é disponibilizado para fins acadêmicos e educacionais. Consulte os termos de uso das bibliotecas utilizadas para aplicações comerciais.

---

**Universidade do Estado do Amazonas**  
**Escola Superior de Tecnologia**  
**Curso de Engenharia de Computação**  
**2025**
