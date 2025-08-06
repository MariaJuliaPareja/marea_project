#Imports
from flask import Flask
from flask_cors import CORS
import os
import sys

#Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#Creating function for the main app
def create_app():
    # Flask application
    app = Flask(__name__)
    CORS(app)
    # Configuration
    app.config['DATABASE_PATH'] = 'data/marea_data.db'
    # Initialize components
    init_components(app)
    # Register modular routes
    register_blueprints(app)
    return app