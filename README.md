# CESOL Pro - Dashboard de Gestão Escolar v2.0

Sistema de dashboard premium para gestão escolar, com interface moderna, temas Dark/Light e análises financeiras avançadas.

## ✨ Novidades da v2.0 Premium

- 🎨 **UI Kit Premium**: Temas "Midnight Scholar" (Dark) e "Scholar Pro" (Light)
- 🌓 **Toggle Dark/Light**: Alternância instantânea de temas
- 📊 **Gráficos Animados**: Plotly com transições suaves
- 🧭 **Navegação Lateral**: Menu hierárquico com streamlit-option-menu
- 🎯 **Cards de Métricas**: KPIs com sombras, ícones e variações
- 🚨 **Alertas Gerenciais**: Sistema de alertas com severidade

## 📁 Estrutura do Projeto (Clean Architecture)

```text
cesol_pro/
├── config/                  
│   └── expenses.json       # Configurações dinâmicas de custos (OCP)
├── .streamlit/
│   └── config.toml         # Configuração do Streamlit
├── assets/                 # Estilos CSS (dark, light, global)
├── components/             # Design System e Componentes UI
│   ├── cards.py            # Cards de métricas
│   ├── typography.py       # Renderizador de tipografia e HTML (DRY)
│   └── ...
├── utils/                  # Utilitários globais
├── views/                  # Views modulares (Apresentação)
│   ├── overview.py         # Dashboard principal
│   ├── financial.py        # Análise financeira
│   └── ...
└── src/
    ├── app/
    │   └── main.py         # Entry point (Injeção de Dependências)
    ├── services/           # Microsserviços de Domínio (SRP)
    │   ├── academic.py     # Lógica de alunos e churn
    │   ├── financial.py    # Lógica de receitas, custos e projeções
    │   ├── exports.py      # Geração de arquivos (Excel)
    │   └── ingestion.py    # Importação de dados
    ├── schemas/            # Contratos de Validação (Pandera)
    └── database/           # Modelos SQLAlchemy
```
## Padrões Arquiteturais Aplicados (v2.2)

Nesta versão, o sistema foi refatorado seguindo boas práticas de Engenharia de Software:
* **SRP (Single Responsibility Principle):** Serviços segmentados por domínio (`academic.py`, `financial.py`, `exports.py`), eliminando "God Classes".
* **OCP (Open-Closed Principle):** Parâmetros de negócio (como custos fixos) extraídos para `config/expenses.json`, permitindo alteração sem mexer no código Python.
* **DRY (Don't Repeat Yourself):** Design System implementado em `components/typography.py` para centralizar a geração de HTML e garantir consistência visual.

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/cesol_db
```

### 3. Executar o Dashboard

```bash
cd cesol_pro
streamlit run src/app/main.py
```

## 🎨 Sistema de Temas

### Tema Dark (Midnight Scholar)
- **Background**: `#0F172A`
- **Surface**: `#1E293B`
- **Texto Principal**: `#F1F5F9`
- **Texto Secundário**: `#94A3B8`

### Tema Light (Scholar Pro)
- **Background**: `#F8FAFC`
- **Surface**: `#FFFFFF`
- **Texto Principal**: `#0F172A`
- **Texto Secundário**: `#475569`

### Cores de Destaque
- **Sucesso**: `#10B981`
- **Info**: `#3B82F6`
- **Aviso**: `#F59E0B`
- **Perigo**: `#EF4444`
- **Especial**: `#8B5CF6`

## 📊 Funcionalidades

### Dashboard Principal (Overview)
- Resumo financeiro global
- Receita, despesas e resultado líquido
- Taxa de retenção
- Distribuição por segmento

### Financeiro
- Performance por segmento/série
- Composição de custos (gráfico donut)
- Receita por série (gráfico de barras)
- Ticket médio e variações

### Retenção
- Taxa de churn e retenção
- Motivos de saída (gráfico de pizza)
- Insights gerenciais
- Alertas de evasão

### Projeções
- Forecasting de receita
- Simulação de inadimplência
- Download em Excel
- Gráfico de área com risco

### Administração
- Upload de CSV de alunos
- Validação de schema
- Informações do sistema
- Processamento de importações

## 🧩 Componentes

### Cards de Métricas
```python
from components.cards import render_metric_card

render_metric_card(
    label="Receita Total",
    value="R$ 125.450,00",
    delta="↑ 12%",
    delta_color="success",
    icon="coins",
    variant="success"
)
```

### Gráficos Premium
```python
from components.charts import create_premium_pie, create_premium_bar

# Gráfico de pizza/donut
fig = create_premium_pie(data, values_col='valor', names_col='categoria')

# Gráfico de barras
fig = create_premium_bar(data, x_col='grade', y_col='net_tuition')
```

### Alertas
```python
from components.alerts import show_alert_premium, show_alert_container

# Alerta individual
show_alert_premium(
    message="Margem operacional baixa",
    alert_type="warning",
    title="Atenção"
)

# Container de alertas
show_alert_container(alerts_list, expanded=True)
```

## 🔧 Configuração

### config.toml
```toml
[theme]
primaryColor = "#10B981"
backgroundColor = "#F8FAFC"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#1E293B"
font = "sans serif"

[server]
enableCORS = false
enableXsrfProtection = true
```

## 📋 Requisitos

- Python 3.9+
- Streamlit 1.55.0
- Plotly 6.6.0
- SQLAlchemy 2.0
- PostgreSQL

## 📄 Licença

CESOL Pro - Gestão Escolar Inteligente
© 2024 CESOL Pro Team
