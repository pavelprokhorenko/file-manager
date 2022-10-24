# Dockerfile

FROM python:3.10-buster

# copy source and install dependencies
RUN mkdir -p /opt/app

COPY . /opt/app

WORKDIR /opt/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /opt/app

# start service
STOPSIGNAL SIGTERM
CMD ["bash", "start-server.sh"]
