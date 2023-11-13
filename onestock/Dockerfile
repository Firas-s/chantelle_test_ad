
FROM python:3.9

ENV PYTHONUNBUFFERED True

COPY runs/onestock/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install keyrings.google-artifactregistry-auth
#COPY <key_location> /app/key.json
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json
RUN pip install -r requirements.txt

ENV APP_HOME /app

COPY runs/onestock/app.py $APP_HOME/
COPY runs/onestock/src $APP_HOME/src

WORKDIR $APP_HOME

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --reload app:app