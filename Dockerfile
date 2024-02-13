FROM python:3.8.10-slim
WORKDIR /app
COPY . /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN cat Requirements.txt  # Print the contents of requirements.txt for debugging
RUN pip install -r Requirements.txt
LABEL image.name=$IMAGE_NAME
