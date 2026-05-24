# pull official base image
#FROM docker.arvancloud.ir/python:3.12-slim-bullseye
FROM python:3.12-slim-bullseye
# maintainers info
LABEL maintainer="bigdeli.ali3@gmail.com"

ENV PYTHONUNBUFFERED=1 \
    PIP_INDEX_URL=https://mirror-pypi.runflare.com/simple

# Install Nginx using internal mirrors
RUN sed -i 's|http://deb.debian.org/debian|http://mirror.arvancloud.ir/debian|g' /etc/apt/sources.list \
 && sed -i 's|http://security.debian.org/debian-security|http://mirror.arvancloud.ir/debian-security|g' /etc/apt/sources.list

RUN apt-get update -o Acquire::Check-Valid-Until=false \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /usr/src/app

# install dependencies using internal Python mirror
COPY ./requirements.txt .
RUN pip install --upgrade pip  \
    && pip install -r requirements.txt

# Set up Gunicorn
COPY ./core .

# Configure Nginx
COPY ./dockerfiles/prod/django/nginx/nginx.conf /etc/nginx/nginx.conf

# exposing nginx port
EXPOSE 80

# copy entrypoint
COPY ./dockerfiles/prod/django/entrypoint.sh .

# make entrypoint executable
RUN chmod +x ./entrypoint.sh

# execute entrypoint
CMD ["./entrypoint.sh", "python3", "ruserver", "0.0.0.0.8000"]