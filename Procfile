web: gunicorn ispeye.wsgi --log-file -
release: python manage.py migrate --no-input && python manage.py collectstatic --no-input && python manage.py seed_emails
