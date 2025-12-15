FROM python:3.12-slim


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*


ENV POETRY_VERSION=2.0.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"


WORKDIR /app


COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


COPY src /app/src


ENV PYTHONPATH=/app/src

EXPOSE 8000
