#!/bin/bash

celery -A integrator_app.celery worker --concurrency=1 &> /Users/vladislav.bezugliy/Dev/MyProjects/integrator/logs/celery.log  &

celery --pidfile= -A integrator_app.celery beat --loglevel=INFO &> /Users/vladislav.bezugliy/Dev/MyProjects/integrator/logs/celery_beat.log &

gunicorn --bind :5000 integrator_app:app
