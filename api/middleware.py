import json
import time
from uuid import uuid4

import redis
import settings

import app 
# DONE
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)


def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None
    #NOTE. we consider that the best option is a queue for processing and another queue for the results
    
    queue_in = settings.REDIS_QUEUE+"-in"
    queue_out = settings.REDIS_QUEUE+"-out"
   
    job_id = str(uuid4())
    job_data = {
        "id": job_id,
        "image_name": image_name,
    }    

    db.rpush(queue_in, json.dumps(job_data))

    # Using an infinite click is not a good practice, we consider a timeout
    start_time = time.time()
    
    while  time.time() - start_time < settings.MAX_WAIT_TIME:
        _, data_byte = db.brpop(queue_out,timeout=0)
        if data_byte:
            json_out = json.loads(data_byte.decode("utf-8"))
            if json_out.get("id") == job_id:                
                prediction = json_out["prediction"]
                score = json_out["score"]
                break
            
        time.sleep(settings.API_SLEEP)
   
    return prediction, score
