import streamlit as st
from utils.db import get_hospitals_collection
from utils.gemini import get_gemini_response
from streamlit_option_menu import option_menu



def send_report_page():

    st.header("Send a Report")

    hospitals = get_hospitals_collection()

    if "touched_question" not in st.session_state:
        st.session_state.touched_question = ""
    if "data" not in st.session_state:
        st.session_state.data = {}

    with st.form("my_form"):
        hospital_name = st.text_input("Enter the Hospital Name")
        hospital_location = st.text_input("Enter the Hospital Location")
        complaint = st.text_input("Enter your complaints via bullets and ask AI to construct a response. Please be specific with examples of what happened.")
        ai_answer = st.form_submit_button("Click to touch up answer")

        if ai_answer:
            response = get_gemini_response("Touch up this complaint as if you are complaining under 50 words. No madlib brackets: " + complaint)
            st.text(response)
            st.session_state.touched_question = response

        submitted = st.form_submit_button("Submit")
        verify = st.empty()

        if submitted:
            prompt = st.session_state.touched_question if st.session_state.touched_question else complaint
            keyWords = get_gemini_response("Identify AT MOST 3 KEYWORDS or ADJECTIVES used here and return them separated with commas: " + prompt)
            arr_key_words = keyWords.split(",")

            query = {"hospitalName": hospital_name, "hospitalLocation": hospital_location}
            existing_doc = hospitals.find_one(query)

            if existing_doc:
                tagged_array = existing_doc["taggedWords"]
                for word in arr_key_words:
                    word = word.strip().lower()
                    found = False
                    for obj in tagged_array:
                        if obj["word"] == word:
                            obj["count"] += 1
                            found = True
                    if not found:
                        tagged_array.append({"word": word, "count": 1})
                hospitals.update_one(query, {"$push": {"complaint": prompt}, "$set": {"taggedWords": tagged_array}})
                st.write("Complaint Submitted!")
            else:
                json_key_words = [{"word": word.strip().lower(), "count": 1} for word in arr_key_words]
                st.session_state.data = {
                    "hospitalName": hospital_name,
                    "hospitalLocation": hospital_location,
                    "complaint": [prompt],
                    "taggedWords": json_key_words,
                }
                response = get_gemini_response("YES OR NO? One word answer ONLY. Does response display mistreatment AND is it ON TOPIC with Maternal Mortality?: " + prompt)
                if response.upper().strip() == "YES":
                    hospitals.insert_one(st.session_state.data)
                    verify.markdown("Verified ✔")
                    st.write("Submitted")
                elif response.upper().strip() == "NO":
                    verify.markdown("Not Verified X")

# Run the send report page
send_report_page()

