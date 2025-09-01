FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential python3-dev gcc libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

EXPOSE 5000
CMD ["poetry", "run", "python", "app.py"]
