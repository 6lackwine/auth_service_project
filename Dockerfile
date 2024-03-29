FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.2"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY auth_service .

CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]