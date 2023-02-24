from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys
from PIL import Image
import pytesseract

__author__ = 'Santhosh Thottingal <santhosh.thottingal@gmail.com>'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route('/', methods = ['GET', 'POST'])
def index():
     languages = pytesseract.get_languages()
     return render_template("index.html", languages=languages)

@app.route('/api/languages', methods = ['GET'])
def listSupportedLanguages():
    languages = pytesseract.get_languages()
    return jsonify(languages=languages)

@app.route('/api/ocr', methods = ['POST'])
def ocr():
    f = request.files['file']
    language = request.form.get("language", default="eng")
    # create a secure filename
    filename = secure_filename(f.filename)

    # save file to /static/uploads
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    f.save(filepath)


    # perform OCR on the processed image
    text = pytesseract.image_to_string(Image.open(filepath), lang=language)

    # remove the processed image
    os.remove(filepath)

    return jsonify(text=text)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)
