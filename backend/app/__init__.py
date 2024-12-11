from flask import Flask
from .routes import main_blueprint

def create_app():
    app = Flask(__name__)

    # Session configuration
    # app.config['SESSION_TYPE'] = 'filesystem'
    # app.secret_key = 'supersecretkey'  # Replace with your secret key
    # Session(app)

    app.register_blueprint(main_blueprint)
    return app
