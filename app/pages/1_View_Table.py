import streamlit as st
from logic import load_storage
import pandas as pd

st.set_page_config(layout="wide")
st.title("📦 Full Orders Table")

df = load_storage()

# Convert Paid at to datetime (safe)
if "Paid at" in df.columns and not df.empty:
    df["Paid at"] = pd.to_datetime(df["Paid at"], errors="coerce")
else:
    df["Paid at"] = pd.Series(dtype="datetime64[ns]")

# -------- Sidebar Filters --------
st.sidebar.header("Filters")

if df.empty:
    st.warning("No data available yet.")
    st.stop()  # Stop the rest of the page from executing

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
    orders_list = [o.strip() for o in order_search.split(",") if o.strip()]
    df = df[df["Order"].astype(str).isin(orders_list)]

# -------- Display --------
st.subheader("Filtered Orders")
st.dataframe(df, use_container_width=True)
