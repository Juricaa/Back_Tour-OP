# Étape 1 : build — installer les dépendances
FROM python:3.11-slim AS build

# Répertoire de travail
WORKDIR /app

# Éviter les invites interactives
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le reste du code du projet
COPY . .

# Étape 2 : image finale plus légère
FROM python:3.11-slim

WORKDIR /app

# Installer uniquement les dépendances système minimales
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers nécessaires depuis la première étape
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app /app

# Exposer le port 8000
EXPOSE 8000

# Commande par défaut : Gunicorn (production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
