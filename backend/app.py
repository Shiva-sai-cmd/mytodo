from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import pymysql
import os

from config import Config
from extensions import mysql, mail

pymysql.install_as_MySQLdb()
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
mysql.init_app(app)
mail.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(todo_bp, url_prefix='/api/todo')

if __name__ == '__main__':
    app.run(debug=os.getenv("FLASK_DEBUG", True))
