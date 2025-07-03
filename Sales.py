import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title='Basic Sales Dashboard', layout='wide')

np.random.seed(42)
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=500),
    'Sales': np.random.randint(500, 5000, size=500),
    'Region': np.random.choice(['Delhi', 'Mumbai', 'Pune', 'Nashik'], size=500),
    'Product': np.random.choice(['Electronics', 'Clothing', 'Food & Beverages'], size=500)
})


st.sidebar.title('Filters')
regions = st.sidebar.multiselect('Select Region', df['Region'].unique(), default=df['Region'].unique())
products = st.sidebar.multiselect('Select Product', df['Product'].unique(), default=df['Product'].unique())

filtered_df = df[(df['Region'].isin(regions)) & (df['Product'].isin(products))]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
col2.metric("Average Sales", f"${filtered_df['Sales'].mean():.0f}")
col3.metric("Records", len(filtered_df))

Region_Sales = df.groupby('Region')['Sales'].sum().reset_index()

fig1 = px.bar(filtered_df, x='Region',y='Sales')
st.plotly_chart(fig1,use_container_width=True)

fig2 = px.pie(filtered_df, names='Region',values='Sales')
st.plotly_chart(fig2,use_container_width=True)

Product_Sales = df.groupby('Product')['Sales'].sum().reset_index()

fig4 = px.bar(Product_Sales,x='Product',y='Sales')
fig4.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Product_Sales['Sales'].max()+1000000]))
st.plotly_chart(fig4,use_container_width=True)

fig5 = px.pie(Product_Sales,names='Product',values='Sales')
fig5.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Product_Sales['Sales'].max()+1000000]))
st.plotly_chart(fig5,use_container_width=True)

fig6= px.scatter_3d(filtered_df,x='Product',y='Region',z='Sales',color='Product',size_max=10)
st.plotly_chart(fig6,use_container_width=True)

st.dataframe(df.describe())
st.subheader("Filtered Data")
st.dataframe(filtered_df)