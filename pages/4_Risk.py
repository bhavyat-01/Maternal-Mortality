import streamlit as st
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.models import load_model


def predictRisk(): 
    st.title("Hey")

    # Load the model
    model = load_model('my_model.h5')  # Replace with your model file name

    # Use the model for predictions
    predictions = model.predict(input_data)
    
    
predictRisk()