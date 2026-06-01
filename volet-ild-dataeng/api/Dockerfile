# API Néovolt Grid+ — image légère (volet ILD)
FROM python:3.11-slim

# Bonnes pratiques : pas de .pyc, logs non bufferisés
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NEOVOLT_DB=/data/neovolt.db

WORKDIR /app

# Dépendances d'abord (cache de couche Docker)
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Code de l'API
COPY main.py .

# Sécurité : ne pas tourner en root (DevSecOps)
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# L'entrepôt est monté en lecture seule sur /data (voir docker-compose.yml)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
