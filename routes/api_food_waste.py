from flask import Blueprint, jsonify, request
from utils.res_wrapper import success_response, error_response

food_waste_api = Blueprint("food_waste_api", __name__)

@food_waste_api.route('/api/food-waste')
def get_food():
    return success_response(data="belum ada data", message="ok")