from dotenv import load_dotenv
from flask import Flask, jsonify, request
from procurement.procurement import wcapi
from it_systems.halo_service import get_halo_token, get_halo_agent_details, get_client_details
import requests
from flask_cors import CORS
from flask_caching import Cache

app = Flask(__name__)
CORS(app)


# Cache Configuration
app.config['CACHE_TYPE'] = 'SimpleCache' # Would use something like RedisCache or MemcachedCache in production
app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Cache timeout in seconds (5 minutes)
cache = Cache(app)

# Fetching orders from WooCommerce 
@app.route('/api/orders/techary', methods=['GET'])
@cache.cached()
def get_orders():
    """Fetching order details from the Techary Procurement Portal"""
    try:
        response = wcapi.get("orders", params={"per_page": 100})
        if response.status_code == 200:
            orders = response.json()
            
            # Extracting specific fields from each order
            order_data = []
            for order in orders:
                order_info = {
                    "order_id": order.get("id"),
                    "billing_company": order["billing"].get("company"),
                    "total": order.get("total"),
                    "line_items": [],
                    "po_number": order.get("transaction_id"), 
                    "status": order.get("status"),
                    "date_paid": order.get("date_paid"),
                    "first_name": order["billing"].get('first_name'),
                    "last_name": order["billing"].get('last_name'),
                    "currency_symbol": order.get('currency_symbol')
                    
                }
                
                #Getting line items (product details)
                for item in order.get("line_items", []):
                    line_item_info = {
                        "name": item.get("name"),
                        "quantity": item.get("quantity"),
                        "sku": item.get("sku"),
                        "total": item.get("total")
                    }
                    order_info["line_items"].append(line_item_info)
                order_data.append(order_info)
                
            print(len(orders))
            # Returning the filtered mapped orders  
            return jsonify({"orders": order_data, "order_number": len(order_info) }), 200
        else:
            return jsonify({"error": "Failed to fetch orders", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": "An error ocurred while fetching orders", "details": str(e)}), 500


# Fetching a list of stock from WooCommerce
@app.route('/api/products', methods=['GET'])
def get_products():
    """Fetching Products available from the Techary Procurement Portal"""
    try:
        response = wcapi.get('products')
        if response.status_code == 200:
            product_list = response.json()
            
            # Extracting data
            product_data = []
            for product in product_list:
                product_info = {
                    "product_id": product.get('id'),
                    "name": product.get('name'),
                    "sku": product.get('sku'),
                    "price": product.get('price'),
                    
                }
                
                product_data.append(product_info)
            
            return jsonify({"products": product_data}), 200
        else:
            return jsonify({"error": "Failed to fetch orders", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": "An error ocurred while fetching orders", "details": str(e)}), 500
    


# Fetching Techary tickets from HaloPSA
@app.route('/api/tickets/<client_name>/<ticket_category>', methods=['GET'])
@cache.cached()
def get_tickets_for_techary(client_name, ticket_category):
    """Fetching tickets from HaloPSA using the access token"""
    
    # Get client details
    client_id = get_client_details(client_name)
    if isinstance(client_id, dict) and client_id.get("error"):
        return jsonify({"error": "Failed to fetch client details", "details": client_id}), 500
    
    print(client_name)
    # Getting HaloPSA OAuth2 access token
    access_token = get_halo_token()
    if not access_token:
        return jsonify({"error": "Failed to fetch access token"})
    
    # HaloPSA tickets endpoints
    tickets_url = "https://jarvis.techary.com/api/Tickets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Query Parameters
    query_params ={
        "client_id": client_id,
        "page_size": 50,
        "page_no": 2,
        "order": "ticket_id",
        "open_only": True,
        "search": ticket_category,
    }
    
   
    
    try:
        # Making the request to fetch tickets from techary
        response = requests.get(tickets_url, headers=headers, params=query_params)
        if response.status_code == 200:
            ticket_response = response.json()
            
            ticket_list = ticket_response.get("tickets", [])
            
            # Processing ticket data
            ticket_data = []
            for ticket in ticket_list:
                ticket_info = {
                    "ticket_id": ticket.get("id"), 
                    "category": ticket.get('category_1'),
                    "id_summary": ticket.get("idsummary"), 
                    "summary": ticket.get("summary"),
                    "end_user": ticket.get("user_name"),
                    "assigned_agent": get_halo_agent_details(ticket.get('agent_id')),
                    # "details": ticket.get('details'), 
                }
                ticket_data.append(ticket_info)
            
            
            print(len(ticket_list))
            return jsonify({"tickets": ticket_data, "total_open_tickets": len(ticket_list)}), 200
        else:
            return jsonify({"error": "Failed to fetch tickets", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": "An error ocurred while fetching tickets", "details": str(e)}), 500






# Creating a ticket







if __name__ == '__main__':
    app.run(debug=True)