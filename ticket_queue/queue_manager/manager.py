from fastapi import FastAPI
from utils.redis_client import get_redis_connection

app = FastAPI()
r = get_redis_connection()

@app.get("/next")
def next_ticket():
    ticket = r.rpoplpush("queue", "processing")
    return {"ticket_id": ticket}
