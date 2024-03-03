FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY auth_service .

CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]