from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import pymysql
from extensions import mysql, mail

pymysql.install_as_MySQLdb()
load_dotenv()

app = Flask(__name__)
CORS(app)

# Secret keys
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

# MySQL credentials
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Initialize extensions
mysql.init_app(app)
mail.init_app(app)
jwt = JWTManager(app)

# Register routes
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp
CORS(auth_bp)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(todo_bp, url_prefix='/api/todo')

if __name__ == '__main__':
    app.run(debug=True)
