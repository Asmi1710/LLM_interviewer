import os
from flask_cors import CORS

def init_cors(app):
    app.config['CORS_ORIGINS'] = ['*']
    app.config['CORS_METHODS'] = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
    app.config['CORS_EXPOSE_HEADERS'] = ['access-token']
    CORS(app)
