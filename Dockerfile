# Pull official latest Python Docker image
FROM python:3.11.2

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \

  # poetry:
  POETRY_VERSION=1.3.2 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    brotli \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /code

# Copy only requirements, to cache them in docker layer
COPY ./poetry.lock ./pyproject.toml /code/

# Project initialization:
RUN --mount=type=cache,target=/var/cache/pypoetry \
  poetry version \
  # Install deps:
  && poetry run pip install -U pip \
  && pip install tornado \
  && pip install prometheus_client \
  && poetry install --only main --no-interaction --no-ansi

COPY . /code
