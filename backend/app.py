from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import pymysql
import os

from config import Config
from extensions import mysql, mail

# Use pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables from .env file (for local development)
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Load config from Config class
app.config.from_object(Config)

# Initialize extensions
mysql.init_app(app)
mail.init_app(app)
jwt = JWTManager(app)

# Register blueprints
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp

CORS(auth_bp)  # Optional: CORS for individual blueprint
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(todo_bp, url_prefix='/api/todo')

# Run the app (for local use)
if __name__ == '__main__':
    app.run(debug=True)
