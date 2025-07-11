import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import numpy as np

st.set_page_config(page_title='Basic Sales Dashboard', layout='wide')

np.random.seed(42)
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=2000),
    'Sales': np.random.randint(500, 10000, size=2000),
    'Region': np.random.choice(['Delhi', 'Mumbai', 'Pune', 'Nashik'], size=2000),
    'Product': np.random.choice(['Electronics', 'Clothing', 'Food & Beverages'], size=2000)
})

st.title("Sales Analysis")

st.sidebar.title('Filters')
regions = st.sidebar.multiselect('Select Region', df['Region'].unique(), default=df['Region'].unique())
products = st.sidebar.multiselect('Select Product', df['Product'].unique(), default=df['Product'].unique())

filtered_df = df[(df['Region'].isin(regions)) & (df['Product'].isin(products))]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
col2.metric("Average Sales", f"${filtered_df['Sales'].mean():.0f}")
col3.metric("Records", len(filtered_df))

Region_Sales = df.groupby('Region')['Sales'].sum().reset_index()
Max_Sales_Region = df.groupby('Region')['Sales'].sum().idxmax()
st.markdown(f"The Maximum Sale is in the {Max_Sales_Region} Region")

fig1 = px.bar(filtered_df, x='Region',y='Sales')
st.plotly_chart(fig1,use_container_width=True)

Pie_R = st.checkbox('View Pie Chart for Region')
if Pie_R:
    st.success('Pie Chart for Region Sales')
    fig2 = px.pie(filtered_df, names='Region',values='Sales')
    st.plotly_chart(fig2,use_container_width=True)

Product_Sales = df.groupby('Product')['Sales'].sum().reset_index()
Max_Product_Sales = df.groupby('Product')['Sales'].sum().idxmax()
st.markdown(f"The product With Maximum Sales is {Max_Product_Sales}")

fig4 = px.bar(Product_Sales,x='Product',y='Sales')
fig4.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Product_Sales['Sales'].max()+1000000]))
st.plotly_chart(fig4,use_container_width=True)

df['Month'] = df['Date'].dt.strftime('%B')
month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
df['Month'] = pd.Categorical(df['Month'],categories=month_order,ordered=True)
monthwise = df.groupby('Month').sum(numeric_only=True)
st.bar_chart(monthwise)

product_market = st.checkbox("See the line chart for Product and Region Sales")
if product_market:
    fig10 = px.line(Product_Sales,x ='Product',y= 'Sales')
    st.plotly_chart(fig10,use_container_width=True)
    fig11 = px.line(Region_Sales,x ='Region',y= 'Sales')
    st.plotly_chart(fig11,use_container_width=True)

Insights = st.checkbox("See The insights of The Data")
if Insights:
    Top_Region = df.groupby('Region')['Sales'].sum().nlargest(2).reset_index()
    st.success("The Top 2 Region With The Highest Sales Are:")
    for i ,row in Top_Region.iterrows():
        st.write(f"{i+1} {row['Region']}:{row['Sales']}")
    Top_Product = df.groupby('Product')['Sales'].sum().nlargest(2).reset_index()
    st.success("The Top 2 Products With Higest Sales Are:")
    for i ,row in Top_Product.iterrows():
        st.write(f"{i+1} {row['Product']}:{row['Sales']}")
    Top_Months = monthwise['Sales'].nlargest(3).reset_index()
    st.success("The Top 3 Months With Highest Sales Are:")
    for i ,row in Top_Months.iterrows():
        st.write(f"{i+1} {row['Month']}:{row['Sales']}")

Monthly_Sales = st.checkbox('View Line Chart Of Monthly Sales')
if Monthly_Sales:
    st.success("The Line Chart For Monthly Sales")
    month_sale = px.line(df,x= 'Month',y= 'Sales')
    st.plotly_chart(month_sale,use_container_width=True)

Each_product_Sale = st.checkbox("View Sales For Each Product")
if Each_product_Sale:
    st.success("The Monthly Sales For Each Product")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_sales_p = df.groupby(['Product','Month'])['Sales'].sum().reset_index()
    product_list = monthly_sales_p['Product'].unique()
    selected_product = st.multiselect("Select products to view Monthly Sales",product_list)

    for Product in selected_product:
        product_data = monthly_sales_p[monthly_sales_p['Product']== Product] 
        st.line_chart(product_data.set_index('Month')['Sales'])

Each_Region_Sale = st.checkbox("View Monthly Sales For Each Product")
if Each_Region_Sale:
    st.success("The Monthly Sales Of Each Region")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)  
    monthly_sales_r = df.groupby(['Region','Month'])['Sales'].sum().reset_index()
    Region_List = monthly_sales_r['Region'].unique()
    selected_region = st.multiselect("Select The Region",Region_List)

    for Region in selected_region:
        Region_Data = monthly_sales_r[monthly_sales_r['Region'] == Region]
        st.line_chart(Region_Data.set_index('Month')['Sales'])
               
Pie_s = st.checkbox("View Pie Chart For Product Sales")
if Pie_s:
    st.success('Pie Chart for Product Sales')
    fig5 = px.pie(Product_Sales,names='Product',values='Sales')
    fig5.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Product_Sales['Sales'].max()+1000000]))
    st.plotly_chart(fig5,use_container_width=True)


fig6= px.scatter_3d(filtered_df,x='Product',y='Region',z='Sales',color='Product',size_max=10)
st.plotly_chart(fig6,use_container_width=True)

fig7 = px.density_heatmap(df, x='Product', y='Region', z='Sales')
st.plotly_chart(fig7,use_container_width=True)

line_3d = st.checkbox("View 3d Line chart")
if line_3d:
    st.success("The Line 3d For Sales")
    fig8 = px.line_3d(df,x='Product',y='Region',z='Sales',color='Region')
    st.plotly_chart(fig8,use_container_width=True)

st.dataframe(df.drop(columns=['Date']).describe())
st.subheader("Filtered Data")
st.dataframe(filtered_df)