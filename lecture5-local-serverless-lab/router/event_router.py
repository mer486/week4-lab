import redis
import requests
import json
import time

r = redis.Redis(host="redis", port=6379, db=0)

IMAGE_RESIZER_URL = "http://image-resizer:5000/resize"
THUMBNAIL_URL = "http://thumbnail:5000/thumbnail"
NOTIFIER_URL = "http://notifier:5000/notify"


print("Event Router started...", flush=True)

while True:
    try:
        event = r.blpop("image_events", timeout=5)

        if event:
            _, event_data = event
            data = json.loads(event_data.decode("utf-8"))

            filename = data.get("filename")
            event_type = data.get("event_type")

            print(f"Received event: {event_type} for {filename}", flush=True)

            if event_type == "image_uploaded":
                requests.post(IMAGE_RESIZER_URL, json={"filename": filename})
                requests.post(THUMBNAIL_URL, json={"filename": filename})
                requests.post(NOTIFIER_URL, json={"filename": filename})

    except Exception as e:
        print(f"Router error: {e}", flush=True)
        time.sleep(2)