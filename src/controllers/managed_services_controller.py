from flask import Blueprint, jsonify, request
from services.managed_services import ManagedServices

managed_service_bp = Blueprint('managed_services', __name__)
managed_services = ManagedServices()

@managed_service_bp.route('/tickets/<client_name>/<ticket_category>', methods=['GET'])
def get_customer_tickets(client_name, ticket_category):
    """Fetching tickets from HaloPSA using the access token"""
    results = managed_services.get_tickets_for_techary(client_name, ticket_category)
    if "error" in results:
        return jsonify(results), 500
    return jsonify(results), 200