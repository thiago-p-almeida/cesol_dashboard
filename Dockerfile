# 1. Usa uma imagem oficial do Python, leve e otimizada
FROM python:3.11-slim

# 2. Evita que o Python grave arquivos .pyc e força logs diretamente no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Instala dependências do sistema operacional necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia apenas o arquivo de dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .

# 6. Instala as bibliotecas do projeto
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copia o restante do código do projeto
COPY . .

# 8. Expõe a porta que o Streamlit usa por padrão
EXPOSE 8501

# 9. Comando de checagem de saúde (mantém a Fly informada se a app travou)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 10. O comando que dá vida ao sistema
CMD["streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]