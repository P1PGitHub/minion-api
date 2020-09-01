web: gunicorn minionapi.minionapi.wsgi:application --log-file - --log-level debug
python minionapi/manage.py collectstatic --noinput
minionapi/manage.py migrate