import os
from flask import Flask, jsonify, request
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESIZED_FOLDER = "resized"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESIZED_FOLDER, exist_ok=True)

EVENT_IMAGE_RESIZED = "image.resized"
EVENT_IMAGE_THUMBNAIL_CREATED = "image.thumbnail.created"


def resize_image(input_path, output_path):
    with Image.open(input_path) as img:
        img.thumbnail((300, 300))
        img.save(output_path)


def create_thumbnail(input_path, output_path):
    with Image.open(input_path) as img:
        img.thumbnail((100, 100))
        img.save(output_path)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "image-service", "status": "up"}), 200


@app.route("/images", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "image file is required"}), 400

    image = request.files["image"]
    filename = image.filename

    original_path = os.path.join(UPLOAD_FOLDER, filename)
    resized_path = os.path.join(RESIZED_FOLDER, f"resized_{filename}")
    thumbnail_path = os.path.join(RESIZED_FOLDER, f"thumbnail_{filename}")

    image.save(original_path)

    resize_image(original_path, resized_path)
    create_thumbnail(original_path, thumbnail_path)

    return jsonify({
        "message": "Image uploaded and processed",
        "events": [
            {
                "type": EVENT_IMAGE_RESIZED,
                "file": resized_path,
                "size": "300x300"
            },
            {
                "type": EVENT_IMAGE_THUMBNAIL_CREATED,
                "file": thumbnail_path,
                "size": "100x100"
            }
        ]
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)