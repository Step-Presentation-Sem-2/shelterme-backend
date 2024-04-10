FROM python:3.11-slim
WORKDIR /app
COPY . /app

# Update and install system packages required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN cat Requirements.txt  # Print the contents of requirements.txt for debugging
RUN pip install -r Requirements.txt
LABEL image.name=$IMAGE_NAME
