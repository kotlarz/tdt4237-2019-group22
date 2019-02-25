#!/usr/bin/env bash
python3 sec/manage.py migrate --no-input
python3 sec/manage.py shell < ./create_superuser.py
python3 sec/manage.py collectstatic --noinput
python3 sec/manage.py loaddata seed.json

uwsgi --chdir=/usr/src/app/sec -w sec.wsgi:application --processes=2 --harakiri=20 --http :80XX --master
