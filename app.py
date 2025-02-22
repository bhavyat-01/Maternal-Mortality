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
from streamlit_card import card


st.set_page_config(layout="wide")

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, tls=True,tlsAllowInvalidCertificates=True)
db = client['Mortality-App']
hospitals = db["Hospitals"]
gemini_uri = os.getenv("gemini_uri")



selected2 = option_menu(None, ["Home", "Send Report", "Chat Support", 'Hospital Ratings', 'Predict My Risk'], 
    icons=['house', 'activity', "chat", 'hospital', 'heart-pulse-fill'], 
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
        
    if 'data' not in st.session_state:
        st.session_state.data = {}
    
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
                
            keyWords = client.models.generate_content(
                model="gemini-2.0-flash", contents="Identify AT MOST 3 KEYWORDS or ADJECTIVES used here and return them separated with commas: "+prompt
            )
            
            arr_key_words = keyWords.text.split(',')
            
            #first obtain the existing document
            query = {
                "hospitalName": hospital_name,
                "hospitalLocation": hospital_location
            }
            
            existing_doc = hospitals.find_one(query)
            
            # if hospital exists
            if existing_doc:
                
                tagged_array = existing_doc['taggedWords']
                
                for word in arr_key_words:
                    found = False
                    for obj in tagged_array:
                        word = word.strip().lower()
                        if obj["word"] == word:
                            obj["count"] = obj["count"] + 1
                            found = True
                    if not found:
                        tagged_array.append({"word": word, "count": 1})
                            
                hospitals.update_one(
                    query,
                    {
                    "$push": {"complaint": prompt},  # Add the new complaint to the array
                    "$set": {"taggedWords": tagged_array}
                    }
                )
                
                st.write("Complaint Submitted!")
                
            else:
                #create JSON with each array element and number 1
                json_key_words =  [None]*3
                
                i = 0
                for word in arr_key_words:
                    
                    #gets rid of new line character
                    if "\n" in word:
                        word = word[0:len(word)-1]
                    #gets rid of spaces
                    word = word.strip()
                    #adds json object
                    json_key_words[i] = {"word": word.lower(), "count": 1}
                    i = i+1
                
                # If the document doesn't exist, create a new one
                st.session_state.data = {
                    "hospitalName": hospital_name,
                    "hospitalLocation": hospital_location,
                    "complaint": [prompt],  # Initialize the array with the new complaint
                    "taggedWords": json_key_words
                }
                    
                response = client.models.generate_content(
                    model="gemini-2.0-flash", contents="YES OR NO? One word answer ONLY. Does response display mistreatment OR is it ON TOPIC with  Maternal Mortality OR treatment in hospitals?: "+prompt
                )
                        
                if response.text.upper().strip()=="YES":
                    if len(st.session_state.data) > 0:
                        ret = hospitals.insert_one(st.session_state.data)

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
    


if(selected2 == "Hospital Ratings"):
    arr = list(hospitals.find())
    #for hospital in arr:
    def create_card(hospital_name, tagged_words):
    
        words_html = "".join([f'<div style="display: block; font-size: 14px; color: #555; align-self:center; background-color: #FD574C; padding: 5px;padding-left: 10px; padding-right: 10px; border-radius: 20px; text-align: right; border-color: white; color: white">{word}</div>' for word in tagged_words])
        card_html = f"""
        <div style="
            width: 100%;
            height: auto;
            padding: 20px;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            border-style: solid;
            border-color: white;
            margin-bottom: 20px;
        ">
            <h3 style="font-size: 18px; font-weight: bold; color: white">
                {hospital_name}
            </h3>
            <div style="display: flex; flex-direction: row; align-self: center; justify-content: space-between; gap: 20px; text-align: right;">
                {words_html}
                
            </div>
            
        </div>
        """
        return card_html

    if "complaint_visibility" not in st.session_state:
        st.session_state["complaint_visibility"] = {}
    for hospital in arr:
        final_tagged = sorted(hospital["taggedWords"], key=lambda x: x["count"], reverse=True)
        final_tagged = [item["word"] for item in final_tagged[:3]]
        card_html = create_card(hospital["hospitalName"], final_tagged)
        
        # Add a unique key to the button using the hospital's _id
        if st.button("Complaints", key=f"complaints_{hospital['_id']}"):
            # Set complaint visibility for this hospital to True
            st.session_state["complaint_visibility"][hospital["_id"]] = True
        
        # Display complaints if visible
        if st.session_state["complaint_visibility"].get(hospital["_id"], False):
            st.write(f"Complaints for {hospital['hospitalName']}:")
            for item in hospital["complaint"]:
                st.write(f"- {item}")
            
            # Add a "Close" button to hide complaints
            if st.button("Close", key=f"close_{hospital['_id']}"):
                # Immediately set complaint visibility to False
                st.session_state["complaint_visibility"][hospital["_id"]] = False
                # Force a rerun to update the UI immediately
                st.rerun()

        st.html(card_html)



        

                

        

        
