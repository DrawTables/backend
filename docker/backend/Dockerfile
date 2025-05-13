FROM mcr.microsoft.com/playwright:v1.52.0-noble

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend
ARG SRC_DIR=./src
ARG POETRY_HOME=/etc/poetry
ENV PATH="$PATH:$POETRY_HOME/bin"

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_HOME python3 -
COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root
RUN poetry run playwright install

COPY $SRC_DIR $SRC_DIR
COPY ./certs ./certs
EXPOSE 8888

CMD ["poetry", "run", "uvicorn", "src.__main__:app", "--host", "0.0.0.0", "--port", "8888", "--workers", "4"]
