import os
import time
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:5001")

def fetch_product_with_retry(product_id, retries=3, delay=1):
    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=2)

            if response.status_code == 200:
                return response.json()

            if response.status_code == 404:
                return None

        except requests.RequestException:
            pass

        if attempt < retries - 1:
            time.sleep(delay)

    raise Exception("product-service unavailable")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "order-service", "status": "up"}), 200

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if product_id is None or quantity is None:
        return jsonify({"error": "product_id and quantity are required"}), 400

    try:
        product = fetch_product_with_retry(product_id)
    except Exception:
        return jsonify({"error": "product-service unavailable"}), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    total_price = product["price"] * quantity

    return jsonify({
        "message": "Order created",
        "product": product["name"],
        "quantity": quantity,
        "total_price": total_price
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)