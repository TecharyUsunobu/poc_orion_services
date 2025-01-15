from flask import Flask
from flask_cors import CORS
from flask_caching import Cache


app = Flask(__name__)
CORS(app)


#Cache Configuration
app.config.from_object()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)