import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
features = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\features.csv")
stores = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\stores.csv")
train = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\train.csv")
test = pd.read_csv("C:\\Users\\jayapratha\\Desktop\\walmart\\dataset\\test.csv")

# Merge datasets
merged = train.merge(stores, how='left').merge(features, how='left')
testing_merged = test.merge(stores, how='left').merge(features, how='left')

# Convert Date to datetime format
merged['Date'] = pd.to_datetime(merged['Date'])
testing_merged['Date'] = pd.to_datetime(testing_merged['Date'])

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [merged.Date.min(), merged.Date.max()])
dept = st.sidebar.multiselect("Select Department", merged.Dept.unique())

st.sidebar.header("Store Filters")
store_type = st.sidebar.multiselect("Select Store Type", merged.Type.unique())
store_size = st.sidebar.slider("Select Store Size Range", int(merged.Size.min()), int(merged.Size.max()), (int(merged.Size.min()), int(merged.Size.max())))

st.sidebar.header("Feature Filters")
temp_range = st.sidebar.slider("Select Temperature Range", float(merged.Temperature.min()), float(merged.Temperature.max()), (float(merged.Temperature.min()), float(merged.Temperature.max())))
fuel_price_range = st.sidebar.slider("Select Fuel Price Range", float(merged.Fuel_Price.min()), float(merged.Fuel_Price.max()), (float(merged.Fuel_Price.min()), float(merged.Fuel_Price.max())))
cpi_range = st.sidebar.slider("Select CPI Range", float(merged.CPI.min()), float(merged.CPI.max()), (float(merged.CPI.min()), float(merged.CPI.max())))
unemployment_range = st.sidebar.slider("Select Unemployment Range", float(merged.Unemployment.min()), float(merged.Unemployment.max()), (float(merged.Unemployment.min()), float(merged.Unemployment.max())))
is_holiday = st.sidebar.radio("Is Holiday", ["All", True, False])

# Apply filters
filtered_data = merged[merged["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

if dept:
    filtered_data = filtered_data[filtered_data.Dept.isin(dept)]
if store_type:
    filtered_data = filtered_data[filtered_data.Type.isin(store_type)]
filtered_data = filtered_data[(filtered_data.Size.between(store_size[0], store_size[1]))]
filtered_data = filtered_data[(filtered_data.Temperature.between(temp_range[0], temp_range[1]))]
filtered_data = filtered_data[(filtered_data.Fuel_Price.between(fuel_price_range[0], fuel_price_range[1]))]
filtered_data = filtered_data[(filtered_data.CPI.between(cpi_range[0], cpi_range[1]))]
filtered_data = filtered_data[(filtered_data.Unemployment.between(unemployment_range[0], unemployment_range[1]))]
if is_holiday != "All":
    filtered_data = filtered_data[filtered_data.IsHoliday == is_holiday]

# Dashboard title
st.title("Walmart Sales Analysis Dashboard")

# Box plot for Weekly Sales Distribution
st.subheader("Weekly Sales Distribution")
fig = px.box(filtered_data, y='Weekly_Sales', title='Weekly Sales Distribution')
st.plotly_chart(fig)

# Violin plot for Sales by Store Type
st.subheader("Sales Distribution by Store Type")
fig = px.violin(filtered_data, x='Type', y='Weekly_Sales', box=True, points='all', title='Sales by Store Type')
st.plotly_chart(fig)

# Heatmap for Weekly Sales Trends
st.subheader("Weekly Sales Trends Over Time")
sales_pivot = filtered_data.pivot_table(values='Weekly_Sales', index=filtered_data.Date.dt.isocalendar().week,  # ✅ Corrected 
                                        columns=filtered_data.Date.dt.year, 
                                        aggfunc='mean')

plt.figure(figsize=(12, 6))
sns.heatmap(sales_pivot, cmap='coolwarm', annot=False)
st.pyplot(plt)

# Sunburst Chart: Store Type & Dept Breakdown
st.subheader("Sales Breakdown by Store Type and Department")
fig = px.sunburst(filtered_data, path=['Type', 'Dept'], values='Weekly_Sales', title='Sales Breakdown')
st.plotly_chart(fig)

# Bubble Chart: Store Size, Fuel Price vs. Sales
st.subheader("Impact of Store Size and Fuel Price on Sales")
fig = px.scatter(filtered_data, 
                 x='Size', 
                 y='Fuel_Price', 
                 size=filtered_data['Weekly_Sales'].abs(),  # ✅ Ensure positive values
                 color='Type', 
                 title='Store Size & Fuel Price vs Sales')

st.plotly_chart(fig)

# Treemap for Dept-wise Sales Contribution
st.subheader("Department-wise Sales Contribution")
fig = px.treemap(filtered_data, path=['Dept'], values='Weekly_Sales', title='Dept Sales Contribution')
st.plotly_chart(fig)
