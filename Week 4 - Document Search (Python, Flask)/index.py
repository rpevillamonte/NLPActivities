from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from EntityDetector import EntityDetector
import json
import os

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = str(os.getcwd()) + '\\PDFs'

app.secret_key = 'key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['pdfUpload']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)
    ed = EntityDetector()
    ed.process_to_json()
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_json():
    path = str(os.getcwd()) + '\\entities.json'
    with open(path) as file:
        data = json.load(file)
    pdfs = []
    term = request.form['term']
    for k,v in data.items():
        included = False
        entity_list = v
        for d in entity_list:
            if term == d['entity'] and included == False:
                pdfs.append(k)
                included = True
    return jsonify({'results' : pdfs})
                

app.run(debug=True)