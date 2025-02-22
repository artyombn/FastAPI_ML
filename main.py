import logging
import random

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

predictions = [
    {"prediction": "spam", "confidence": 0.95, "reason": "Contains 'win' and 'prize'"},
    {"prediction": "spam", "confidence": 0.87, "reason": "Too many exclamation marks"},
    {"prediction": "no_spam", "confidence": 0.90, "reason": "No spam-related keywords detected"},
    {"prediction": "spam", "confidence": 0.80, "reason": "Suspicious link detected"},
    {"prediction": "no_spam", "confidence": 0.85, "reason": "Appears to be a regular conversation"},
    {"prediction": "spam", "confidence": 0.92, "reason": "Sender is blacklisted"},
    {"prediction": "no_spam", "confidence": 0.88, "reason": "Message structure is normal"},
]

class InputData(BaseModel):
    message: str

class OutputData(BaseModel):
    prediction: str
    confidence: float
    reason: str | None

@app.get("/")
async def index():
    return {"Description": "This is ML prediction.\n"
                           "Send a dict in the following format {'message':'Your message'} "
                           "to predict if this spam or not"}

def get_input_data(dict: InputData) -> OutputData:
    input_data = dict
    logger.debug(input_data)
    # ...
    # ML processing on prediction using dict: InputData
    # ...

    fake_json = random.choice(predictions)
    prediction = OutputData(**fake_json)
    logger.debug(prediction)
    return prediction

@app.post("/prediction/", response_model=OutputData)
async def predict(result: OutputData = Depends(get_input_data)):
    return result.model_dump()

