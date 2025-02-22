import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df2 = pd.read_csv('race.csv')
df2.plot(x='X.1', y=['White', 'Hispanic', 'Black', 'Asian'], kind='line', marker='o', title='Percentage of Mortality Rate vs. Race')
plt.xlabel('Year')
plt.ylabel('Percentage of Mortality Rate')
plt.xticks(range(int(df2['X.1'].min()), int(df2['X.1'].max()) + 1))

col1, col2 = st.columns([1, 1])
with col2:  # Put the plot in the left column
    st.pyplot(plt)

#st.pyplot(plt)

df3 = pd.read_csv('age.csv')
df3.plot(x='Year', y=['Under 25', '25-39', '40 and Older'], kind='line', marker='o', title='Percentage of Mortality Rate vs Age')
plt.xlabel('Year')
plt.ylabel('Percentage of Mortality Rate')
plt.xticks(range(int(df3['Year'].min()), int(df3['Year'].max()) + 1))

with col1:  # Put the plot in the left column
    st.pyplot(plt)