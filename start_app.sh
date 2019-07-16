#!/bin/bash

celery -A integrator_app.celery worker --concurrency=1 &> /home/integrator_proj/logs/celery.log  &

celery -A integrator_app.celery beat --loglevel=INFO &> /home/integrator_proj/logs/celery_beat.log  &

gunicorn --bind :5000 integrator_app:app
