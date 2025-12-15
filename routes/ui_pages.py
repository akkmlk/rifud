from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)

@pages.route('/')
def index():
    return render_template('user/index.html')

@pages.route('/register')
def register():
    return render_template('auth/register.html')

@pages.route('/login')
def login():
    return render_template('auth/login.html')