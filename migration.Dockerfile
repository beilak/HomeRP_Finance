FROM python:3.11.2-alpine3.17

WORKDIR /migration

RUN apk update
RUN pip install --no-cache-dir poetry==1.3.2

COPY poetry.lock pyproject.toml ./

RUN poetry env use python3 \
    && poetry install


COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

ENTRYPOINT ["poetry", "run", "alembic", "upgrade", "head"]
