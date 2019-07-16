FROM python:3.7

ENV FLASK_APP integrator_app.py
ENV FLASK_CONFIG production

WORKDIR /home/integrator_proj

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY integrator integrator
COPY migrations migrations
COPY integrator_app.py config.py start_app.sh '.env' ./

RUN chmod +x ./start_app.sh

# run-time configuration
EXPOSE 5000 5432
