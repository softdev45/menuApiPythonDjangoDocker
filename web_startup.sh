#!/bin/bash
#celery -A eMenu worker --loglevel=Info &
#celery -A eMenu beat --loglevel=Info &
python manage.py runserver "0.0.0.0:8000"

