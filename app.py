import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import joblib

from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

st.set_page_config(
    page_title="AI Financial Intelligence",
    layout="wide"
)

st.title("AI Financial Intelligence Platform")

st.subheader(
    "Real Time Multi Stock Prediction System"
)

# load model
model = joblib.load(
    "stock_model.pkl"
)

# stock selection
stock = st.selectbox(

    "Select Stock",

    ["AAPL","MSFT","GOOGL","AMZN","TSLA"]
)

# latest stock data
data = yf.download(

    stock,

    period="1y"
)

# fixing columns issue
if isinstance(data.columns, pd.MultiIndex):

    data.columns = (
        data.columns.get_level_values(0)
    )

# RSI
data["RSI"] = RSIIndicator(
    close=data["Close"]
).rsi()

# MACD
data["MACD"] = MACD(
    close=data["Close"]
).macd()

# EMA
data["EMA"] = EMAIndicator(
    close=data["Close"]
).ema_indicator()

# Bollinger Bands
bb = BollingerBands(
    close=data["Close"]
)

data["BB_High"] = (
    bb.bollinger_hband()
)

data["BB_Low"] = (
    bb.bollinger_lband()
)

# daily return
data["Daily_Return"] = (
    data["Close"].pct_change()
)

# volatility
data["Volatility"] = (
    (data["High"] - data["Low"])
    /
    data["Close"]
)

# volume change
data["Volume_Change"] = (
    data["Volume"].pct_change()
)

# momentum
data["Momentum"] = (
    data["Close"]
    -
    data["Close"].shift(10)
)

# moving average ratio
data["MA_Ratio"] = (
    data["Close"]
    /
    data["EMA"]
)

# trend strength
data["Trend_Strength"] = (
    data["MACD"]
    *
    data["RSI"]
)

# stock encoding
stock_map = {

    "AAPL":0,
    "MSFT":1,
    "GOOGL":2,
    "AMZN":3,
    "TSLA":4
}

data["Stock_Code"] = (
    stock_map[stock]
)

# remove missing rows
data.dropna(inplace=True)

features = [

    "RSI",
    "MACD",
    "EMA",
    "BB_High",
    "BB_Low",
    "Volume",
    "Daily_Return",
    "Volatility",
    "Volume_Change",
    "Momentum",
    "MA_Ratio",
    "Trend_Strength",
    "Stock_Code"
]

latest = (
    data[features]
    .tail(1)
)

# prediction
pred = model.predict(latest)[0]

# confidence
prob = model.predict_proba(latest)[0]

confidence = round(
    max(prob) * 100,
    2
)

# recommendation logic
if confidence < 60:

    signal = "HOLD"

elif pred == 1:

    signal = "BUY"

else:

    signal = "SELL"

# volatility risk
avg_volatility = (

    data["Volatility"]

    .tail(30)

    .mean()
)

if avg_volatility < 0.02:

    risk = "LOW"

elif avg_volatility < 0.05:

    risk = "MEDIUM"

else:

    risk = "HIGH"

# AI explanations
latest_rsi = (
    data["RSI"]
    .iloc[-1]
)

latest_macd = (
    data["MACD"]
    .iloc[-1]
)

reasons = []

if latest_rsi > 70:

    reasons.append(
        "RSI indicates overbought market"
    )

elif latest_rsi < 30:

    reasons.append(
        "RSI indicates oversold recovery"
    )

if latest_macd > 0:

    reasons.append(
        "MACD shows bullish momentum"
    )

else:

    reasons.append(
        "MACD shows bearish momentum"
    )

if risk == "HIGH":

    reasons.append(
        "Market volatility is high"
    )

# UI
st.metric(
    "Recommendation",
    signal
)

st.metric(
    "Confidence",
    f"{confidence}%"
)

st.metric(
    "Risk Level",
    risk
)

# chart
st.subheader(
    "Stock Price Chart"
)

st.line_chart(
    data["Close"]
)

# explanations
st.subheader(
    "AI Analysis"
)

for r in reasons:

    st.write("-", r)

# latest data
st.subheader(
    "Latest Market Data"
)

st.dataframe(
    data.tail(5)
)
