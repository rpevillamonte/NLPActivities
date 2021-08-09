from flask import Flask, request, jsonify, render_template
import os
from chunker import process_content

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan-sentence', methods=['POST'])
def scan():
    text = request.form['text_input']
    
    return jsonify({'result' : process_content(text)})

app.run(debug=True)