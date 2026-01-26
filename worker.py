cat > CodingBot/workers/worker.py <<'EOF'
import time
import os

ID = os.getenv("WORKER_ID", "1")

while True:
    print(f"[Worker {ID}] running")
    time.sleep(10)
EOF
