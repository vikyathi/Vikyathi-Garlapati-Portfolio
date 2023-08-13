import streamlit as st
import altair as alt
import pandas as pd

st.header("Sales and Profits of each Category")
st.markdown("Based on the catogory and sub category, Furniture had most sales and profit over the time and In Furniture chairs had most sales and profit")

df = pd.read_csv("Superstore.csv", encoding='cp1252')
df['Order Date'] = pd.to_datetime(df["Order Date"], format='%m/%d/%Y')
df['OrderYear']=df['Order Date'].dt.year

sub_category_sales = df.groupby(['Sub-Category', 'Category'])['Sales'].sum().reset_index(name='sales')
sub_category_profit = df.groupby(['Sub-Category', 'Category'])['Profit'].sum().reset_index(name='profit')

def get_altair_line_chart(df, y_axis):
    line_chart = alt.Chart(df).mark_line().encode(
        x='OrderYear:N',
        y=y_axis,
        color = 'Category'
    ).properties(
        height = 300
    )
    st.altair_chart(line_chart, use_container_width=True)

def get_altair_bar_chart(df, y_axis):
    sales_chart = alt.Chart(df).mark_bar().encode(
    alt.X(field='Sub-Category', type='nominal', sort= '-y'),
    y=y_axis,
    color = y_axis
    ).transform_filter(
        alt.FieldEqualPredicate(field='Category', equal= selected_category)
    )
    st.altair_chart(sales_chart, use_container_width=True)


tab1, tab2, tab3, tab4 = st.tabs(['Category Sales', 'Category Profit',
                'Sub Category Sales','Sub Category Profits'])

with tab1:
    category_sales = df.groupby(['OrderYear', 'Category']).agg({'Sales':'sum'}).reset_index()
    y_axis = 'Sales'
    get_altair_line_chart(category_sales, y_axis)

with tab2:
    category_profit = df.groupby(['OrderYear', 'Category']).agg({'Profit':'sum'}).reset_index()
    y_axis = 'Profit'
    get_altair_line_chart(category_profit, y_axis)

with tab3:
    selected_category = st.selectbox('Select a category from the drop down to view sales of sub category',
        ['Furniture','Office Supplies', 'Technology'])
    get_altair_bar_chart(sub_category_sales, y_axis='sales')

with tab4:
    selected_category = st.selectbox('Select a category from the drop down to view profts of sub category',
        ['Furniture','Office Supplies', 'Technology'])
    get_altair_bar_chart(sub_category_profit, y_axis='profit')




