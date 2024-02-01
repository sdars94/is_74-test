FROM python:3.10-bullseye

WORKDIR ml_microservice/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry POETRY_VERSION=1.5.1 python3  && \
    cd /usr/local/bin && \
    ln -s /etc/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-dev

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/ml_microservice"

CMD sh -c "gunicorn app.main:app --workers 2 --worker-class \
           uvicorn.workers.UvicornWorker --bind=0.0.0.0:5000"