import time
import requests

QUEUE_MANAGER_URL = "http://localhost:8001/next"

def process_ticket(ticket_id):
    print(f"[WORKER] Processing ticket {ticket_id}")
    time.sleep(3)
    print(f"[WORKER] Ticket {ticket_id} processed")

while True:
    response = requests.get(QUEUE_MANAGER_URL).json()
    ticket_id = response.get("ticket_id")
    
    if ticket_id:
        process_ticket(ticket_id)
    else:
        time.sleep(1)
