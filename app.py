from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database('Users') 

class MyUser(UserMixin):
    def __init__(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({'_id': user_id})
    if user:
        return MyUser(user['_id'], user['email'], user['username'], user['password'])
    return render_template('welcome_user')

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
        user = MyUser(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.users.insert_one({'email': user.email, 'username': user.username, 'password': user.password})
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
        if user is not None and user['password'] == form.password.data:
            user_obj = MyUser(user['_id'], user['email'], user['username'], user['password'])
            login_user(user_obj)
            flash("您已經成功的登入系統")
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('welcome_user')
            return redirect(next_page)
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
