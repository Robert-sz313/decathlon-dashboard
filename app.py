import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from data_read import *

st.set_page_config(page_title="Decathlon Customer Dashboard", layout="wide")
st.title("Decathlon Customer Dashboard")

# ====== Dane ======
orders = load_orders()
customer_orders = load_customer_orders()
sports = load_sports()

# ====== KPI ======
sports_count = sports.groupby("customer_id")["sport"].nunique().reset_index()
sports_count.columns = ["customer_id", "num_sports"]

orders_count = customer_orders.groupby("customer_id")["order_id"].nunique().reset_index()
orders_count.columns = ["customer_id", "num_orders"]

avg_order_value = orders["value"].mean()
repeat_customers_pct = (orders_count["num_orders"] > 1).mean() * 100
multi_sport_clients = (sports_count["num_sports"] > 2).sum()

sport_counts = sports["sport"].value_counts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Clients with >2 sports", multi_sport_clients)
col2.metric("Most popular sport", sport_counts.idxmax())
col3.metric("Least popular sport", sport_counts.idxmin())
col4.metric("Average order value", f"{avg_order_value:.2f}")
st.subheader(f"% Clients with >1 order: {repeat_customers_pct:.1f}%")

# ====== Wykresy w go ======
st.header("Visualizations")

# 1. Histogram liczby sportów na klienta
hist_sports = go.Figure()
hist_sports.add_trace(go.Histogram(
    x=sports_count["num_sports"],
    nbinsx=10,
    marker_color='blue'
))
hist_sports.update_layout(
    title="Number of Sports per Customer",
    xaxis_title="Number of Sports",
    yaxis_title="Number of Customers"
)
st.plotly_chart(hist_sports, use_container_width=True)

# 2. Popularność sportów
bar_sports = go.Figure()
bar_sports.add_trace(go.Bar(
    x=sport_counts.index,
    y=sport_counts.values,
    marker_color='green'
))
bar_sports.update_layout(
    title="Sport Popularity",
    xaxis_title="Sport",
    yaxis_title="Number of Customers"
)
st.plotly_chart(bar_sports, use_container_width=True)

# 3. Histogram wartości zamówień
hist_orders = go.Figure()
hist_orders.add_trace(go.Histogram(
    x=orders["value"],
    nbinsx=20,
    marker_color='orange'
))
hist_orders.update_layout(
    title="Order Value Distribution",
    xaxis_title="Order Value",
    yaxis_title="Number of Orders"
)
st.plotly_chart(hist_orders, use_container_width=True)
