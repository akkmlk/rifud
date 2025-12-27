from flask import Blueprint, jsonify, request
from utils.res_wrapper import success_response, error_response

food_waste_api = Blueprint("food_waste_api", __name__)

locations = [
    {"id": 1, "name": "Shell Jatiwaringin", "lat": -6.2547, "lng": 106.9129, "addr": "Jl. Jatiwaringin Raya, Jakarta"},
    {"id": 2, "name": "Shell Pondok Gede", "lat": -6.2698, "lng": 106.9021, "addr": "Jl. Raya Jatiwaringin, Bekasi"},
    {"id": 3, "name": "Shell Wibawa Mukti", "lat": -6.2620, "lng": 106.9480, "addr": "Jl. Wibawa Mukti, Bekasi"},
    {"id": 4, "name": "Shell Cibubur", "lat": -6.3600, "lng": 106.8820, "addr": "Jl. Raya Cibubur, Jakarta Timur"},
    {"id": 5, "name": "Shell Depok", "lat": -6.3910, "lng": 106.8310, "addr": "Depok, Jawa Barat"}
]


@food_waste_api.route('/api/food-waste')
def get_food():
    return success_response(data="belum ada data", message="ok")

@food_waste_api.route('/api/locations')
def api_location():
    return jsonify(locations)