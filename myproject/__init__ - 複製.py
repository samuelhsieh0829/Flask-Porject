import os
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

client = MongoClient(os.environ.get('MONGODB_URI'))

db = client.get_database('Users')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
