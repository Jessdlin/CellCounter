FROM python:3.7 AS base

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /build
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile --dev

WORKDIR /app