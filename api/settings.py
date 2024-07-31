import os

# Run API in Debug mode
API_DEBUG = True

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")


# We will store user feedback on this file
FEEDBACK_FILEPATH = "feedback/feedback"
FEEDBACK_PATH = "feedback/"
os.makedirs(FEEDBACK_PATH, exist_ok=True)
print(f"FEEBACK FOLDER: {FEEDBACK_PATH}")

# REDIS settings
# Queue name
REDIS_QUEUE = "service_queue"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = 'redis_srv'
#REDIS_IP = os.getenv("REDIS_IP", "redis")
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05
# TIMEOUT
MAX_WAIT_TIME = 30 #seconds

DECIMAL_PRECISION = 4