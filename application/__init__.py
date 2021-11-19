from flask import Flask
from flask_bootstrap import Bootstrap
from decouple import config

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config['SECRET_KEY'] = config('SECRET_KEY')

    with app.app_context():
        from . import main  # Import routes

        return app
        