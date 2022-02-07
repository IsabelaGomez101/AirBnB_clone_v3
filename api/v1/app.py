#!/usr/bin/python3
"""Import package"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST') or '0.0.0.0'
port = getenv('HBNB_API_PORT') or 5000


@app.teardown_appcontext
def teardown(exception):
    """Function to call storage.close"""
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """Handler for 404 errors, returns a JSON-formatted 404"""
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    """Main function"""
    app.run(host=host, port=port, threaded=True)
