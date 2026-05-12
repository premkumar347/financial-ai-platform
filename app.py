import streamlit as st
import random

st.set_page_config(
    page_title="AI Financial Intelligence",
    layout="wide"
)

st.title("AI Financial Intelligence Platform")

st.subheader("Multi-Stock Prediction System")

stock = st.selectbox(
    "Select Stock",
    ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
)

st.write("Selected Stock:", stock)

signals = {
    "AAPL":"BUY",
    "MSFT":"BUY",
    "GOOGL":"HOLD",
    "AMZN":"SELL",
    "TSLA":"SELL"
}

confidence_data = {
    "AAPL":82.5,
    "MSFT":76.4,
    "GOOGL":68.2,
    "AMZN":59.8,
    "TSLA":64.6
}

signal = signals[stock]

confidence = confidence_data[stock]

if confidence < 60:
    risk = "HIGH"
elif confidence < 75:
    risk = "MEDIUM"
else:
    risk = "LOW"

st.metric(
    label="Recommendation",
    value=signal
)

st.metric(
    label="Confidence",
    value=f"{confidence}%"
)

st.metric(
    label="Risk Level",
    value=risk
)

st.write("AI-based stock analysis dashboard")
