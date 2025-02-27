import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

st.header("What is maternal mortality rate?")

maternal_mortality_rate = """
Maternal Mortality Rate (MMR) is the number of women who die due to pregnancy-related problems per 100,000 live births within a certain time period. These deaths can happen during pregnancy, childbirth, or up to 42 days after giving birth. The main causes are complications like heavy bleeding, infections, high blood pressure, and unsafe abortions, many of which can be prevented with proper care.

MMR is an important measure of how good a country's healthcare system is, how easy it is for women to get medical help, and the overall living conditions. In wealthier countries, lower MMR is due to good healthcare, trained doctors, and access to prenatal and postnatal care. In poorer countries, higher rates happen because of limited access to healthcare, poverty, and lack of education. 

To reduce maternal deaths, it is important to improve healthcare, ensure skilled help during childbirth, and provide timely medical care to all women.
"""
st.text(maternal_mortality_rate)

# Load data
df2 = pd.read_csv("assets/race.csv")
df3 = pd.read_csv("assets/age.csv")

# Create plots
fig1 = px.line(df2, x="X.1", y=["White", "Hispanic", "Black", "Asian"], markers=True, title="Percentage of Mortality Rate vs. Race")
fig1.update_layout(xaxis_title="Year", yaxis_title="Percentage of Mortality Rate")

fig2 = px.line(df3, x="Year", y=["Under 25", "25-39", "40 and Older"], markers=True, title="Percentage of Mortality Rate vs. Age")
fig2.update_layout(xaxis_title="Year", yaxis_title="Percentage of Mortality Rate")

# Display plots and text
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True, key="fig1")
with col2:
    st.subheader("Race as a Factor")
    st.text("Race affects maternal mortality, with Black, Indigenous, and Hispanic women having higher risks than white women. This is due to factors like less access to good healthcare, higher rates of health problems, and economic struggles. Racial discrimination in healthcare can also lead to delays or poor treatment. To reduce these differences, it’s important to improve healthcare access and make sure all women get fair and timely care.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Age as a Factor")
    st.text("Age is an important factor in maternal mortality. Teenagers, especially those under 20, face higher risks due to physical immaturity, while women over 35 also experience increased risks due to age-related complications like high blood pressure, diabetes, and fertility issues. Women in their 20s to early 30s generally have the lowest risk, as their bodies are physically more equipped for pregnancy. Therefore, both very young and older mothers are at higher risk for complications during pregnancy and childbirth.")
with col2:
    st.plotly_chart(fig2, use_container_width=True, key="fig2")

st.header("Our Solution to Combat Maternal Mortality Rates in Healthcare")
st.text("To address racial bias in healthcare, we developed a Medical Bias Reporter system. This platform enables patients and healthcare professionals to anonymously report instances of racial discrimination or unfair treatment. By analyzing these reports, we can identify patterns, improve training programs, and drive systemic change toward equitable healthcare for all.Additionally, we created a Pregnancy Risk Predictor using machine learning. This tool leverages patient data to assess potential risks during pregnancy, helping doctors make more informed decisions and provide personalized care. By integrating AI-driven insights with bias reporting, we aim to foster a more inclusive and data-driven approach to improving healthcare outcomes.")
