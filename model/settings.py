import os

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "uploads/"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")

# REDIS
# Queue name
REDIS_QUEUE = "service_queue"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = 'redis_srv'

# Sleep parameters which manages the
# interval between requests to our redis queue
SERVER_SLEEP = 0.05

DECIMAL_PRECISION = 4
