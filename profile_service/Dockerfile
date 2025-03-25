FROM python:3.13-alpine

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /opt

COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==2.1.1" --no-cache-dir \
    && poetry config virtualenvs.create false  \
    && poetry install --no-root --no-cache 

COPY . .

ENTRYPOINT ["poetry", "run", "python", "main.py"]
