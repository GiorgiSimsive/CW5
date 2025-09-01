FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional dos2unix curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.2
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root

COPY . .

# ВАЖНО для Windows: конвертируем окончания строк и выставляем +x
RUN dos2unix docker/entrypoint/*.sh docker/wait-for-it.sh || true && \
    chmod +x docker/entrypoint/*.sh && \
    chmod +x docker/wait-for-it.sh
