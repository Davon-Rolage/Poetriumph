FROM postgres:15

LABEL maintainer="davon.rolage@gmail.com"
LABEL description="Postgres image for poetry.newa.fun"
LABEL version="1.0"

COPY *.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
