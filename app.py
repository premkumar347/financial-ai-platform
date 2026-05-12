import streamlit as st

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

st.metric(
    label="Recommendation",
    value="SELL"
)

st.metric(
    label="Confidence",
    value="64.69%"
)

st.metric(
    label="Risk Level",
    value="MEDIUM"
)

st.write("AI-based stock analysis dashboard")
