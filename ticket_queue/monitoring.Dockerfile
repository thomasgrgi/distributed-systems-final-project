FROM python:3.10-slim

# Dossier de travail dans le container
WORKDIR /app

# Copier le code du service monitoring
COPY monitoring/ /app

# Installer les dépendances nécessaires
RUN pip install fastapi uvicorn redis requests

# Lancer l'API monitoring
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
