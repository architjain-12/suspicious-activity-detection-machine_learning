from flask import Flask

UPLOAD_FOLDER = 'E:/sih/AnomalyDetection_CVPR18/output/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
