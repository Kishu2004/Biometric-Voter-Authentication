from datetime import datetime
from pathlib import Path

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

AUTH_LOG = LOG_DIR / "auth.log"
FRAUD_LOG = LOG_DIR / "fraud.log"

def log_auth(message):
    with open(AUTH_LOG, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")

def log_fraud(message):
    with open(FRAUD_LOG, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")
