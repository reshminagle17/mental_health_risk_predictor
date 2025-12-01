from sqlalchemy import Column, Integer, String, DateTime,create_engine,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import declarative_base

# create the base clsaa for declarative models
base=declarative_base()
# create the sql lite database engine
engine=create_engine('sqlite:///health_predictions.db')
# create a session maker factory bound to our database
sessionLocal=sessionmaker(bind=engine)

class HealthData(base):
    __tablename__="health_data"

    # primary key as unique identifier
    id=Column(Integer,primary_key=True,index=True)

    # user inputs
    sleep_hours=Column(Float)
    exercise_hours=Column(Float)
    stress_level=Column(Integer)
    social_activity=Column(Integer)
    work_hours=Column(Float)
    screen_time=Column(Float)

    # model prediction output
    prediction=Column(String)

    # timestamp for tracking when the prediction was made 
    timestamp=Column(DateTime,default=datetime.utcnow)

# create all defined tables in the database
base.metadata.create_all(bind=engine)

def get_db():
    """
    database session generator that is yielding a database session 
    and ensuring its closure after use"""
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()