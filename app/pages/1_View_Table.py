import streamlit as st
from logic import load_storage
import pandas as pd

st.set_page_config(layout="wide")
st.title("📦 Full Orders Table")

df = load_storage()

# Convert Paid at to datetime for filtering
df["Paid at"] = pd.to_datetime(df["Paid at"], errors="coerce")

# -------- Sidebar Filters --------
st.sidebar.header("Filters")

# Date range filter
min_date = df["Paid at"].min()
max_date = df["Paid at"].max()
date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date()
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    mask_date = (df["Paid at"].dt.date >= start) & (df["Paid at"].dt.date <= end)
    df = df[mask_date]

# Quantity filter
min_quantity = st.sidebar.number_input(
    "Minimum total items per order", min_value=1, value=1, step=1
)
quantity_per_order = df.groupby("Order")["Quantity"].sum().reset_index()
orders_to_keep = quantity_per_order[quantity_per_order["Quantity"] >= min_quantity]["Order"]
df = df[df["Order"].isin(orders_to_keep)]

# Product name search
product_search = st.sidebar.text_input("Search Product Name contains")
if product_search:
    df = df[df["Product Name"].str.contains(product_search, case=False, na=False)]

# Multi-order search (comma-separated)
order_search = st.sidebar.text_input("Search Orders (comma-separated)")
if order_search:
    # Clean user input
    orders_list = [o.strip() for o in order_search.split(",") if o.strip()]
    
    # Convert df["Order"] to int if possible, then to string
    df_orders_str = df["Order"].fillna(0).astype(int).astype(str)
    
    # Filter
    df = df[df_orders_str.isin(orders_list)]


# -------- Display --------
st.subheader("Filtered Orders")
st.dataframe(df, use_container_width=True)
