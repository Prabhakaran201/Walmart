import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
features = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\features.csv")
stores = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\stores.csv")
train = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\train.csv")
test = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\test.csv")

# Merge datasets
merged = train.merge(stores, how='left').merge(features, how='left')

def preprocess_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week
preprocess_data(merged)

# Sidebar Filters
st.sidebar.header("Filter Data")

date_filter = st.sidebar.date_input("Select Date Range", (merged['Date'].min(), merged['Date'].max()))
dept_filter = st.sidebar.multiselect("Select Department", merged['Dept'].unique())

st.sidebar.header("Store Filters")
type_filter = st.sidebar.multiselect("Select Store Type", stores['Type'].unique())
size_filter = st.sidebar.slider("Select Store Size", int(stores['Size'].min()), int(stores['Size'].max()), (int(stores['Size'].min()), int(stores['Size'].max())))

st.sidebar.header("Feature Filters")
temp_filter = st.sidebar.slider("Temperature", float(features['Temperature'].min()), float(features['Temperature'].max()), (float(features['Temperature'].min()), float(features['Temperature'].max())))
fuel_price_filter = st.sidebar.slider("Fuel Price", float(features['Fuel_Price'].min()), float(features['Fuel_Price'].max()), (float(features['Fuel_Price'].min()), float(features['Fuel_Price'].max())))
cpi_filter = st.sidebar.slider("CPI", float(features['CPI'].min()), float(features['CPI'].max()), (float(features['CPI'].min()), float(features['CPI'].max())))
unemployment_filter = st.sidebar.slider("Unemployment", float(features['Unemployment'].min()), float(features['Unemployment'].max()), (float(features['Unemployment'].min()), float(features['Unemployment'].max())))
holiday_filter = st.sidebar.selectbox("Holiday Status", ["All", True, False])

# Apply Filters
filtered_data = merged.copy()
filtered_data = filtered_data[(filtered_data['Date'] >= pd.to_datetime(date_filter[0])) & (filtered_data['Date'] <= pd.to_datetime(date_filter[1]))]
if dept_filter:
    filtered_data = filtered_data[filtered_data['Dept'].isin(dept_filter)]
if type_filter:
    filtered_data = filtered_data[filtered_data['Type'].isin(type_filter)]
filtered_data = filtered_data[(filtered_data['Size'] >= size_filter[0]) & (filtered_data['Size'] <= size_filter[1])]
filtered_data = filtered_data[(filtered_data['Temperature'] >= temp_filter[0]) & (filtered_data['Temperature'] <= temp_filter[1])]
filtered_data = filtered_data[(filtered_data['Fuel_Price'] >= fuel_price_filter[0]) & (filtered_data['Fuel_Price'] <= fuel_price_filter[1])]
filtered_data = filtered_data[(filtered_data['CPI'] >= cpi_filter[0]) & (filtered_data['CPI'] <= cpi_filter[1])]
filtered_data = filtered_data[(filtered_data['Unemployment'] >= unemployment_filter[0]) & (filtered_data['Unemployment'] <= unemployment_filter[1])]
if holiday_filter != "All":
    filtered_data = filtered_data[filtered_data['IsHoliday'] == holiday_filter]

# Display Data
st.title("Walmart Sales Dashboard")
st.dataframe(filtered_data)

# Visualizations
st.subheader("Sales Trends Over Time")
fig = px.line(filtered_data, x='Date', y='Weekly_Sales', title="Weekly Sales Over Time")
st.plotly_chart(fig)

st.subheader("Store Type Popularity")
fig = px.pie(filtered_data, values=filtered_data['Type'].value_counts().values, names=filtered_data['Type'].value_counts().index, title='Store Type Distribution')
st.plotly_chart(fig)

st.subheader("Average Sales Per Store Type")
avg_sales = filtered_data.groupby('Type')['Weekly_Sales'].mean().reset_index()
fig = px.bar(avg_sales, x='Type', y='Weekly_Sales', title='Average Sales per Store Type', color_discrete_sequence=["Blue"])
st.plotly_chart(fig)

st.subheader("Monthly Sales Trends")
monthly_sales = filtered_data.groupby(['Year', 'Month'])['Weekly_Sales'].mean().reset_index()
fig = px.line(monthly_sales, x='Month', y='Weekly_Sales', color='Year', title="Average Monthly Sales")
st.plotly_chart(fig)

st.subheader("Sales Distribution Across Departments")
dept_sales = filtered_data.groupby('Dept')['Weekly_Sales'].mean().reset_index()
fig = px.bar(dept_sales, x='Dept', y='Weekly_Sales', title="Average Sales per Department", color_discrete_sequence=["#DC143C"])
st.plotly_chart(fig)

st.subheader("Store Size vs Sales")
fig = px.scatter(filtered_data, x='Size', y='Weekly_Sales', color='Type', title="Store Size vs Weekly Sales")
st.plotly_chart(fig)

st.subheader("Fuel Price vs Sales")
fig = px.scatter(filtered_data, x='Fuel_Price', y='Weekly_Sales', color='Type', title="Fuel Price vs Weekly Sales")
st.plotly_chart(fig)

st.subheader("Unemployment vs Sales")
fig = px.scatter(filtered_data, x='Unemployment', y='Weekly_Sales', color='Type', title="Unemployment vs Weekly Sales")
st.plotly_chart(fig)

st.subheader("Correlation Matrix")
numeric_data = filtered_data.select_dtypes(include=['number'])
fig = px.imshow(numeric_data.corr(), title='Correlation Matrix', color_continuous_scale='Reds')
st.plotly_chart(fig)

# Additional Charts
st.subheader("Simple Scatter Chart")
st.scatter_chart(filtered_data[['Size', 'Weekly_Sales']])

st.subheader("Simple Bar Chart")
st.bar_chart(filtered_data[['Dept', 'Weekly_Sales']].set_index('Dept'))
