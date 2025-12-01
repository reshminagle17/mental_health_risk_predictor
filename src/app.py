# importing from third party libraries 
from fastapi import FastAPI , Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import joblib

# importing from internal files
import numpy as np
from models import get_db, HealthData

# initializing the FastAPI app
app=FastAPI(title='Mental health Risk Predictor')

class HealthDataInput(BaseModel):
    sleep_hours:float
    exercise_hours:float
    stress_level:int
    social_activity:int
    work_hours:float
    screen_time:float

def create_dummy_model():
    from sklearn.ensemble import RandomForestClassifier
    model=RandomForestClassifier(n_estimators=10,random_state=42)
    X=np.random.rand(100,6)
    Y=np.random.choice(['Low Risk','Medium Risk','High Risk'], size=100)
    model.fit(X,Y)
    return model

# initialize the ml model

model=create_dummy_model()
@app.post("/predict")
def predict_mental_health_risk(data:HealthDataInput, db:Session=Depends(get_db)):
    try:
        # convert input data to numpy array for prediction
        input_data=np.array([[
                                data.sleep_hours,
                                data.exercise_hours,
                                data.stress_level,
                                data.social_activity,
                                data.work_hours,
                                data.screen_time
                            ]])
        # use model to make prediction 
        prediction=model.predict(input_data)
        prediction=prediction[0]
        # create and save recordas to the database
        db_record=HealthData(
                                sleep_hours=data.sleep_hours,
                                exercise_hours=data.exercise_hours,
                                stress_level=data.stress_level,
                                social_activity=data.social_activity,
                                work_hours=data.work_hours,
                                screen_time=data.screen_time,
                                prediction=prediction 
                                )
        db.add(db_record)
        db.commit()

        return {"prediction":prediction}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

@app.get("/history")

def get_prediction_history(db:Session=Depends(get_db)):
    records=db.query(HealthData).order_by(HealthData.timestamp.desc()).limit(10).all()
    return records



