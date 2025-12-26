import os
from datetime import timedelta
from flask import url_for
from extensions import mysql
from MySQLdb.cursors import DictCursor

def get_profile(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    profile = cur.fetchone()
    cur.close()

    if profile.get('open_time'):
        profile['open_time'] = str(profile['open_time'])
    if profile.get('closed_time'):
        profile['closed_time'] = str(profile['closed_time'])

    return profile

def put_profile(id, data):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT foto FROM users WHERE id = %s", (id,))
    old_data = cur.fetchone()
    old_foto = old_data['foto'] if old_data else None

    foto = data.get('foto')
    if foto:
        if old_foto:
            old_path = os.path.join("static", old_foto)
            if os.path.exists(old_path):
                os.remove(old_path)

    fields = []
    params = []

    for key, value in data.items():
        if value is not None:
            fields.append(f"{key} = %s")
            params.append(value)

    if not fields:
        return None
    
    query = f"""
                UPDATE users SET {', '.join(fields)}
                WHERE id = %s
        """
    params.append(id)

    cur.execute(query, tuple(params))
    mysql.connection.commit()
    
    cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
    user = cur.fetchone()
    cur.close()

    if user.get('foto'):
        user['foto_url'] = (url_for('static', filename=user['foto'], _external=True))
    else:
        user['foto_url'] = None

    if isinstance(user.get('open_time'), timedelta):
        user['open_time'] = str(user['open_time'])
    if isinstance(user.get('closed_time'), timedelta):
        user['closed_time'] = str(user['closed_time'])

    return user

def get_available_city():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT DISTINCT city FROM users ORDER BY city ASC")
    citys = cur.fetchall()
    cur.close()
    return citys

def get_transactions_history(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT 
            users.foto AS foto_resto,
            transactions.id AS id_transaction,
            food_waste.name AS name,
            food_waste.foto AS foto_fw,
            food_waste.description AS description,
            transactions.status AS status,
            transactions.price_total AS price_total,
            CONCAT(
                CASE DAYNAME(transactions.transaction_date)
                    WHEN 'Monday' THEN 'Senin'
                    WHEN 'Tuesday' THEN 'Selasa'
                    WHEN 'Wednesday' THEN 'Rabu'
                    WHEN 'Thursday' THEN 'Kamis'
                    WHEN 'Friday' THEN 'Jumat'
                    WHEN 'Saturday' THEN 'Sabtu'
                    WHEN 'Sunday' THEN 'Minggu'
                END,
                ', ',
                DATE_FORMAT(transactions.transaction_date, '%%H:%%i:%%s')
            ) AS transaction_date
        FROM transactions
        JOIN food_waste ON transactions.food_waste_id = food_waste.id
        JOIN users ON transactions.user_id = users.id
        WHERE users.id = %s 
                AND transactions.status IN ('success', 'cancel')
        ORDER BY transactions.transaction_date ASC
    """, (id,))
    transactions_history = cur.fetchall()
    cur.close()
    return transactions_history

def login(email):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT id, name, phone, email, password, address FROM users WHERE email = %s", (email, ))
    data = cur.fetchone()
    cur.close()
    return data

def resto_registration(email, password, name, city, address, role):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("INSERT INTO users (email, password, name, city, address, role) VALUES (%s, %s, %s, %s, %s, %s)", (email, password, name, city, address, role))
    mysql.connection.commit()

    user_id = cur.lastrowid
    cur.execute("SELECT id, name, email, password, city, address, role FROM users WHERE id = %s", (user_id, ))
    user = cur.fetchone()
    cur.close()
    return user

def user_registration(name, email, password):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password, ))
    mysql.connection.commit()

    user_id = cur.lastrowid
    cur.execute("SELECT id, name, email, password FROM users WHERE id = %s", (user_id, ))
    user = cur.fetchone()
    cur.close()
    return user

def get_order(resto_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""SELECT 
                transactions.id, 
                food_waste.foto, 
                food_waste.type, 
                users.name AS pembeli, 
                food_waste.name AS fw_name, 
                transactions.qty, 
                transactions.price_total, 
                transactions.payment_type, 
                transactions.status 
                FROM transactions 
                JOIN users ON transactions.user_id = users.id 
                JOIN food_waste ON transactions.food_waste_id = food_waste.id 
                WHERE food_waste.user_id = %s 
                AND transactions.status IN ('waiting', 'ready')
                ORDER BY transactions.transaction_date DESC""", (resto_id, ))
    order = cur.fetchall()
    cur.close()
    return order

def get_order_history(resto_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""SELECT 
                transactions.id, 
                food_waste.foto, 
                food_waste.type, 
                users.name AS pembeli, 
                food_waste.name AS fw_name, 
                transactions.qty, 
                transactions.price_total, 
                transactions.payment_type, 
                transactions.status 
                FROM transactions 
                JOIN users ON transactions.user_id = users.id 
                JOIN food_waste ON transactions.food_waste_id = food_waste.id 
                WHERE food_waste.user_id = %s 
                AND transactions.status IN ('success', 'declined')
                ORDER BY transactions.transaction_date DESC""", (resto_id, ))
    order_history = cur.fetchall()
    cur.close()
    return order_history