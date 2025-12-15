FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn redis requests

CMD ["uvicorn", "queue_manager.manager:app", "--host", "0.0.0.0", "--port", "8001"]
