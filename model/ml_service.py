import json
import os
import time

import numpy as np
import redis
import settings

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.StrictRedis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)

# TODO
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ...


def predict(image_name):
    """
    
    """
    class_name = None
    pred_probability = None
    # Make prediction
    predictions = ... #model.predict()
    
    return class_name, pred_probability


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
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # TODO
         # Wait for a new job from Redis
        # Wait for a new job from Redis
        _, job_data = db.brpop(settings.REDIS_QUEUE)

        # Parse the job data
        job = json.loads(job_data.decode('utf-8'))
        
        # Extract job id and image name
        job_id = job['id']
        image_name = job['image_name']

        print(f"Processing job {job_id} for image {image_name}")

        # Get predictions using the `predict` function
        try:
            class_name, pred_probability = predict(image_name)

            # Store the results in Redis using the original job ID as the key
            result = {
                "prediction": class_name,
                "score": pred_probability,
            }
            db.set(job_id, json.dumps(result))
            print(f"Job {job_id} completed. Result: {result}")
        except Exception as e:
            print(f"Error processing job {job_id}: {str(e)}")
            # Optionally, you could store the error in Redis
            db.set(job_id, json.dumps({"error": str(e)}))
        

        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
