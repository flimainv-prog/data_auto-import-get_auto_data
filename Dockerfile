FROM python:3.11-slim

WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências com versões específicas
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    streamlit==1.38.0 \
    pandas==2.2.2 \
    numpy==1.26.4 \
    yfinance==0.2.40

EXPOSE 8501

# Usa forma shell do CMD para expansão correta de ${PORT:-8501}
CMD streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0
