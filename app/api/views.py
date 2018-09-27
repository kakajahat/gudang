from flask import jsonify
from json import dumps
from flask_login import login_required, current_user

from . import api
from ..models import Inventory

@api.route('/api/', methods=['GET'])
def api_home():
    return "API"

@api.route('/api/inventory', methods=['GET'])
def api_inventory():
    inventory = Inventory.query.all()
    return jsonify([i.serialize for i in inventory])

