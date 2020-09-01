web: gunicorn --pythonpath minionapi/ minionapi.wsgi --log-file - --log-level debug
python minionapi/manage.py collectstatic --noinput
minionapi/manage.py migrate