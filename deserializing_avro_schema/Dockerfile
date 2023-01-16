FROM python:3.11.0

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  # poetry:
  POETRY_VERSION=1.2.2 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME="/opt/poetry" \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install shellcheck for running linting
RUN apt-get update && apt-get install -y shellcheck

# Installing `poetry` package manager:
# https://github.com/python-poetry/poetry
RUN curl -sSL 'https://install.python-poetry.org' | python \
  && poetry --version

RUN mkdir /code
WORKDIR /code

# Copy only requirements, to cache them in docker layer
COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./deserializing_avro_schema /code

RUN mkdir /code/script
COPY ./deserializing_avro_schema/local_entrypoint.sh /code/script

RUN chmod +x /code/script/local_entrypoint.sh
