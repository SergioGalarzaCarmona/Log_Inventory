#!/bin/sh

# Espera a que el servicio de base de datos responda
echo "Esperando a que la base de datos esté disponible..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Base de datos lista, iniciando servidor Django..."

exec "$@"