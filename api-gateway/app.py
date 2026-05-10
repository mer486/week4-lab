import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:5001")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:5002")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:5003")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "api-gateway", "status": "up"}), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    return jsonify(response.json()), response.status_code

@app.route("/orders", methods=["POST"])
def create_order():
    response = requests.post(f"{ORDER_SERVICE_URL}/orders", json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route("/payments", methods=["POST"])
def create_payment():
    response = requests.post(f"{PAYMENT_SERVICE_URL}/payments", json=request.get_json())
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)