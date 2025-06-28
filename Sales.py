import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='Basic Sales Dashboard', layout='wide')

np.random.seed(42)
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=200),
    'Sales': np.random.randint(500, 5000, size=200),
    'Region': np.random.choice(['Delhi', 'Mumbai', 'Pune', 'Nashil'], size=200),
    'Product': np.random.choice(['Electronics', 'Clothing', 'Food & Beverages'], size=200)
})


st.sidebar.title('Filters')
regions = st.sidebar.multiselect('Select Region', df['Region'].unique(), default=df['Region'].unique())
products = st.sidebar.multiselect('Select Product', df['Product'].unique(), default=df['Product'].unique())

filtered_df = df[(df['Region'].isin(regions)) & (df['Product'].isin(products))]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
col2.metric("Average Sales", f"${filtered_df['Sales'].mean():.0f}")
col3.metric("Records", len(filtered_df))

st.subheader("Filtered Data")
st.dataframe(filtered_df)