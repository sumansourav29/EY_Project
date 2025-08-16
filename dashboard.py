import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# ---------------------------
# Header
# ---------------------------
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.markdown("""
    <style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        background-color: #111;
        color: white;
        border-radius: 10px;
    }
    .header .left {
        font-size: 24px;
        font-weight: bold;
    }
    .header .right {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    .circle {
        width: 35px;
        height: 35px;
        background-color: #444;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    </style>

    <div class="header">
        <div class="left">💰 Crypto</div>
        <div class="right">
            <div>Dashboard</div>
            <div>Chart</div>
            <div>Wallet</div>
            <div>News</div>
            <div class="circle">⚙️</div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ---------------------------
# Function to create crypto box
# ---------------------------
def crypto_box(symbol, name):
    try:
        data = yf.download(symbol, period="7d", interval="1h")
        if data.empty:
            st.error(f"No data for {name}")
            return

        current_price = float(data["Close"].iloc[-1])
        start_price = float(data["Close"].iloc[0])
        change = ((current_price - start_price) / start_price) * 100

        line_color = "lime" if current_price > start_price else "red"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index, y=data["Close"],
            mode="lines",
            line=dict(color=line_color, width=2)
        ))
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            margin=dict(l=10, r=10, t=10, b=10),
            height=200
        )

        st.markdown(f"### {name}")
        st.metric(label="Price", value=f"${current_price:,.2f}", delta=f"{change:.2f}%")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading {name}: {e}")


# ---------------------------
# Display 6 Crypto Boxes
# ---------------------------
col1, col2, col3 = st.columns(3)
with col1:
    crypto_box("BTC-USD", "Bitcoin")
with col2:
    crypto_box("ETH-USD", "Ethereum")
with col3:
    crypto_box("BNB-USD", "Binance Coin")

col4, col5, col6 = st.columns(3)
with col4:
    crypto_box("ADA-USD", "Cardano")
with col5:
    crypto_box("XRP-USD", "Ripple")
with col6:
    crypto_box("SOL-USD", "Solana")
