# Dockerfile

FROM python:3.10-bullseye

# copy source and install dependencies
ENV VIRTUAL_ENV=/venv
RUN python3.10 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# start service
STOPSIGNAL SIGTERM
CMD ["sh", "start-server.sh"]
