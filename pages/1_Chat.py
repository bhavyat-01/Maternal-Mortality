import streamlit as st
from utils.gemini import get_gemini_response
from streamlit_option_menu import option_menu
from streamlit_chat import message
from utils.db import get_hospitals_collection




def chat_support_page():


    hospitals = get_hospitals_collection()
    arr = list(hospitals.find())

    hospital_data_str = "\n".join([
        f"Hospital: {hospital['hospitalName']}, "
        f"Location: {hospital['hospitalLocation']}, "
        f"Complaints: {', '.join(hospital.get('complaint', []))}, "

        for hospital in arr
    ])
    st.header("Chatbot Support Center")

    st.write("Welcome! You can ask some questions about maternal health in general or questions on hospitals that have bad reviews.")

    st.write("Here are some sample questions to ask on maternal mortality:")
    st.write("1. Give me some statistics on maternal mortality?")
    st.write("2. What age has the highest risk of maternal death?")
    st.write("You can also ask us questions about our database on hospitals with reported incidences of bias")
    st.write("1. What are some hospitals that have a bad rating?")
    st.write("2. What are some key complaints in *hospital-name* (to look at reported hospitals, check Ratings tab or ask Chat)")

    question = st.text_input("Ask any concerns or questions...")

    system_message = f"""
    You are an expert on maternal mortality and healthcare. You have access to the following hospital data:

    {hospital_data_str}

    You also have general knowledge of maternal health. 

    Avoid saying, "based on the data provided" or something similar.

    Stay focused on prompts related to maternal mortality and healthcare. For general greetings ONLY, you can respond with appropriate responses.

    If the user asks a question that is not related to maternal mortality or healthcare, do not repeat the user's question or engage in a literal response. Instead, respond with:

    "Unfortunately, that doesn't relate to maternal mortality or healthcare. Please ask a question related to these topics."

    If the user misspells something or makes a typo, do not repeat the question verbatim. Ignore the spelling issue and provide a relevant, on-topic response (or indicate the need for a maternal mortality-related question).
    """

    if question:
        message(question, is_user = True)
        response = get_gemini_response(system_message + question)
        reply = response if response else "I'm not sure how to respond."
        message(reply)

# Run the chat support page
chat_support_page()
