import time
import requests
import redis

QUEUE_MANAGER_URL = "http://localhost:8001/next"

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def process_ticket(ticket_id):
    print(f"[WORKER] Processing ticket {ticket_id}")
    time.sleep(3)
    print(f"[WORKER] Ticket {ticket_id} processed")

    r.lrem("processing", 0, ticket_id)
    print(f"[WORKER] Ticket {ticket_id} removed from processing list")
    

while True:
    response = requests.get(QUEUE_MANAGER_URL).json()
    ticket_id = response.get("ticket_id")
    
    if ticket_id:
        process_ticket(ticket_id)
    else:
        time.sleep(1)
