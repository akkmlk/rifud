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

@pages.route('/daftar')
def daftar():
    return render_template('resto/index.html')

@pages.route('/tambah')
def tambah():
    return render_template('resto/add.html')

@pages.route('/edit')
def edit():
    return render_template('resto/edit.html')

@pages.route('/dashboard')
def frameset():
    return render_template('resto/frameset.html')

@pages.route('/navbar')
def navbar():
    return render_template('resto/navbar.html')

@pages.route('/sidebar')
def sidebar():
    return render_template('resto/sidebar.html')
@pages.route('/produk')
def produk():   
    return render_template('resto/produk.html')
@pages.route('/pesanan')
def pesanan():
    return render_template('resto/pesanan.html')
@pages.route('/riwayat_pesanan')
def riwayat_pesanan():
    return render_template('resto/riwayat_pesanan.html')

# @pages.route('/register-resto')
# def register_resto():
#     return render_template('auth/regist_resto.html')

@pages.route('/home-resto')
def home_resto():
    return render_template('resto/home.html')

