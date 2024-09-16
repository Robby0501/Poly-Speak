from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask import g
from flask_cors import CORS
from app.routes.api import api_bp
from config import Config
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import logging

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import your models
from app.models.user import User

# Create tables
Base.metadata.create_all(bind=engine)

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
    
    @app.before_request
    def before_request():
        g.db = SessionLocal()
    
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    # Print all registered routes for verification
    with app.app_context():
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001) 