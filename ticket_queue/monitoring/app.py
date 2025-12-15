from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import redis
import os
import threading
import time
import requests

app = FastAPI()
load_thread = None
stop_load = False

app.mount("/static", StaticFiles(directory="/app/static"), name="static")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("index.html") as f:
        return f.read()

@app.get("/stats")
def stats():
    return {
        "join_requests": int(redis_client.get("stats:join_requests") or 0),
        "queue": redis_client.lrange("queue", 0, -1),
        "workers": redis_client.hgetall("workers:active")
    }

@app.post("/load")
def start_load(rate_per_minute: int):
    global load_thread, stop_load

    stop_load = False

    def generate_load():
        interval = 60 / rate_per_minute
        while not stop_load:
            try:
                requests.post("http://gateway:8000/join_queue")
            except Exception:
                pass
            time.sleep(interval)

    load_thread = threading.Thread(target=generate_load, daemon=True)
    load_thread.start()

    return {"status": "load started", "rate": rate_per_minute}

@app.post("/stop_load")
def stop_load_generation():
    global stop_load
    stop_load = True
    return {"status": "load stopped"}
