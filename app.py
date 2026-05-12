import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AI Financial Intelligence",
    layout="wide"
)

st.title("AI Financial Intelligence Platform")

st.subheader("Multi-Stock Prediction System")

model = joblib.load("stock_model.pkl")

stocks = {
    "AAPL":[55,0.5,210,220,1000000,0.02,0.03,0.01,2500000000000,30,0.08,0.25,1.2,0],
    "MSFT":[62,0.7,320,330,1200000,0.03,0.02,0.02,2800000000000,35,0.10,0.30,1.1,1],
    "GOOGL":[48,0.2,140,150,900000,0.01,0.02,0.01,1800000000000,28,0.09,0.27,1.0,2],
    "AMZN":[70,1.1,180,195,1500000,0.04,0.05,0.03,1700000000000,60,0.12,0.15,1.4,3],
    "TSLA":[80,1.8,250,280,2000000,0.06,0.08,0.05,800000000000,75,0.20,0.10,2.0,4]
}

stock = st.selectbox(
    "Select Stock",
    list(stocks.keys())
)

st.write("Selected Stock:", stock)

features = np.array(stocks[stock]).reshape(1,-1)

pred = model.predict(features)[0]

prob = model.predict_proba(features)[0]

confidence = round(max(prob)*100,2)

if confidence < 60:
    risk = "HIGH"
elif confidence < 75:
    risk = "MEDIUM"
else:
    risk = "LOW"

signal = "BUY" if pred == 1 else "SELL"

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
