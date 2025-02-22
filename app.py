import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = ""
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Mortality-App']
users = db["Users"]

selected2 = option_menu(None, ["Home", "Send Report", "Chat Support", 'Hospital Ratings'], 
    icons=['house', 'activity', "chat", 'hospital'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if(selected2 == "Home"):

    st.header("What is maternal mortality rate?")

    maternal_mortality_rate = """
    Maternal Mortality Rate (MMR) is the number of women who die due to pregnancy-related problems per 100,000 live births within a certain time period. These deaths can happen during pregnancy, childbirth, or up to 42 days after giving birth. The main causes are complications like heavy bleeding, infections, high blood pressure, and unsafe abortions, many of which can be prevented with proper care.

    MMR is an important measure of how good a country's healthcare system is, how easy it is for women to get medical help, and the overall living conditions. In wealthier countries, lower MMR is due to good healthcare, trained doctors, and access to prenatal and postnatal care. In poorer countries, higher rates happen because of limited access to healthcare, poverty, and lack of education. 

    To reduce maternal deaths, it is important to improve healthcare, ensure skilled help during childbirth, and provide timely medical care to all women.
    """

    st.text(maternal_mortality_rate)

    df2 = pd.read_csv('race.csv')

    fig1 = px.line(df2, x='X.1', y=['White', 'Hispanic', 'Black', 'Asian'], 
                markers=True, title='Percentage of Mortality Rate vs. Race')
    fig1.update_layout(xaxis_title='Year', yaxis_title='Percentage of Mortality Rate')

    df3 = pd.read_csv('age.csv')

    fig2 = px.line(df3, x='Year', y=['Under 25', '25-39', '40 and Older'], 
                markers=True, title='Percentage of Mortality Rate vs. Age')
    fig2.update_layout(xaxis_title='Year', yaxis_title='Percentage of Mortality Rate')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True, key="fig1")

    with col2:
        st.subheader("Age as a Factor")
        st.text("Age is an important factor in maternal mortality. Teenagers, especially those under 20, face higher risks due to physical immaturity, while women over 35 also experience increased risks due to age-related complications like high blood pressure, diabetes, and fertility issues. Women in their 20s to early 30s generally have the lowest risk, as their bodies are physically more equipped for pregnancy. Therefore, both very young and older mothers are at higher risk for complications during pregnancy and childbirth.")
        
        
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Race as a Factor")
        st.text("Race affects maternal mortality, with Black, Indigenous, and Hispanic women having higher risks than white women. This is due to factors like less access to good healthcare, higher rates of health problems, and economic struggles. Racial discrimination in healthcare can also lead to delays or poor treatment. To reduce these differences, it’s important to improve healthcare access and make sure all women get fair and timely care.")
        

    with col2:
        st.plotly_chart(fig2, use_container_width=True, key="fig2")

    
    st.header("Our solution to help combat racial bias")
    st.text("To help fight racial bias in healthcare, we can create a Medical Bias Reporter system. This would allow patients and healthcare workers to report any instances of racial discrimination or unfair treatment. The system would be easy to use, letting people submit anonymous reports about biased behavior. These reports would be reviewed to find patterns, train staff, and make improvements. By using this tool, healthcare systems can become more aware of issues and work towards fairer and more equal treatment for everyone.")

    fig1 = px.line(df2 , x='X.1', y=['White', 'Hispanic', 'Black', 'Asian'], 
    markers=True, title='Percentage of Mortality Rate vs. Race')
    fig1.update_layout(xaxis_title='Year', yaxis_title='Percentage of Mortality Rate')

    fig2 = px.line(df3, x='Year', y=['Under 25', '25-39', '40 and Older'], 
    markers=True, title='Percentage of Mortality Rate vs. Age')
    fig2.update_layout(xaxis_title='Year', yaxis_title='Percentage of Mortality Rate')
    

if(selected2 == "Send Report"):
    with st.form("my_form"):
        st.header("Report a hospital")
        hospital_name = st.text_input("Enter the Hospital Name")
        hospital_location = st.text_input("Enter the Hospital Location")
        complaint = st.text_input("Enter your Complaint")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Hospital Name: ", hospital_name, "Hospital Location", hospital_location)

if(selected2 == "Chat Support"):
    st.header("Chatbot Support Center")
    
    question = st.text_input('Ask any concerns or questions...')

    if question:
        client = genai.Client(api_key="AIzaSyBhWqsOUmAgsq2YDinL_28i0qAO-vxC0Bc")
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents="DON't answer unless related TO MATERNAL MORTALITY: "+question
        )
        st.write(response.text)
    
