import os
import pandas as pd

CSV_PATH = "data/orders.csv"

HEADER = [
    "Order ID","Order","Paid at","Product Name","ERP SKU","SKU",
    "Quantity","Shipping Name","Country","Tracking Number","Cost"
]

def ensure_csv():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        pd.DataFrame(columns=HEADER).to_csv(CSV_PATH, index=False)

def load_storage():
    ensure_csv()
    df = pd.read_csv(CSV_PATH)
    df = preprocess(df)
    df.to_csv(CSV_PATH, index=False)
    return df

def preprocess(df):
    # Drop empty rows/totals
    if "Order ID" in df.columns:
        df = df[df["Order ID"].notna()]

    # Keep only columns we expect
    df = df[[c for c in HEADER if c in df.columns]]

    df = df.fillna("")
    return df

def append_orders(uploaded_df):
    """
    Append uploaded orders to storage.
    Returns the newly added rows and the updated storage.
    Raises ValueError if any duplicate Order numbers are detected.
    """
    ensure_csv()

    uploaded_clean = preprocess(uploaded_df)
    storage = load_storage()

    # Convert both columns to string for robust comparison
    storage_orders = storage["Order"].astype(str)
    uploaded_orders = uploaded_clean["Order"].astype(str)

    # Check for duplicates
    duplicates = set(storage_orders) & set(uploaded_orders)
    if duplicates:
        raise ValueError(f"Duplicate Order numbers detected: {', '.join(duplicates)}. Append canceled.")

    # Append
    final = pd.concat([storage, uploaded_clean], ignore_index=True)
    final.to_csv(CSV_PATH, index=False)

    # Return newly added rows and full CSV
    return uploaded_clean, final
