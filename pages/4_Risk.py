import streamlit as st
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
from utils.gemini import get_gemini_response



def predictRisk(): 

    # Load the model
    model = tf.keras.models.load_model('risk_predictor.h5')  # Replace with your model file name

    
    st.title("Predict Your Risk for Complications during Pregnancy")
    st.text("Enter simple information such as age, blood pressure, blood sugar, etc. to see how risky your pregnancy may be. Take a look at the suggestions below to reduce your risk.")
    with st.form("my_form"):
        age = st.text_input("Enter Age")
        SBP = st.text_input("Enter Systolic BP")
        DBP = st.text_input("Enter Diastolic BP")
        BS = st.text_input("Enter Blood Sugar")
        BT = st.text_input("Enter Body Temperature")
        HR = st.text_input("Enter Heart Rate")
        button = st.form_submit_button("Submit Information")

        if button:
            # Use the model for predictions
            predictions = model.predict(np.array([[float(age), float(SBP), float(DBP), float(BS), float(BT), float(HR)]]))
            predicted_class = tf.argmax(predictions, axis=1).numpy()[0]  # Get the predicted class
            
            if(predicted_class == 0):
                risk_level = "low"
            elif(predicted_class == 1):
                risk_level = "medium"
            else:
                risk_level = "high"
            
            response = get_gemini_response("UNDER 200 WORDS: What can I do if I am at "+risk_level+" risk for maternal mortality? Specifically age wise.")
            st.markdown("To prevent any unfortunate event, "+response)
    
predictRisk()
