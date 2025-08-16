import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(page_title="Crypto Exchange", layout="wide")

# ----------------------------
# Header
# ----------------------------
st.markdown("""
    <style>
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
    .crypto-card {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        color: white;
        text-align: center;
    }
    .price {
        font-size: 20px;
        font-weight: bold;
    }
    .change-pos {
        color: lime;
        font-weight: bold;
    }
    .change-neg {
        color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

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
# Crypto List
# ----------------------------
cryptos = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Binance Coin": "BNB-USD",
    "Cardano": "ADA-USD",
    "Ripple": "XRP-USD",
    "Solana": "SOL-USD"
}

cols = st.columns(len(cryptos))

# ----------------------------
# Loop Coins
# ----------------------------
for i, (name, ticker) in enumerate(cryptos.items()):
    try:
        data = yf.download(ticker, period="7d", interval="1h")

        if data.empty:
            with cols[i]:
                st.markdown(f"<div class='crypto-card'><h4>{name}</h4><h3>N/A</h3><p>No Data</p></div>", unsafe_allow_html=True)
        else:
            latest_price = data["Close"].iloc[-1]
            prev_price = data["Close"].iloc[-24] if len(data) > 24 else data["Close"].iloc[0]

            change_pct = ((latest_price - prev_price) / prev_price) * 100
            change_class = "change-pos" if change_pct >= 0 else "change-neg"
            change_symbol = "↑" if change_pct >= 0 else "↓"

            # Trend line
            color = "lime" if latest_price > data["Close"].iloc[0] else "red"
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                line=dict(color=color, width=2)
            ))
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=0, r=0, t=0, b=0),
                height=100,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )

            with cols[i]:
                st.markdown(
                    f"<div class='crypto-card'>"
                    f"<h4>{name}</h4>"
                    f"<div class='price'>${latest_price:,.2f}</div>"
                    f"<div class='{change_class}'>{change_symbol} {change_pct:.2f}% (24h)</div>"
                    f"</div>", unsafe_allow_html=True
                )
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        with cols[i]:
            st.markdown(f"<div class='crypto-card'><h4>{name}</h4><h3>Error</h3><p>{str(e)}</p></div>", unsafe_allow_html=True)
