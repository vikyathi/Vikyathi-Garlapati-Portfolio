import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from vega_datasets import data

st.set_page_config(layout="wide")
st.title('Analysis on cars vega dataset')

st.header('Cars Dataset')

#import the salary dataset
salary_data = data.cars()

st.write(salary_data)

st.sidebar.header('Pick two variables for your scatter plot and bar graph')

x_val = st.sidebar.selectbox('Pick your x_axis', salary_data.select_dtypes(include=np.number).columns.tolist())
y_val = st.sidebar.selectbox('Pick your y_axis', salary_data.select_dtypes(include=np.number).columns.tolist())

scatter = alt.Chart(salary_data).mark_point(filled=True).encode(
    alt.X( x_val, title= f'{x_val}'),
    alt.Y( y_val, title= f'{y_val}'), 
    alt.Color('Origin'),
    tooltip=[x_val, y_val, 'Origin']).properties(
    title=f'Correlation between {x_val} and {y_val}',
    width=500,
    height=300
).interactive()

bar = alt.Chart(salary_data).mark_bar().encode(
    x= x_val, y= y_val).properties(
    title=f'bar graph of {x_val} and {y_val}'
).interactive()

col1, col2 = st.columns(2)

with col1:
  st.altair_chart(scatter, use_container_width=True)
with col2:
  st.altair_chart(bar)
  

#calculate the correlation
corr = round(salary_data[x_val].corr(salary_data[y_val]), 2)
st.write(f'The correlation between {x_val} and {y_val} is {corr}')