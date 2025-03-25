FROM python:3.13-alpine

#ENV POETRY_VIRTUALENVS_CREATE=false \
    #POETRY_VERSION=1.4.0 \
    #PREFECT_HOME='~/.prefect' \
    #PREFECT_LOCAL_STORAGE_PATH='${PREFECT_HOME}/storage'

#RUN apt-get update && apt-get install -y --no-install-recommends \
    #wget \
    #git \
    #&& rm -rf /var/lib/apt/lists/*


#COPY pyproject.toml poetry.lock ./

#RUN pip install "poetry==$POETRY_VERSION" --no-cache-dir \
    #&& poetry config virtualenvs.create false  \
    #&& poetry install --without dev --no-root --no-cache \
    #&& playwright install firefox \
    #&& playwright install-deps firefox

#COPY . .

#ENTRYPOINT ["sh", "Deploy/entrypoint.sh"]
