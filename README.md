> ⚠️ **Nota de Confidencialidade e Proteção de Dados:** Este repositório é um **Technical Showcase (Clone de Portfólio)** do sistema original. A aplicação hospedada na demonstração ao vivo utiliza **dados 100% sintéticos e fictícios** para preservar o sigilo do modelo de negócio e garantir conformidade com a LGPD. O código-fonte representa um estudo de caso arquitetural, mas sua propriedade intelectual pertence exclusivamente aos detentores dos direitos.

<br>

<div align="center">
  <h1>🎓 CESOL Pro</h1>
  <h3>Dashboard de Gestão Escolar e Business Intelligence</h3>
  
  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
  [![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
  [![Fly.io](https://img.shields.io/badge/Fly.io-Cloud_Deployed-7b3b9b?style=for-the-badge&logo=flydotio&logoColor=white)](https://fly.io)
</div>

<br>

<div align="center">
  <h2>🌐 <a href="https://cesol-pro.fly.dev/" target="_blank">Acessar Demonstração ao Vivo (Live Demo)</a></h2>
  <p><i>O sistema pode levar alguns segundos para carregar no primeiro acesso devido à política de economia de recursos da nuvem (Cold Start).</i></p>
</div>

<br>

## ❖ O Desafio de Negócio (Business Case)
Instituições de ensino lidam com alto volume de dados fragmentados. O **CESOL Pro** nasceu para resolver a "cegueira gerencial", consolidando informações financeiras, acadêmicas e de retenção de alunos em uma plataforma única. A ferramenta permite aos diretores tomarem decisões baseadas em dados reais de CAC (Custo de Aquisição), LTV (Lifetime Value), Taxas de Churn e Ocupação.

---

## ⬚ Visão Geral da Interface (Screenshots)

<div align="center">
  <!-- Substitua os caminhos abaixo pelas suas imagens reais na pasta assets -->
  <img src="https://github.com/thiago-p-almeida/cesol_dashboard/blob/main/assets/dashboard.png" alt="Dashboard Principal" width="800">
  <br><br>
  <img src="https://github.com/thiago-p-almeida/cesol_dashboard/blob/main/assets/financeiro.png" alt="Performance Financeira" width="800">
</div>

---

## ⬢ Arquitetura e Engenharia de Software
Este projeto foi desenhado focando em manutenibilidade e escalabilidade, fugindo do paradigma de "scripts espaguete" comum em projetos de análise de dados. 

### 1. Padrões Arquiteturais Aplicados
* **Clean Architecture:** Separação estrita entre a camada de Apresentação (`/views` e `/components`), Lógica de Negócios (`/services`) e Camada de Dados (`/database` e `/schemas`).
* **Princípio SRP (Single Responsibility):** Lógicas segmentadas em microsserviços internos (ex: `academic.py` não lida com funções financeiras).
* **Princípio OCP (Open-Closed):** Variáveis de negócio (como capacidade física da escola e custos base) isoladas em `/config/*.json`, permitindo alteração de regras sem necessidade de refatorar código Python.
* **Injeção de Dependências:** Serviços são instanciados e injetados de forma controlada via `@st.cache_resource`, otimizando drasticamente o uso de memória RAM.

### 2. Infraestrutura (Cloud-Native)
* **Containerização:** Totalmente isolado via `Dockerfile` otimizado e focado em performance (apenas 425MB de tamanho final da imagem).
* **Gestão de Memória Virtual:** Configuração de alocação de *Swap file* interno no contêiner para prevenir travamentos por *OOM Kill* durante cálculos do Pandas.
* **PostgreSQL Separado:** Banco de dados relacional apartado da aplicação, garantindo persistência e segurança.

### 3. Data Quality & ETL
* O módulo de Ingestão de Dados (via uploader de CSV) utiliza **Pandera** para tipagem rigorosa. Antes da inserção no Banco, o sistema traduz chaves, formata datas, normaliza erros ortográficos (ex: "Ensino Fundamental" -> "Fundamental I") e valida taxonomias relacionais.

---

## ⚙︎ Stack Tecnológica

### Backend & Lógica
- **Python 3.11:** Core language.
- **Pandas & NumPy:** Processamento em lote, manipulação de dataframes e cálculos de BI.
- **SQLAlchemy 2.0:** ORM robusto para transações no banco de dados.
- **Pandera:** Validação estatística e garantias de contrato de dados (Data Quality).

### Frontend & UI/UX
- **Streamlit:** Framework reativo com injeção de CSS *Custom properties* e *Atomic DOM*.
- **Plotly Express:** Gráficos interativos, animados e polimórficos.
- **Design System Propriedade:** Tema Dark/Light dinâmico com paleta semântica focada em UI/UX Premium.

### DevOps & Deploy
- **Docker:** Criação da imagem da aplicação.
- **Fly.io:** Plataforma PaaS edge-network rodando micromaquinas virtuais de Linux.
- **Neon / Fly Postgres:** Provisão do Banco de Dados SQL.

---

## ◈ Funcionalidades Principais (Features)
- **Dashboard Global:** Cálculo em tempo real de Margem Operacional, Receita Total, Despesas Fixas e Saúde Financeira.
- **Unit Economics:** Motor automatizado que cruza dados financeiros com marketing para calcular Custo de Aquisição (CAC) e LTV, retornando *insights* da saúde do investimento.
- **Retenção & Churn:** Acompanhamento da taxa de evasão, gerando visões em *donut charts* dos motivos de saída e painéis de risco.
- **Análise Pedagógica:** Identificação inteligente de "Distorção Idade-Série" baseada na taxonomia aprovada pelo MEC.
- **Módulo de Projeção (Forecasting):** Gráfico preditivo (Área) simulando inadimplência (Slider dinâmico) vs. Receita Bruta/Líquida em até 24 meses futuros.

---

## § Licença e Direitos Autorais

Copyright (c) 2026 CESOL Pro. Todos os direitos reservados.

Este código-fonte é de propriedade exclusiva e confidencial. É estritamente proibida a cópia, reprodução, distribuição, comercialização ou modificação, parcial ou total, sem autorização prévia por escrito.

---
<div align="center">
  <small>Engenharia de Software e Data App desenvolvido por <a href="https://github.com/thiago-p-almeida">Thiago Almeida</a></small>
</div>