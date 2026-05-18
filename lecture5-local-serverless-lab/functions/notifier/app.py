from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    filename = data.get("filename")

    print(f"Notification: image processed successfully: {filename}", flush=True)

    return jsonify({
        "status": "success",
        "message": f"Notification sent for {filename}"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "notifier running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)