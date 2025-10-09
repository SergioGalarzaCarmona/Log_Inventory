#!/bin/sh
set -e

host="db"
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres no está listo aún - esperando..."
  sleep 2
done

>&2 echo "Postgres está listo - arrancando Django"
exec "$@"