# Imports
from flask import Blueprint, request, jsonify, current_app
import time

# Create blueprint for API routes
api_bp = Blueprint('api', __name__)


@api_bp.route('/sensor-data', methods=['POST'])
