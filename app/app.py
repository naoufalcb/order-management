import streamlit as st
import pandas as pd
from logic import load_storage, append_orders

st.set_page_config(layout="wide")
st.title("Orders Importer")

uploaded = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded:
    df_upload = pd.read_excel(uploaded)
    st.subheader("Preview of Uploaded File")
    st.dataframe(df_upload, use_container_width=True)

    if st.button("Append to CSV"):
        try:
            new_rows, full_csv = append_orders(df_upload)
            st.success("Rows appended successfully.")

            st.subheader("📌 Newly Added Rows")
            st.dataframe(new_rows, use_container_width=True)

            st.subheader("📦 Current CSV Storage")
            st.dataframe(full_csv, use_container_width=True)

        except ValueError as e:
            st.error(str(e))

else:
    st.subheader("📦 Current CSV Storage")
    st.dataframe(load_storage(), use_container_width=True)
