FROM python:3.9

WORKDIR /code/build

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# MODE=[runserver, gunicorn, celery, celerybeat]
ENV MODE=gunicorn
ENV PYTHONPATH "/code/build/app"

CMD bash -C './start.sh'
