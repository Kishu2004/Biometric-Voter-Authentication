import os
from db import reset_database

# Clear database
reset_database()

# Clear logs
log_dir = "data/logs"
for file in os.listdir(log_dir):
    os.remove(os.path.join(log_dir, file))

print("✅ System reset complete")
