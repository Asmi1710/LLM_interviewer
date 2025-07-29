from flask import Flask
from app.config import configure_app
from app.db import init_db
from app.routes import initialize_routes
from app.exceptions import configure_exception_handler
from app.cors import init_cors

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)
    init_db(app)
    initialize_routes(app)
    configure_exception_handler(app)
    init_cors(app)

    # Autocomplete in flask shell
    import readline
    readline.parse_and_bind('tab:complete')

    return app