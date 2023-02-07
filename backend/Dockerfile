# Pull official latest Python Docker image

FROM python:3.11

# Set the working directory
WORKDIR /usr/backend

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy all backend files
COPY . .

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

# Execute entrypoint.sh
CMD ["sh", "/usr/backend/entrypoint.sh"]
