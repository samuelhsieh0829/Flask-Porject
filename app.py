from bson import ObjectId
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin
from pymongo import MongoClient
from myproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import sys

sys.dont_write_bytecode = True

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database('Users')
print(client)
class MyUser(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.username = user_data['username']
        self.password_hash = user_data['password_hash']

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return MyUser(user_data)
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已經登出系統")
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = {
            'email': form.email.data,
            'username': form.username.data,
            'password_hash': hashed_password
        }
        db.users.insert_one(user)
        flash("感謝註冊本系統成為會員")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.find_one({'email': form.email.data})
        if user and check_password_hash(user['password_hash'], form.password.data):
            user_obj = MyUser(user)
            login_user(user_obj)
            flash("您已經成功的登入系統")
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('welcome_user')
            return redirect(next_page)
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
