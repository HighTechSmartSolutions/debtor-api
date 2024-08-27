FROM python:3.10-bullseye

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc git \
    && apt install netcat-traditional \
    && curl https://packages.microsoft.com/keys/microsoft.asc | \
    tee /etc/apt/trusted.gpg.d/microsoft.asc\
    && curl https://packages.microsoft.com/config/debian/11/prod.list | \
    tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir /app/static
RUN mkdir /app/staticfiles

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]