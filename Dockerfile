# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 9020

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=9020

# Install system packages required by Wagtail and Django.
RUN apt-get update && \
    apt-get install --yes --quiet --no-install-recommends \
        build-essential \
        libpq-dev \
        libmariadbclient-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libwebp-dev && \
        rm -rf /var/lib/apt/lists/* && \
    pip3 install daphne

# Install the application server.
RUN pip3 install daphne

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /opt/FPN_Backend

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

COPY . /opt/FPN_Backend

WORKDIR /opt/FPN_Backend

# Install the project requirements.
RUN pip3 install -r /opt/FPN_Backend/requirements.txt

RUN pip3 install psycopg2

WORKDIR /opt/FPN_Backend/FPN_Backend

# # Copy the source code of the project into the container.
# COPY --chown=wagtail:wagtail . .

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

ENV DB_NAME="defaultdb"
ENV DB_USER="doadmin"
ENV DB_PASSWORD="guo0iehm170wgmxw"
ENV DB_HOST="db-postgresql-fpn-api-do-user-8133290-0.b.db.ondigitalocean.com"
ENV DB_PORT="25060"

ENV ALLOWED_HOSTS="127.0.0.1,localhost,172.17.0.1,api.thefinpro.net,167.172.168.48"
ENV DURATION='600'
ENV ROOT_SECRET="C9euClrULxcXghvIAf60VGkSESF6c5U7meVgD4tCEfGakZZH9l67eE7N2a3rFfi0IA6"

CMD ["daphne", "-b", "0.0.0.0", "-p", "9020", "FPN_Backend.asgi:application"]
