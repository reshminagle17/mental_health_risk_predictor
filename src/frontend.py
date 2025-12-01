import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# page configuration
st.set_page_config(page_title="Mental Health Risk Predictor",
                   page_icon="🧠",
                   layout="wide")

# main title and description

st.title("🧠 Mental Health Risk Predictor")
st.write("Enter your lifestyle factors to get a mental health risk assessment.")


# create 2 columns for better layout organization 
col1,col2=st.columns(2)

# left Columns: Input form 
with col1:
    st.subheader("Enter your Data")
    # sliders inputs -each slider has specific range and default values

    sleep_hours=st.slider(
        "Weekly Excerise Hours",
        0.0,12.0,7.0,0.5,
        help="how many hours do you sleep on average?"
    )
    exercise_hours=st.slider(
        "Weekly Excerise Hours",
        1,10,5,
        help="how many hours do you exercise per week ?"
    )
    stress_level=st.slider(
        "Stress level(1-10)",
        1,10,5,
        help="Rate your stress level(1=very low,10=very high)"
    )
    social_activity=st.slider(
        "Social Activity level(1-10)",
        1,10,5,
        help="Rate your social activity level (1=very low,10=very high)"
    )
    work_hours=st.slider(
        "Daily work hours",
        0.0,16.0,8.0,0.5,
        help="how many hours do you sleep on average?"
    )
    Screen_time=st.slider(
        "Daily Screen time  hours",
        0.0,16.0,6.0,0.5,
        help="how many hours do you spend on screens laptop,smartphone,tablet,other?"
    )

# prediction button
if st.button("Predict Risk"):
    data={
            "sleep_hours":sleep_hours,
            "exercise_hours":exercise_hours,
            "stress_level":stress_level,
            "social_activity":social_activity,
            "work_hours":work_hours,
            "screen_time":Screen_time
    }
    try:
        # nake Post request to backend API
        response=requests.post("http://localhost:8000/predict",json=data)
        if response.status_code==200:
            prediction=response.json()['prediction']
            st.success(f'Predicted Risk Level:{prediction}')
        else:
            st.error("Error making the Prediction. please try again")
    except requests.exceptions.ConnectionError:
        st.error("could not connect to the prediction service.Is the backend server running?")


# right column - history display
with col2:
    st.subheader("Recent Predictions")
    try:
        # fetching the prediction history free backend
        response=requests.get("http://localhost:8000/history")
        if response.status_code==200:
            history=response.json()
            if history:
                df=pd.DataFrame(history)
                df['timestamp']=pd.to_datetime(df['timestamp'])
                df['timestamp']=df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                # history table with selected columns display
                st.dataframe(
                    df[['timestamp','sleep_hours','exercise_hours','stress_level',
                        'social_activity','work_hours','screen_time','prediction']]   
                )
            else:
                st.info("No prediction history available yet!.")


    except requests.exceptions.ConnectionError: 
        st.error("could not connect to the prediction service.Is the backend server running?")




