#landing page = 127.0.0.1:5000
from flask import Flask
from flask import request, render_template
import joblib

app = Flask(__name__)


#model = joblib.load('modelName.pkl')

@app.route('/')
def landing():
    return render_template('landing.html', landing_image = '/static/LandingExample.png')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/data/sample')
def sample():
    info = ['/static/LandingExample.png', '/static/LandingExample.png', '/static/LandingExample.png']
    return render_template('sample.html', samples = info)

@app.route('/test')
def predict():
    return render_template('prediction.html')
