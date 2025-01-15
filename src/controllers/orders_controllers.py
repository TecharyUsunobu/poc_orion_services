from flask import Blueprint, jsonify, request
from services.procurement_service import ProcurementService

orders_bp = Blueprint('orders', __name__)
procurement_service = ProcurementService()

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """Fetching order details from the Techary Procurement Portal"""
    try:
        orders = procurement_service.fetch_orders()
        return jsonify({"orders": orders}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
 
@orders_bp.route('/<order_id>', methods=['GET'])   
def get_order_by_id(order_id):
    """Fetching order details by order ID from the Techary Procurement Portal"""
    try:
        order = procurement_service.fetch_order_by_id(order_id)
        return jsonify({"order": order}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    