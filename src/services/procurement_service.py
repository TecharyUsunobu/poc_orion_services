from woocommerce import API
import os

# Initializing WooCommerce API
wcapi = API(
    url="https://portalstage.techary.com/",
    consumer_key=os.getenv('WOO_CONSUMER_KEY'),
    consumer_secret=os.getenv('WOO_CONSUMER_SECRET'),
    timeout=30
)

class ProcurementService:
    def __init__(self):
        self.base_url = "https://portalstage.techary.com/"
        
    def fetch_orders(self):
        response = wcapi.get('orders', params={"per_page": 100})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch orders: {response.text}")
        
    def fetch_order_by_id(self, order_id):
        response = wcapi.get(f'orders/{order_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch order: {response.text}")
        
    def fetch_products(self):
        response = wcapi.get('products')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch products: {response.text}")