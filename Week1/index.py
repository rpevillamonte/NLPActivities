from flask import Flask, request, jsonify, render_template
from predictWord import predict

import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def get_suggestions():
    
    text = request.form['text']
        
    return jsonify({'counts' : predict(text)})
                
app.run(debug=True)