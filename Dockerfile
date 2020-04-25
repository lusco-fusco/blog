FROM fnndsc/ubuntu-python3:latest
LABEL maintainer = "Andrea Magan <andrea.magan@outlook.com>, Luis Lorenzo <luis.lorenzom@outlook.com>"

# Arguments
ARG PORT
ARG HOST
ARG CSRF_ENABLED
ARG DEBUG
ARG SECRET_KEY
ARG MIGRATION_PATH
ARG DATABASE_HOST
ARG DATABASE_PORT
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG SQLALCHEMY_TRACK_MODIFICATIONS

# Environment
ENV LANG C.UTF-8

ENV PORT=${PORT}
ENV HOST=${HOST}
ENV CSRF_ENABLED=${CSRF_ENABLED}
ENV DEBUG=${DEBUG}
ENV SECRET_KEY=${SECRET_KEY}
ENV MIGRATION_PATH=${MIGRATION_PATH}
ENV DATABASE_HOST=${DATABASE_HOST}
ENV DATABASE_PORT=${DATABASE_PORT}
ENV DATABASE_NAME=${DATABASE_NAME}
ENV DATABASE_USER=${DATABASE_USER}
ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}
ENV SQLALCHEMY_TRACK_MODIFICATIONS=${SQLALCHEMY_TRACK_MODIFICATIONS}

# Install mysql client, will be used to ping mysql
RUN apt-get update && apt-get -y install libpq-dev

# Upgrade pip
RUN pip install --upgrade pip

# Download Source Code
WORKDIR /home/luscofusco/
ENV HOME /home/luscofusco
COPY . ${HOME}

# Install python dependencies
RUN pip install -r requirements.txt

# Define entrypoint
ENTRYPOINT ["python3.6", "app.py"]