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
├── atividade2/                     # ATIVIDADE 2: Chat com Assinatura Digital
│   ├── src/
│   │   ├── chat_app.py             # Aplicação de chat com WebSocket
│   │   └── performance_analysis.py # Análise de performance do chat
│   ├── templates/
│   │   ├── login.html              # Interface de login
│   │   └── chat.html               # Interface do chat
│   ├── data/
│   │   ├── chat_performance_results.csv
│   │   └── chat_stress_results.csv
│   ├── results/
│   │   ├── chat_performance_analysis.png
│   │   ├── chat_operations_comparison.png
│   │   ├── chat_metrics_latex.png
│   │   ├── chat_statistics_latex.png
│   │   └── chat_metrics_table_latex.tex
│   ├── certificates/               # Certificados gerados automaticamente
│   ├── run_chat.py                 # Script do chat
│   ├── run_performance_analysis.py # Script de análise
│   └── generate_latex_charts.py    # Gráficos para LaTeX
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

### Atividade 2: Sistema de Chat com Assinatura Digital

**Roteiro de Execução:**

```bash
# 1. Executar o chat e enviar mensagens
python atividade2/run_chat.py
# (Acesse http://localhost:8081, faça login, envie mensagens, depois Ctrl+C)

# 2. Gerar gráficos com dados reais coletados
python atividade2/generate_latex_charts.py
```

**Sistema de Coleta:**
- ✅ **Métricas Reais**: Coleta automática durante uso do chat
- ✅ **Dados Reais**: Apenas mensagens reais enviadas pelos usuários
- ✅ **Sem Simulação**: Análise baseada exclusivamente em uso real

**Resultados gerados:**
- Sistema de chat em tempo real com WebSocket
- Certificados X.509 gerados automaticamente
- 4 gráficos baseados em métricas reais + 1 tabela LaTeX
- Análise de operações criptográficas reais

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

### Atividade 2: Sistema de Chat com Assinatura Digital

**Arquitetura Implementada:**
- **Backend**: Flask + SocketIO para WebSocket
- **Frontend**: Interface web responsiva com JavaScript
- **Criptografia**: RSA-PSS + SHA-256 para assinatura digital
- **Certificados**: X.509 auto-assinados gerados automaticamente

**Funcionalidades Avançadas:**
- Comunicação bidirecional em tempo real via WebSocket
- Assinatura automática de todas as mensagens
- Verificação de integridade em tempo real
- Sistema de salas (rooms) para broadcast
- Estatísticas dinâmicas de uso
- Indicadores visuais de status de verificação
- Painel lateral com usuários online
- Interface responsiva para dispositivos móveis

**Características Técnicas:**
- RSA 2048 bits para geração de chaves
- Certificados PKCS#12 com senha
- Armazenamento seguro de certificados
- Coleta de métricas de performance em tempo real
- Análise robusta de throughput e latência

**Métricas de Performance Coletadas:**
- Tempo de assinatura (usuário único): ~63ms (média)
- Tempo de assinatura (multiusuário): ~180ms (média)
- Tempo de verificação: ~0.10ms (média)
- Throughput de assinatura: ~6.62 KB/s (único), ~2.65 KB/s (multi)
- Throughput de verificação: ~4.217 MB/s
- Escalabilidade: Degradação de 2.8x com múltiplos usuários
- Teste de stress com 5 usuários simultâneos por 30s

## Visualizações Geradas

### Atividade 1 (4 gráficos):
- Comparação de performance geral
- Análise de throughput
- Escalabilidade por tamanho
- Matriz de correlação

### Atividade 2 (4 gráficos + 1 tabela LaTeX):
- Performance das operações do chat (chat_performance_analysis.png)
- Comparação de operações do chat (chat_operations_comparison.png)
- Métricas para LaTeX (chat_metrics_latex.png)
- Estatísticas para LaTeX (chat_statistics_latex.png)
- Tabela LaTeX (chat_metrics_table_latex.tex)

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
