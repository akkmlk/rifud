from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)

@pages.route('/')
def index():
    return render_template('user/index.html')

@pages.route('/riwayat_transaksi')
def riwayat_transaksi():
    return render_template('user/riwayat_transaksi.html')

@pages.route('/riwayat_pesanan')
def riwayat_pesanan():
    return render_template('resto/riwayat_pesanan.html')

@pages.route('/daftar_pesanan')
def daftar_pesanan():
    return render_template('resto/daftar_pesanan.html')

@pages.route('/register')
def register():
    return render_template('auth/register.html')

@pages.route('/login')
def login():
    return render_template('auth/login.html')

@pages.route('/daftar')
def daftar():
    return render_template('resto/index.html')

@pages.route('/tambah')
def tambah():
    return render_template('resto/add.html')

@pages.route('/edit')
def edit():
    return render_template('resto/edit.html')