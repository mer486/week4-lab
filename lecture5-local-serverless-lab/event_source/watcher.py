import redis
import json
import os
import time

r = redis.Redis(host="redis", port=6379, db=0)

INPUT_DIR = "/data/input"
seen_files = set()

print("Event Source started. Watching input folder...", flush=True)

while True:
    try:
        files = os.listdir(INPUT_DIR)

        for filename in files:
            if filename not in seen_files:
                seen_files.add(filename)

                event = {
                    "event_type": "image_uploaded",
                    "filename": filename
                }

                r.rpush("image_events", json.dumps(event))

                print(f"Published event: {event}", flush=True)

        time.sleep(3)

    except Exception as e:
        print(f"Watcher error: {e}", flush=True)
        time.sleep(3)