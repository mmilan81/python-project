# Usa una versione leggera e ufficiale di Python
FROM python:3.11-slim

# Imposta la cartella di lavoro dentro il container
WORKDIR /app

# Copia i requisiti e installali
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del progetto
COPY . .

# Esponi la porta 8000
EXPOSE 8000

# Comando per avviare il server
CMD ["python", "avvia.py"]