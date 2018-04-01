#!/bin/sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py compilemessages -l sv -l en
exec "$@"
