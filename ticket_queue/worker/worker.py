import time
import requests
import redis
import os

QUEUE_MANAGER_URL = "http://queue_manager:8001/next"
WORKER_ID = os.getenv("WORKER_ID", "worker-unknown")


# Initialize Redis connection
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def process_ticket(ticket_id):
    print(f"[WORKER] Processing ticket {ticket_id}")
    time.sleep(3)
    print(f"[WORKER] Ticket {ticket_id} processed")

    r.lrem("processing", 0, ticket_id)
    print(f"[WORKER] Ticket {ticket_id} removed from processing list")
    

while True:

    try:
        response = requests.get(QUEUE_MANAGER_URL, timeout=2)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        print(f"[{WORKER_ID}] Queue manager not ready, retrying...")
        time.sleep(2)
        continue

    ticket_id = data.get("ticket_id")

    if ticket_id:
        r.hset("workers:active", WORKER_ID, ticket_id)

        process_ticket(ticket_id)

        r.hdel("workers:active", WORKER_ID)

    else:
        time.sleep(1)

    # response = requests.get(QUEUE_MANAGER_URL).json()
    # ticket_id = response.get("ticket_id")
    
    # if ticket_id:
    #     process_ticket(ticket_id)
    # else:
    #     time.sleep(1)
