import os
from flask_cors import CORS

def init_cors(app):
    app.config['CORS_ORIGINS'] = ['http://localhost:3000', 'https://voicruit.com']
    app.config['CORS_METHODS'] = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
    CORS(app)
