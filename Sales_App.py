import pandas as pd
import streamlit as st
import plotly.express as px

st.title("SALES DASHBOARD")
file_path = r"C:\Users\saura\OneDrive\Desktop\Sales_final.xlsx"
df = pd.read_excel(file_path,engine='openpyxl')
print(df.head())
print(df.info())
print(df.describe())

st.sidebar.title('Filters')
Status = st.sidebar.multiselect('Select Status:',df['STATUS'].unique(),default=df['STATUS'].unique())
Year = st.sidebar.multiselect('Select Year:',df['YEAR_ID'].unique(),default=df['YEAR_ID'].unique())
Country = st.sidebar.multiselect('Select Country:',df['COUNTRY'].unique(),default=df['COUNTRY'].unique())

filter_df = df[(df['STATUS'].isin(Status)) & (df['YEAR_ID'].isin(Year)) & (df['COUNTRY'].isin(Country)) ]

col1, col2, col3 = st.columns(3)
col1.metric('Total Sales',f"${filter_df['SALES'].sum():,}")
col2.metric('Average Sales',f"${filter_df['SALES'].mean():.0f}")
col3.metric('Records',len(filter_df))

col1,col2 = st.columns(2)
with col1 :
    Year_sales=filter_df.groupby('YEAR_ID')['SALES'].sum().reset_index()
    fig_line = px.line(Year_sales,x= 'YEAR_ID',y= 'SALES',title="Yearly Sales" )
    fig_line.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Year_sales['SALES'].max()+100000]))
    st.plotly_chart(fig_line,use_container_width=True)

with col2:
    Country_sales=filter_df.groupby('COUNTRY')['SALES'].sum().reset_index()
    fig_bar=px.bar(Country_sales,x='COUNTRY',y='SALES',title= 'Toatl Sales By Country')
    st.plotly_chart(fig_bar,use_container_width=True)
st.subheader("FILTERED_DATA")
st.dataframe(filter_df)
