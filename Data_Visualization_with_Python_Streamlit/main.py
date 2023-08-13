import streamlit as st
import pandas as pd
import altair as alt

# read the dataset
df = pd.read_csv("Superstore.csv", encoding='cp1252')
df['Order Date'] = pd.to_datetime(df["Order Date"], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df["Ship Date"]).dt.date

st.header('Superstore Data Analysis')

tab1,tab2 = st.tabs(['Dataset','Total sales and profit'])

with tab1:
    st.markdown("The Dataset is taken from the tableau to see how to visilaze the data in streamlit." +
                " It has order details of the customers over the time period 2014 to 2017. Analysing the superstore dataset " +
                "to see how the sales and profits are impacted considering various factors.")

    st.subheader('Dataset')
    st.write(df.head())

with tab2:

    sales = int(df['Sales'].sum())
    formatted_sales = str(sales)
    profit = int(df['Profit'].sum())
    formatted_profit = str(profit)
    profit = round(sales/profit,2)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", "$"+ formatted_sales[: 1] + "."+ formatted_sales[1:3] + "M")
    col2.metric("Total Profit", "$"+ formatted_profit[:3]+ "K")
    col3.metric("Profit ratio", str(profit))

    category_df = df.groupby(['Category'])['Category'].count().reset_index(name='counts')
    category_sales = df.groupby(['Category'])['Sales'].sum().reset_index(name='category sales')
    category_profit = df.groupby(['Category'])['Profit'].sum().reset_index(name='category profit')


    category_selected = st.selectbox('Select category',
    ['Most popular category','Category sales', 'Category profit'])

    if category_selected == 'Most popular category':
        dataframe = category_df
        x_axis = 'counts'
    elif category_selected == 'Category sales':
        dataframe = category_sales
        x_axis = 'category sales'
    else:
        dataframe = category_profit
        x_axis = 'category profit'
    st.markdown("Top categories with most sales and profits")
    bar_plot = alt.Chart(dataframe).mark_bar().encode(
        x=x_axis,
        y=alt.Y('Category', sort='-x'),
        color = x_axis,
        tooltip = (x_axis, 'Category')
    ).properties(
        height = 150
    )
    st.altair_chart(bar_plot, use_container_width=True)

    #total number of unique customers every year
    st.markdown("The number of unique customers gradually increased from 2015 to 2017 as the store icreasing the marketing strategies.")
    df['Year'] = df['Order Date'].dt.year
    customer_data = df.groupby('Year').agg({'Customer Name':'nunique'}).reset_index()
    line_plot = alt.Chart(customer_data).mark_line().encode(
        x = alt.X('Year:N', axis=alt.Axis(tickSize=0)),
        y=alt.Y('Customer Name', scale=alt.Scale(domain=[540, 700]), title = 'unique customer count')
    ).properties(
        height = 250
    )
    st.altair_chart(line_plot, use_container_width=True)






