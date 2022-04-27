FROM --platform=linux/amd64 python:3.10-slim as python-base

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

FROM python-base as requirements-stage

WORKDIR /tmp 
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Generate requirements.txt file
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python-base as production

# Copy only requirements to cache them in docker layer
WORKDIR /app

# Install requirements
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy environment information
COPY ./local-env /app/.env

# Creating folders, and files for a project:
COPY ./src /app/src

# Setup a non-root user to run the app
RUN useradd -m myuser
USER myuser

# Launch the application
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9090"]
CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
