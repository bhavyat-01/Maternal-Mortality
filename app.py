import os
import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_chat import message



st.set_page_config(layout="wide")

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, tls=True,tlsAllowInvalidCertificates=True)
db = client['Mortality-App']
hospitals = db["Hospitals"]
gemini_uri = os.getenv("GEM_URI")


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

    if 'touched_question' not in st.session_state:
        st.session_state.touched_question = ""
    
    with st.form("my_form"):
        st.header("Report a hospital")
        hospital_name = st.text_input("Enter the Hospital Name")
        hospital_location = st.text_input("Enter the Hospital Location")
        complaint = st.text_input("Enter your complaints via bullets and ask AI to construct a response. Please be specific with examples of what happend. ")
        ai_answer = st.form_submit_button('Click to touch up answer')
    
        if ai_answer:
            client = genai.Client(api_key=gemini_uri)
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents="Touch up this complaint as if you are complaining under 50 words. No madlib brackets: "+complaint
            )
            st.text(response.text)
            st.session_state.touched_question = response.text        
            
        submitted = st.form_submit_button("Submit")
        verify = st.empty()
        
        
        if submitted:
            client = genai.Client(api_key=gemini_uri)
            prompt = ""; 
            
            if len(st.session_state.touched_question) > 0:
                prompt = st.session_state.touched_question
            else:
                prompt = complaint
                
            data = {"hospitalName": hospital_name, "hospitalLocation": hospital_location, "complaint": prompt}
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents="YES OR NO? One word answer ONLY. Does response display mistreatment OR is it ON TOPIC with  Maternal Mortality OR treatment in hospitals?: "+prompt
            )
                        

            if response.text.upper().strip()=="YES":
                ret = hospitals.insert_one(data)
                verify = st.markdown('Verified ✔')
                if ret: 
                    st.write("Submitted")
            elif response.text.upper().strip()=="NO":
                verify = st.markdown('Not Verified X')



if(selected2 == "Chat Support"):
    
    st.header("Chatbot Support Center")

    client = genai.Client(api_key=gemini_uri)
    question = st.text_input('Ask any concerns or questions...')

    system_message = """
        You are an expert on maternal mortality. Stay focused on prompts related to maternal mortality. For general greetings ONLY, you can respond with appropriate responses.

        If the user asks a question that is not related to maternal mortality, do not repeat the user's question or engage in a literal response. Instead, respond with:

        "Unfortunately, that doesn't relate to maternal mortality. Please ask a question related to maternal mortality."

        If the user misspells something or makes a typo, do not repeat the question verbatim. Ignore the spelling issue and provide a relevant, on-topic response (or indicate the need for a maternal mortality-related question). For example:

        Example 1:

        User: What are the leading causes of maternal mortality?
        Assistant: The leading causes of maternal mortality include hemorrhage, hypertension, infection, and complications during delivery.
        Example 2:

        User: How can maternal mortality be reduced?
        Assistant: Reducing maternal mortality involves improving access to prenatal care, skilled birth attendants, and emergency obstetric care.
        Example 3:

        User: Hello
        Assistant: Hello! Do you have any questions relating to maternal mortality?
        Example 4:

        User: Whats your fav movie?
        Assistant: Unfortunately, that doesn’t relate to maternal mortality. Please ask a question related to maternal mortality.
        Example 5:

        User: Wht are the main causs of maternal mortlaity?
        Assistant: The leading causes of maternal mortality include hemorrhage, hypertension, infection, and complications during delivery.

    """

    if question:
        message(question) 
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=system_message + question
        )
        reply = response.text if response.text else "I'm not sure how to respond."

        message(reply, is_user=True) 
    
