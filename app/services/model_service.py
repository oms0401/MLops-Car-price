import joblib
import pandas as pd
from app.core.config import setting
from app.cache.redis_cache import get_cached_prediction,set_cached_prediction

model =joblib.load(setting.MODEL_PATH)

def predict_car_price(data: dict):
    #using the whole row as the key in order to save the cache value 
    cached_key= " ".join([str(value) for value in data.values()])
    cached=get_cached_prediction(cached_key)
    if cached:
        return cached
    input_data=pd.DataFrame([data])
    prediction=model.predict(input_data)[0]
    set_cached_prediction(cached_key,prediction)
    return prediction

