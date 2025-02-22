import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

df2 = pd.read_csv('race.csv')

fig1 = px.line(df2, x='X.1', y=['White', 'Hispanic', 'Black', 'Asian'], 
markers=True, title='Percentage of Mortality Rate vs. Race')
fig1.update_layout(xaxis_title='Year', yaxis_title='Percentage of Mortality Rate')

df3 = pd.read_csv('age.csv')

fig2 = px.line(df3, x='Year', y=['Under 25', '25-39', '40 and Older'], 
markers=True, title='Percentage of Mortality Rate vs. Age')
fig2.update_layout(xaxis_title='Year', yaxis_title='Percentage of Mortality Rate')

# Use columns to arrange graphs
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    
    
client = genai.Client(api_key="AIzaSyBhWqsOUmAgsq2YDinL_28i0qAO-vxC0Bc")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
st.write(response.text)



