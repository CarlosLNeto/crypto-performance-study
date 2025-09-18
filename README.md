# Estudo de Desempenho Computacional de Algoritmos de Criptografia

## Descrição

Este projeto apresenta um estudo comparativo detalhado do desempenho computacional dos algoritmos de criptografia simétrica **AES**, **Blowfish** e **Twofish**. O estudo analisa métricas de CPU, memória, tempo de execução e throughput, fornecendo dados quantitativos para auxiliar na seleção de algoritmos em aplicações práticas.

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

## Estrutura do Projeto

```
Projeto01_Parte1/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências Python
├── run_study.py                # Script principal
├── crypto_benchmark.py         # Implementação dos benchmarks
├── analysis.py                 # Análises e visualizações
├── report_generator.py         # Gerador de relatório ABNT
├── benchmark_results.csv       # Dados brutos (gerado)
├── relatorio_tecnico_abnt.txt  # Relatório final (gerado)
└── graficos/                   # Pasta com gráficos (gerada)
    ├── performance_comparison.png
    ├── throughput_analysis.png
    ├── scalability_analysis.png
    ├── correlation_heatmap.png
    ├── statistical_analysis.txt
    └── summary_table.csv
```

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
python run_study.py
```

O script executará automaticamente:
1. **Benchmark**: Testes de performance dos algoritmos
2. **Análise**: Geração de gráficos e análises estatísticas
3. **Relatório**: Criação do documento técnico em formato ABNT

### Execução Individual dos Módulos

Se preferir executar cada etapa separadamente:

```bash
# 1. Executar apenas o benchmark
python crypto_benchmark.py

# 2. Executar apenas as análises (após benchmark)
python analysis.py

# 3. Gerar apenas o relatório (após benchmark e análise)
python report_generator.py
```

## Resultados Gerados

### Arquivos de Dados
- `benchmark_results.csv`: Dados brutos de todos os testes
- `graficos/summary_table.csv`: Tabela resumo estatística

### Visualizações
- `performance_comparison.png`: Comparação geral de performance
- `throughput_analysis.png`: Análise de throughput por algoritmo
- `scalability_analysis.png`: Comportamento com diferentes tamanhos de dados
- `correlation_heatmap.png`: Correlações entre métricas

### Relatórios
- `relatorio_tecnico_abnt.txt`: Documento técnico completo em formato ABNT
- `graficos/statistical_analysis.txt`: Análise estatística detalhada

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

### Análises Estatísticas
- Estatísticas descritivas (média, desvio padrão)
- ANOVA para identificar diferenças significativas
- Análise de correlação entre variáveis
- Testes de significância estatística

## Interpretação dos Resultados

### Gráficos de Performance
Os gráficos mostram comparações diretas entre algoritmos para diferentes métricas, facilitando a identificação do melhor algoritmo para cada cenário.

### Análise de Throughput
Boxplots revelam a distribuição de throughput, incluindo outliers e variabilidade de cada algoritmo.

### Escalabilidade
Gráficos logarítmicos mostram como cada algoritmo se comporta com o aumento do volume de dados.

### Correlações
Heatmap identifica relações entre métricas, revelando trade-offs entre velocidade e uso de recursos.

## Aplicações Práticas

### Recomendações de Uso

**AES**: Recomendado para aplicações gerais que requerem equilíbrio entre segurança e performance.

**Blowfish**: Adequado para sistemas com restrições de recursos processando dados menores.

**Twofish**: Indicado para aplicações que priorizam segurança máxima sobre performance.

### Fatores de Decisão
- Volume de dados a processar
- Restrições de recursos (CPU/memória)
- Requisitos de latência
- Nível de segurança exigido

## Limitações

- Testes realizados em ambiente controlado (macOS)
- Implementação do Twofish pode não refletir otimizações específicas
- Resultados podem variar em diferentes arquiteturas de hardware
- Não inclui análise de consumo energético

## Trabalhos Futuros

- Extensão para outros algoritmos (ChaCha20, Salsa20)
- Testes em diferentes arquiteturas (ARM, x86)
- Análise de consumo energético
- Avaliação com cargas de trabalho mistas
- Implementação de otimizações específicas de hardware

## Contribuições

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de Tópicos Especiais em Computação IV. O código é disponibilizado para fins educacionais e de pesquisa.

## Licença

Este projeto é disponibilizado para fins acadêmicos e educacionais. Consulte os termos de uso das bibliotecas utilizadas para aplicações comerciais.

---

**Autor**: Trabalho Acadêmico - Engenharia de Computação  
**Instituição**: Universidade do Estado do Amazonas  
**Data**: 2025
