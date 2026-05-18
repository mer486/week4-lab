from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

INPUT_DIR = "/data/input"
OUTPUT_DIR = "/data/output"


@app.route("/thumbnail", methods=["POST"])
def create_thumbnail():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "filename is required"}), 400

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, f"thumbnail_{filename}")

    try:
        with Image.open(input_path) as img:
            img = img.resize((100, 100))
            img.save(output_path)

        print(f"Thumbnail saved: {output_path}", flush=True)
        return jsonify({"status": "success", "output": output_path}), 200

    except Exception as e:
        print(f"Thumbnail error: {e}", flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "thumbnail running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)