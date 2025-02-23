import streamlit as st
from utils.db import get_hospitals_collection
from streamlit_option_menu import option_menu


def hospital_ratings_page():

    st.header("Hospital Ratings")

    hospitals = get_hospitals_collection()
    arr = list(hospitals.find())

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
            <div style="display: flex; flex-direction: row; flex-wrap: wrap; align-self: center; justify-content: space-between; gap: 20px; text-align: right;">
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

        if st.button("Complaints", key=f"complaints_{hospital['_id']}"):
            st.session_state["complaint_visibility"][hospital["_id"]] = True

        if st.session_state["complaint_visibility"].get(hospital["_id"], False):
            st.write(f"Complaints for {hospital['hospitalName']}:")
            for item in hospital["complaint"]:
                st.write(f"- {item}")
            if st.button("Close", key=f"close_{hospital['_id']}"):
                st.session_state["complaint_visibility"][hospital["_id"]] = False
                st.rerun()

        st.html(card_html)


# Run the hospital ratings page
hospital_ratings_page()
