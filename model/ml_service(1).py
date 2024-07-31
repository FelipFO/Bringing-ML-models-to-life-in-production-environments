import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image


# DONE
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)

# DONE
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # Load the image file, targeting a size appropriate for ResNet50
    img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(img_path, target_size=(224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
        
    preds = model.predict(x)

    decoded_preds = decode_predictions(preds, top=1)[0][0]
    class_name, pred_probability = decoded_preds[1], decoded_preds[2]
    
    return class_name, round(pred_probability,settings.DECIMAL_PRECISION)


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        queue_in = settings.REDIS_QUEUE+"-in"
        queue_out = settings.REDIS_QUEUE+"-out"
        try:
            _, data_byte = db.brpop(queue_in)
            if data_byte:
                # Load job information
                job = json.loads(data_byte)
                if 'image_name' in job:
                    class_name, pred_probability = predict(job['image_name'])                    
                    if class_name and pred_probability:
                        prediction_data = {
                        "id": job['id'],
                        "image_name": job['image_name'],
                        "prediction": class_name,
                        "score": round(float(pred_probability),settings.DECIMAL_PRECISION)
                        }            
                        db.lpush(queue_out, json.dumps(prediction_data))
                else:
                    print(f"ML Service: No image name provided in job {job['id']}")
        
        except Exception as e:
             print(f"Error in classify_process: {e}")
        
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
