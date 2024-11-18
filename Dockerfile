ARG REPO=docker.io
ARG IMAGE_NAME=python
ARG IMAGE_TAG=3.10.15-slim-bookworm
ARG IMAGE_HASH=sha256:eb9ca77b1a0ffbde84c1dc333beb3490a2638813cc25a339f8575668855b9ff1

FROM $REPO/$IMAGE_NAME:$IMAGE_TAG@$IMAGE_HASH AS base-image

LABEL maintainer="dmitrii@zakharov.cc"

ENV \
  DEBIAN_FRONTEND=noninteractive \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
#   PIP_CONSTRAINT=/app/constraints.txt \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100

# renovate: datasource=repology depName=debian_12/expat versioning=loose
ENV LIBEXPAT_VERSION="2.5.0-1+deb12u1"
  
SHELL ["/bin/bash", "-exo", "pipefail", "-c"]

RUN \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
        libexpat1="${LIBEXPAT_VERSION}" \
    # Create workdir
    && mkdir /app \
    && echo "setuptools<72" >/app/constraints.txt \
    # Upgrade pip
    && pip install --upgrade pip==23.3 \
    # fix CVE-2024-6345
    && pip install --upgrade setuptools==70.0.0 \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/

WORKDIR /app

FROM base-image AS compile-image

ENV \
  # poetry:
  POETRY_VERSION=1.8.2 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

COPY ./poetry.lock ./pyproject.toml /app/

RUN \
    # Install build dependencies:
    apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential=12.9 \
        python3-dev=3.11.2-1+b1 \
    # Install poetry: \
    && pip install --no-cache-dir poetry==$POETRY_VERSION \
    # Create virtualenv:
    && python -m venv --upgrade-deps /app/dev-venv \
    && python -m venv --upgrade-deps /app/prod-venv \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/ \
    # Создаём виртуальное окружение c библиотеками для тестирования
    && poetry export --no-ansi --no-interaction --with dev --output dev-requirements.txt \
    && /app/dev-venv/bin/pip install --no-cache-dir --require-hashes -r dev-requirements.txt \
    # Создаём виртуальное окружение для прода
    && poetry export --no-ansi --no-interaction --output requirements.txt \
    && /app/prod-venv/bin/pip install --no-cache-dir --require-hashes -r requirements.txt \
    # Меняем в файлах абсолютные пути, т.к. в итоге виртуальная среда будет находиться в папке venv
    && rm -rf /app/dev-venv/bin/__pycache__ \
    && sed -i "s|dev-venv|venv|g" /app/dev-venv/bin/* \
    && rm -rf /app/prod-venv/bin/__pycache__ \
    && sed -i "s|prod-venv|venv|g" /app/prod-venv/bin/*

FROM base-image AS build-image

ARG UID=1000
ARG GID=1000

ENV \
  # non-root user ids:
  UID=${UID:-1000} \
  GID=${GID:-1000}

RUN \
    # Create user and group:
    groupadd -r web --gid $GID \
    && useradd -d /app -r -g web web --uid $UID \
    && chown web:web -R /app \
    # Prepare uWSGI:
    && touch /var/run/uwsgi-touch-reload \
    && chown web:web /var/run/uwsgi-touch-reload \
    # Make dirs:
    && mkdir -p /var/www/lk_astra/public /var/www/lk_astra/static /var/www/lk_astra/data \
    && chown -R web:web /var/www/lk_astra

COPY --chown=web:web --chmod=700 deploy/app/scripts/* deploy/app/configs/* /app/

ENV PATH=/app/venv/bin:$PATH

USER web

COPY --chown=web:web ./hw /app/hw

FROM build-image AS prod-image

COPY --chown=web:web --from=compile-image /app/prod-venv /app/venv

CMD ["/app/start-api-prod.sh"]

FROM build-image AS dev-image

COPY --chown=web:web --from=compile-image /app/dev-venv /app/venv
COPY --chown=web:web ./tests /app/tests

CMD ["/app/start-api-prod.sh"]
