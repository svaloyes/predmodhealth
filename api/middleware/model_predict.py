import json
import time
from uuid import uuid4
import redis
import settings

db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)

def predict_hospitalization(data_input):
    """
    Predicts hospitalization risk based on the provided input data.

    This function takes the input data for a patient, generates a unique job ID, 
    and pushes the job into a Redis queue for processing. It then waits for 
    the prediction results to be available in the Redis database. Once the results 
    are ready, it retrieves them, deletes the job from Redis, and returns the 
    prediction and associated score.

    Parameters:
    - data_input (dict): A dictionary containing the input data required for 
      making a prediction. The structure of this data should match the 
      requirements of the underlying prediction model.

    Returns:
    - tuple: A tuple containing:
        - prediction (any): The predicted hospitalization risk (e.g., a class 
          label or numerical score).
        - score (float): A score indicating the confidence or probability 
          associated with the prediction.

    Raises:
    - KeyError: If the expected keys are not found in the results returned 
      from Redis.
    
    Notes:
    - The function uses a blocking loop to wait for results, which may lead 
      to higher latency. Consider implementing a timeout mechanism to avoid 
      potential infinite loops in case of failures.
    - Ensure that Redis is properly configured and running to handle 
      job queuing and result retrieval.
    """
    prediction = None
    score = None
    
    job_id = str(uuid4())
    job_data = {
        "id": job_id,
        "data_input": data_input
    }
    
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))
    
    while True:
        output = db.get(job_id)
        if output:
            results = json.loads(output.decode("utf-8"))
            prediction = results["prediction"]
            score = results["score"]
            db.delete(job_id)
            break
        time.sleep(settings.API_SLEEP)
    
    return prediction, score
