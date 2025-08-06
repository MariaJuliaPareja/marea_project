#Imports
from flask import Blueprint, render_template_string, current_app

# Create blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)