FROM python:3.12-slim

WORKDIR /code

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /code

ENV PYTHONPATH=/code
