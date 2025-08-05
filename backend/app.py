#Imports
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import json
import time
from datetime import datetime
import os

#Flask application
app = Flask(__name__)
CORS(app)

