import streamlit as st
import pandas as pd
import plotly.express as px
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
st.write(f"The Maximum Sale is in the {Max_Sales_Region} Region")

fig1 = px.bar(filtered_df, x='Region',y='Sales')
st.plotly_chart(fig1,use_container_width=True)

Pie_R = st.checkbox('View Pie Chart for Region')
if Pie_R:
    st.success('Pie Chart for Region Sales')
    fig2 = px.pie(filtered_df, names='Region',values='Sales')
    st.plotly_chart(fig2,use_container_width=True)

Product_Sales = df.groupby('Product')['Sales'].sum().reset_index()
Max_Product_Sales = df.groupby('Product')['Sales'].sum().idxmax()
st.write(f"The product With Maximum Sales is {Max_Product_Sales}")

fig4 = px.bar(Product_Sales,x='Product',y='Sales')
fig4.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Product_Sales['Sales'].max()+1000000]))
st.plotly_chart(fig4,use_container_width=True)

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

fig8 = px.line_3d(df,x='Product',y='Region',z='Sales',color='Region')
st.plotly_chart(fig8,use_container_width=True)

st.dataframe(df.drop(columns=['Date']).describe())
st.subheader("Filtered Data")
st.dataframe(filtered_df)