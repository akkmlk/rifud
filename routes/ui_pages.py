from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)

@pages.route('/')
def index():
    return render_template('user/index.html')

@pages.route('/register')
def register():
    return render_template('auth/register.html')

@pages.route('/register-resto')
def register_resto():
    return render_template('auth/register_resto.html')

@pages.route('/login')
def login():
    return render_template('auth/login.html')

@pages.route('/profile')
def profile():
    return render_template('shared/profile.html')


@pages.route('/order-history')
def order_history():
    return render_template('user/order_history.html')