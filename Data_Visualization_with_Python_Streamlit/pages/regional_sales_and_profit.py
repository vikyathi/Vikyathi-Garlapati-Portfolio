import streamlit as st
import altair as alt
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

st.header("Region sales of the Superstore")

df = pd.read_csv("Superstore.csv", encoding='cp1252')
df['Order Date'] = pd.to_datetime(df["Order Date"], format='%m/%d/%Y')
df['OrderYear']=df['Order Date'].dt.year

region_sales = df.groupby(['Region'])['Sales'].sum().reset_index(name='region sales')
sales_over_time = df.groupby(['OrderYear', 'Region']).agg({'Sales':'sum'}).reset_index()

tab1, tab2 = st.tabs(['Region Sales', 'State Profit'])

with tab1:
    st.markdown("As per the total region sales and region sales over the time period 2014 to 2017, West Region has the largest sales and relatively maintained the highest number of sales every year")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(
        data_frame= region_sales,
        names = 'Region',
        values = 'region sales',
        title='Total Region Sales',
        hole = 0.2,
        height= 400,
        width= 350
        )
        st.plotly_chart(fig1)
    with col2:
        st.text("")
        st.text("")
        line_chart = alt.Chart(sales_over_time).mark_line().encode(
        x='OrderYear:N',
        y='Sales',
        color = 'Region'
        ).properties(
            height = 300,
            width = 450,
            title = 'Region sales over the time period'
        )
        st.altair_chart(line_chart, use_container_width=False)

with tab2:

    st.markdown("California has the highest profit out of all states while Texas has highest loss in the profit")
    profit_state_sorted = df.groupby('State')['Profit'].sum().sort_values(ascending=False).reset_index()

    bar_plot = alt.Chart(profit_state_sorted).mark_bar().encode(
        x=alt.X('State', sort = '-y'),
        y=alt.Y('Profit'),
        tooltip = ('State', 'Profit')
    ).properties(
        height = 400
    )
    st.altair_chart(bar_plot, use_container_width=True)

