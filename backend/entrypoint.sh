#!/bin/sh

# Aguarda o banco responder na porta 5432 antes de iniciar o Django
until nc -z db 5432; do
    echo "Aguardando o banco de dados..."
    sleep 1
done

# Aplica migrações e cria superusuário, se desejar
poetry run python manage.py migrate --noinput

# Inicia o Gunicorn
exec poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 300 --workers 4