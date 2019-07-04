FROM python:3.7-alpine

ENV FLASK_APP integrator_app.py
ENV FLASK_CONFIG production
ENV CELERY_BROKER_URL redis://redis:6379
ENV CELERY_RESULT_BACKEND redis://redis:6379

WORKDIR /home/integrator_proj

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY integrator integrator
COPY migrations migrations
COPY integrator_app.py config.py ./

# run-time configuration
EXPOSE 5000
