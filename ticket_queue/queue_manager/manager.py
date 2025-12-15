from fastapi import FastAPI
import uuid
from utils.redis_client import get_redis_connection

app = FastAPI()
r = get_redis_connection()

@app.post("/enqueue")
def enqueue():
    ticket_id = str(uuid.uuid4())

    r.rpush("queue", ticket_id)

    return {"ticket_id": ticket_id}

@app.get("/next")
def next_ticket():
    ticket = r.rpoplpush("queue", "processing")
    return {"ticket_id": ticket}
