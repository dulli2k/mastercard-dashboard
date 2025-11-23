# src/frontend/dashboard.py
import streamlit as st

st.set_page_config(page_title="Inclusive Growth Dashboard", layout="wide")

st.title("💳 Mastercard Inclusive Growth Dashboard")
st.write("Analyze economic inclusion through spending, business, and growth metrics.")

st.header("Spending Trend Example")
st.line_chart({"Spending Index": [100, 120, 140, 160, 180]})
