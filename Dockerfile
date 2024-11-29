FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "celery -A zibal_project worker --loglevel=info & celery -A zibal_project beat --loglevel=info & python manage.py runserver 0.0.0.0:8000"]
