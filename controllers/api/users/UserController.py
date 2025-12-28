from flask import Blueprint, jsonify, request
import os
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from utils.res_wrapper import success_response, error_response
from models.user import get_profile, get_available_city, get_transactions_history, login, resto_registration, user_registration, get_order_history, get_order, put_profile
from werkzeug.security import check_password_hash, generate_password_hash

def profile_user(id):
    try:
        profile = get_profile(id)

        if not profile:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=profile)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def clean(value):
    return value if value not in ['', None] else None
    
def edit_profile_user(id):
    data = {
        "name": clean(request.form.get('name')),
        "phone": clean(request.form.get('phone')),
        "email": clean(request.form.get('email')),
        "address": clean(request.form.get('address')),
        "longitude": clean(request.form.get('longitude')),
        "latitude": clean(request.form.get('latitude')),
        "city": clean(request.form.get('city')),
        "open_time": clean(request.form.get('open_time')),
        "closed_time": clean(request.form.get('closed_time'))
    }

    password = request.form.get('password')
    if password:
        data['password'] = generate_password_hash(password)

    UPLOAD_FOLDER = 'static/uploads/users'
    foto_path = None

    foto = request.files.get('foto')
    if foto:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        ext = foto.filename.rsplit('.', 1)[-1]
        filename = f"{uuid4().hex}.{ext}"
        filename = secure_filename(filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        foto.save(save_path)

        foto_path = f"uploads/users/{filename}"
        data['foto'] = foto_path

    try:
        user = put_profile(id, data)
        
        if not user:
            return error_response("Data gagal updateeeeee", res_code=404)
        
        return success_response(data=user)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def available_city():
    try:
        citys = get_available_city()

        if not citys:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=citys)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def transactions_history(id):
    try:
        transactions_history = get_transactions_history(id)

        if not transactions_history:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=transactions_history)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def order(resto_id):
    try:
        order = get_order(resto_id)

        if not order:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=order)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def order_history(resto_id):
    try:
        order_history = get_order_history(resto_id)

        if not order_history:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=order_history)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

    
def login_proccess():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Email dan Password wajib diisi", 400)
    
    user = login(email)
    if not user:
        return error_response("User tidak ada", 404)
    
    if not check_password_hash(user['password'], password):
        return error_response("Password salah", 401)
    
    return success_response("Login berhasil", data=user, res_code=200)

def resto_registration_proccess():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    city = data.get('city')
    address = data.get('address')
    role = "resto"

    if not email or not password or not name or not city or not address:
        return error_response("Wajib mengisi semua data", res_code=400)
    
    hashed_password = generate_password_hash(password)
    user = resto_registration(email, hashed_password, name, city, address, role)
    
    if not user:
        return error_response("Gagal daftar", res_code=404)
    
    return success_response("Daftar berhasil", data=user, res_code=200)

def user_registration_proccess():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Wajib mengisi semua data", res_code=400)
    
    hashed_password = generate_password_hash(password)
    user = user_registration(name, email, hashed_password)
    
    if not user:
        return error_response("Gagal daftar", res_code=404)
    
    return success_response("Daftar berhasil", data=user, res_code=200)