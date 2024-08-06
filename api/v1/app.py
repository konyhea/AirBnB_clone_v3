#!/usr/bin/python3
"""Creating app with Flask and Blueprint app_views"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Teardown function to close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors and return JSON response"""
    response = {
            "error": "Not found"
    }
    return jsonify(response), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
