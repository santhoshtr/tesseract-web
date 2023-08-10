import os
import pathlib

import pdf2image
import pytesseract
from flask import Flask, jsonify, render_template, request
from langcodes import Language
from PIL import Image
from werkzeug.utils import secure_filename

__author__ = "Santhosh Thottingal <santhosh.thottingal@gmail.com>"
__source__ = "https://github.com/santhoshtr/tesseract-web"

app = Flask(__name__)
UPLOAD_FOLDER = "./static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["SUPPORTED_FORMATS"] = ["png", "jpeg", "jpg", "bmp", "pnm", "gif", "tiff", "webp", "pdf"]


def pdf_to_img(pdf_file):
    return pdf2image.convert_from_path(pdf_file)


def ocr_core(image: Image, language="en"):
    text = pytesseract.image_to_string(image, lang=Language.get(language).to_alpha3())
    return text


def pdf_to_text(pdf_file_path: str, language="en") -> str:
    texts = []
    images = pdf_to_img(pdf_file_path)
    for _pg, img in enumerate(images):
        texts.append(ocr_core(img, language))

    return "\n".join(texts)


def get_languages() -> dict:
    languages = {}
    alpha3codes = pytesseract.get_languages()
    for code in alpha3codes:
        language = Language.get(code)

        languages[language.language] = language.autonym()
    return languages


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", languages=get_languages())


@app.route("/api/languages", methods=["GET"])
def listSupportedLanguages():
    return jsonify(languages=get_languages())


@app.route("/api/ocr", methods=["POST"])
def ocr():
    f = request.files["file"]
    language = request.form.get("language", default="en")
    # create a secure filename
    filename = secure_filename(f.filename)
    file_extension = pathlib.Path(filename).suffix.split(".")[1]
    if file_extension not in app.config["SUPPORTED_FORMATS"]:
        return jsonify(error="File format not supported")

    # save file to /static/uploads
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(filepath)

    if file_extension == "pdf":
        # perform OCR on PDF
        text = pdf_to_text(filepath, language)
    else:
        # perform OCR on the processed image
        text = ocr_core(Image.open(filepath), language)

    # remove the processed image
    os.remove(filepath)

    return jsonify(text=text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
