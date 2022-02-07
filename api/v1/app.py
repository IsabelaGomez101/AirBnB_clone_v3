#!/usr/bin/python3
"""Import package"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown():
    """Function to call storage.close"""
    storage.close()

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

threaded=True

if __name__ == "__main__":
    """Main function"""
    app.run(host=host, port=port)
