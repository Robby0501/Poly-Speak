from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from app.routes.api import api_bp
from config import Config
import logging

def create_app(config_class=Config):
    app = Flask(__name__)

    # Set up logging for debugging
    logging.basicConfig(level=logging.DEBUG)

    # Configure CORS to allow requests from the frontend
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    app.config.from_object(config_class)

    # Register the API blueprint
    app.register_blueprint(api_bp)

    # Root route
    @app.route('/')
    def home():
        return "Welcome to the Poly Speak API"

    # Print all registered routes for verification
    with app.app_context():
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001) 