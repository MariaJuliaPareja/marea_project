#Imports
from flask import Flask
from flask_cors import CORS
import os
import sys

#Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#Creating function for the main app
def create_app():
    #Flask application
    app = Flask(__name__)
    CORS(app)
    #Configuration
    app.config['DATABASE_PATH'] = 'data/marea_data.db'
    #Initialize components
    init_components(app)
    #Register modular routes
    register_blueprints(app)
    return app

#Function to initializate the database and components
def init_components(app):
    
    # Import your database class
    from models.database import MAREADatabase
    
    app.db = MAREADatabase(app.config['DATABASE_PATH'])    
    print("Components initialized")
    print(f"Database: {app.config['DATABASE_PATH']}")

#Function to register all modular routes
def register_blueprints(app):
    
    # Import blueprints from routes
    from routes.api_routes import api_bp
    from routes.dashboard_routes import dashboard_bp
    
    # Register with prefixes
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    
    print("Routes registered:")
    print("API: /api/*")
    print("Dashboard: /*")

if __name__ == '__main__':
    app = create_app()
    #As we don't have a custom Cloud, we will compile this on this localhost directions
    print("PetroSentry Backend ")
    print("=" * 40)
    print("Dashboard: http://localhost:8000")
    print("API: http://localhost:8000/api/")
    print("Modular structure loaded")
    print("=" * 40)
    
    # Run server
    app.run(host='0.0.0.0', port=8000, debug=True)