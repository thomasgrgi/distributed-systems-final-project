from fastapi import FastAPI
import uuid
from utils.redis_client import get_redis_connection

app = FastAPI()
r = get_redis_connection()

@app.post("/join_queue")
def join_queue():
    ticket_id = str(uuid.uuid4())
    r.rpush("queue", ticket_id)
    position = r.llen("queue")
    
    return {
        "ticket_id": ticket_id,
        "position": position
    }

@app.get("/position/{ticket_id}")
def get_position(ticket_id: str):
    queue = r.lrange("queue", 0, -1)
    
    if ticket_id in queue:
        return {"position": queue.index(ticket_id) + 1}
    
    return {"position": -1}
