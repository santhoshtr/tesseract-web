# Tesseract OCR web interface

Supports scanning images and pdfs.

Use prebuilt docker image:
```
docker run -p 3000:80 ghcr.io/santhoshtr/tesseract-ocr-web:latest
```
Open http://0.0.0.0:3000/ using browser

OR

Checkout this repository and
```
docker build -t tesseract-ocr .
docker run -dp 3000:80 tesseract-ocr:latest
```
then
Open http://0.0.0.0:3000/ using browser
