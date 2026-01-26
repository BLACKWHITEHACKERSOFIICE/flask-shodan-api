#!/bin/bash
source CodingBot/.env

python -m uvicorn CodingBot.api.main:app --host 127.0.0.1 --port 8000 &

for i in $(seq 1 $WORKER_COUNT); do
  WORKER_ID=$i python CodingBot/workers/worker.py &
done
