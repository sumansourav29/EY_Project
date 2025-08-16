import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Crypto Exchange", layout="wide")

# ----------------------------
# Custom CSS for Dark Theme
# ----------------------------
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #111111;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        background-color: #0d0d0d;
        border-bottom: 1px solid #333;
    }
    .header .logo {
        font-size: 22px;
        font-weight: bold;
        color: gold;
    }
    .header .menu {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    .menu-item {
        color: white;
        cursor: pointer;
    }
    .profile-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: gold;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        cursor: pointer;
    }
    .card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown("""
<div class="header">
    <div class="logo">Crypto Exchange</div>
    <div class="menu">
        <div class="menu-item">Dashboard</div>
        <div class="menu-item">Charts</div>
        <div class="menu-item">Wallet</div>
        <div class="menu-item">News</div>
        <div class="menu-item">Settings</div>
        <div class="profile-circle">S</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Dashboard Layout
# ----------------------------
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("<div class='card'><h3>Total Balance</h3><h1>$154,610</h1></div>", unsafe_allow_html=True)

    # Portfolio
    st.markdown("<div class='card'><h3>My Portfolio</h3>", unsafe_allow_html=True)
    portfolio = {
        "Bitcoin (BTC)": ["37%", "+2.5%"],
        "Ethereum (ETH)": ["20%", "-1.5%"],
        "Tether (USDT)": ["23%", "-3.5%"],
        "Ripple (XRP)": ["17%", "+3.5%"],
    }
    for coin, stats in portfolio.items():
        st.markdown(f"<p>{coin}: {stats[0]} | {stats[1]}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Fake Data for Chart
    x = pd.date_range("2023-01-01", periods=50)
    y = np.cumsum(np.random.randn(50)) + 30000

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color="gold", width=3)))
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=30, b=0),
        height=400,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)
