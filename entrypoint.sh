#!/bin/sh
python kodkollektivet/manage.py makemigrations
python kodkollektivet/manage.py migrate
python kodkollektivet/manage.py compilemessages -l sv -l en
exec "$@"
