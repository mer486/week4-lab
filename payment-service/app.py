from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "payment-service", "status": "up"}), 200

@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    order_id = data.get("order_id")
    amount = data.get("amount")

    if order_id is None or amount is None:
        return jsonify({"error": "order_id and amount are required"}), 400

    return jsonify({
        "message": "Payment successful",
        "order_id": order_id,
        "amount": amount,
        "payment_status": "paid"
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)