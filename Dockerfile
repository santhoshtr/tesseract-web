FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get -y install tesseract-ocr tesseract-ocr-all poppler-utils\
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]

EXPOSE 80