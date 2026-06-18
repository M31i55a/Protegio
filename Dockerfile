FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Copie requirements et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

EXPOSE 8000

# Lance avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "unified_tool.wsgi:application"]
