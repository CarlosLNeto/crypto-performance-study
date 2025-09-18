# Estudo de Desempenho Computacional de Algoritmos de Criptografia

## Descrição

Este projeto apresenta um estudo comparativo detalhado do desempenho computacional dos algoritmos de criptografia simétrica **AES**, **Blowfish** e **Twofish**. O estudo analisa métricas de CPU, memória, tempo de execução e throughput, fornecendo dados quantitativos para auxiliar na seleção de algoritmos em aplicações práticas.

## Autores

- **Carlos Lavor Neto**
- **Eric Dias Perin**
- **Alexandro Pantoja**

**Disciplina:** Tópicos Especiais em Computação IV  
**Instituição:** Universidade do Estado do Amazonas (UEA)

## Estrutura do Projeto

```
crypto-performance-study/
├── src/                        # Código fonte
│   ├── crypto_benchmark.py     # Implementação dos benchmarks
│   ├── analysis.py             # Análises e visualizações
│   ├── report_generator.py     # Gerador de relatório ABNT
│   └── run_study.py           # Script principal
├── data/                       # Dados gerados
│   └── benchmark_results.csv   # Resultados dos testes
├── results/                    # Resultados e gráficos
│   └── graficos/              # Visualizações geradas
├── docs/                       # Documentação
│   └── relatorio_latex_abnt.tex    # Relatório em LaTeX
├── requirements.txt            # Dependências Python
└── README.md                  # Este arquivo
```

## Características do Estudo

### Algoritmos Analisados
- **AES (Advanced Encryption Standard)**: 128, 192, 256 bits
- **Blowfish**: 128, 256 bits  
- **Twofish**: 128, 192, 256 bits

### Métricas Coletadas
- Tempo de execução (criptografia e descriptografia)
- Uso de CPU (percentual)
- Consumo de memória (MB)
- Throughput (MB/s)
- Análises estatísticas (média, desvio padrão, ANOVA)

### Tamanhos de Dados Testados
- 1 KB (1.024 bytes)
- 10 KB (10.240 bytes)
- 100 KB (102.400 bytes)
- 1 MB (1.048.576 bytes)
- 10 MB (10.485.760 bytes)

## Instalação e Execução

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Executar Estudo Completo
```bash
python src/run_study.py
```

O script executará automaticamente:
1. **Benchmark**: Testes de performance dos algoritmos
2. **Análise**: Geração de gráficos e análises estatísticas
3. **Relatório**: Criação do documento técnico em formato ABNT

### Execução Individual dos Módulos

```bash
# 1. Executar apenas o benchmark
python src/crypto_benchmark.py

# 2. Executar apenas as análises (após benchmark)
python src/analysis.py

# 3. Gerar apenas o relatório (após benchmark e análise)
python src/report_generator.py
```

## Resultados Principais

### Performance Geral
- **AES**: Melhor throughput médio (277.80 MB/s)
- **Blowfish**: Menor consumo de recursos (155.48 MB/s)
- **Twofish**: Performance intermediária (228.19 MB/s)

### Análise Estatística
- **40 configurações testadas** (algoritmos × chaves × tamanhos)
- **100 iterações por teste** para confiabilidade estatística
- **Análise ANOVA** confirma diferenças não significativas (p > 0.05)

## Metodologia

### Configuração dos Testes
- **Iterações por teste**: 100 execuções para garantir confiabilidade estatística
- **Ambiente controlado**: Medições isoladas com limpeza de memória entre testes
- **Dados aleatórios**: Geração de dados criptograficamente seguros para cada teste

### Métricas Coletadas
- **Tempo**: Medição precisa usando `time.perf_counter()`
- **CPU**: Monitoramento via `psutil.Process().cpu_percent()`
- **Memória**: Medição de RSS (Resident Set Size) via `psutil`
- **Throughput**: Calculado como dados processados por segundo

## Aplicações Práticas

### Recomendações de Uso

**AES**: Recomendado para aplicações gerais que requerem equilíbrio entre segurança e performance.

**Blowfish**: Adequado para sistemas com restrições de recursos processando dados menores.

**Twofish**: Indicado para aplicações que priorizam segurança máxima sobre performance.

## Documentação

- **Relatório LaTeX**: Documento completo em formato ABNT para compilação em PDF
- **Gráficos**: 4 visualizações PNG profissionais para inclusão no relatório
- **Dados**: Tabela resumo CSV com estatísticas detalhadas

## Licença

Este projeto é disponibilizado para fins acadêmicos e educacionais. Consulte os termos de uso das bibliotecas utilizadas para aplicações comerciais.

---

**Universidade do Estado do Amazonas**  
**Escola Superior de Tecnologia**  
**Curso de Engenharia de Computação**  
**2025**
