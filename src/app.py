from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from controllers.orders_controllers import orders_bp
from controllers.managed_services_controller import managed_service_bp
import config

app = Flask(__name__)
CORS(app)


#Cache Configuration
app.config.from_object(config.Config)

# Blueprint Registration
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(managed_service_bp, url_prefix='/api/managed_services')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

