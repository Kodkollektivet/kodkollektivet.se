#!/bin/sh
python kodkollektivet/manage.py makemigrations
python kodkollektivet/manage.py migrate
exec "$@"
