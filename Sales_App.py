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
Month = st.sidebar.multiselect('Select Month:',df['MONTH_ID'].unique(),default=df['MONTH_ID'].unique())
Quarter = st.sidebar.multiselect('Select Quarter:',df['QTR_ID'].unique(),default=df['QTR_ID'].unique())
Country = st.sidebar.multiselect('Select Country:',df['COUNTRY'].unique(),default=df['COUNTRY'].unique())

filter_df = df[(df['STATUS'].isin(Status)) & (df['YEAR_ID'].isin(Year)) & (df['COUNTRY'].isin(Country)) ]

col1, col2, col3 = st.columns(3)
col1.metric('Total Sales',f"${filter_df['SALES'].sum():,}")
col2.metric('Average Sales',f"${filter_df['SALES'].mean():.0f}")
col3.metric('Records',len(filter_df))
Year_sales=filter_df.groupby('YEAR_ID')['SALES'].sum().reset_index()
fig_line1 = px.line(Year_sales,x= 'YEAR_ID',y= 'SALES',title="Yearly Sales" )
fig_line1.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Year_sales['SALES'].max()+100000]))
st.plotly_chart(fig_line1,use_container_width=True)

Month_sales=filter_df.groupby('MONTH_ID')['SALES'].sum().reset_index()
fig_line2 = px.line(Month_sales,x= 'MONTH_ID',y= 'SALES',title="Monthly Sales" )
fig_line2.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,Month_sales['SALES'].max()+100000]))
st.plotly_chart(fig_line2,use_container_width=True)


QTR_sales=filter_df.groupby('QTR_ID')['SALES'].sum().reset_index()
fig_line3 = px.line(QTR_sales,x= 'QTR_ID',y= 'SALES',title="Quarterly Sales" )
fig_line3.update_layout(xaxis= dict (type= 'category'),yaxis= dict(range=[0,QTR_sales['SALES'].max()+100000]))
st.plotly_chart(fig_line3,use_container_width=True)

Product_sales =filter_df.groupby("PRODUCTLINE")['SALES'].mean().reset_index()
fig_pie = px.pie(data_frame = filter_df, names = "PRODUCTLINE",values = "SALES",title = "Product_SALES")
st.plotly_chart(fig_pie,use_container_width = True)

fig_bar1 = px.bar(data_frame = filter_df, x = "PRODUCTLINE",y= "SALES",title = "Product_SALES")
st.plotly_chart(fig_bar1,use_container_width = True)

Country_sales=filter_df.groupby('COUNTRY')['SALES'].sum().reset_index()
fig_bar=px.bar(Country_sales,x='COUNTRY',y='SALES',title= 'Totall Sales By Country')
st.plotly_chart(fig_bar,use_container_width=True)
fig_pie1=px.pie(Country_sales,names='COUNTRY',values='SALES',title= 'Totall Sales By Country')
st.plotly_chart(fig_pie1,use_container_width=True)



fig8 = px.scatter_3d(filter_df,x='PRODUCTLINE',y='SALES',z='COUNTRY',color='SALES')
st.plotly_chart(fig8,use_container_width=True)

st.subheader("Summary Statistics")
st.dataframe(filter_df.describe())
st.subheader("FILTERED_DATA")
st.dataframe(filter_df)
