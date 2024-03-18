FROM python:3.11.5-slim

ARG CONNECTION_STRING

ENV CONNECTION_STRING=${CONNECTION_STRING} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.2

RUN apt-get update && apt-get install -y libpq-dev

# System deps:
# RUN curl -sSL https://install.python-poetry.org | python3 -

RUN apt-get update && apt-get install -y \
    curl

# Install Poetry:
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN apt-get update
RUN apt-get -y install gcc

WORKDIR /app

# Install dependencies with Poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app"]