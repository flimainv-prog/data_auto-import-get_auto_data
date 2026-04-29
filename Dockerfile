# Dockerfile para deploy no Render com Python 3.11-slim
FROM python:3.11-slim

WORKDIR /app

# Copia requirements primeiro para cache
COPY requirements.txt .

# Instala dependências sem cache para evitar compilação desnecessária
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Configurações de ambiente
ENV PYTHONUNBUFFERED=1

# Executa Streamlit na porta $PORT definida pelo Render
EXPOSE $PORT

CMD ["sh", "-c", "streamlit run app.py --server.port=$$PORT --server.address=0.0.0.0 --server.headless true"]
