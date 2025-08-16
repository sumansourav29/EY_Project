import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# ---------------------------
# Page Setup
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
        margin-bottom: 20px;
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
    .card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.5);
    }
    .card h3 {
        margin: 0;
        font-size: 18px;
        color: white;
    }
    .metric {
        font-size: 14px;
        margin-bottom: 5px;
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
# Function to create crypto card
# ---------------------------
def crypto_card(symbol, name):
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
            margin=dict(l=0, r=0, t=0, b=0),
            height=120,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.markdown(f"""
            <div class="card">
                <h3>{name}</h3>
                <div class="metric">💵 ${current_price:,.2f}</div>
                <div class="metric">📈 {change:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    except Exception as e:
        st.error(f"Error loading {name}: {e}")


# ---------------------------
# Display Small Crypto Cards in Grid
# ---------------------------
col1, col2, col3 = st.columns(3)
with col1: crypto_card("BTC-USD", "Bitcoin")
with col2: crypto_card("ETH-USD", "Ethereum")
with col3: crypto_card("BNB-USD", "Binance Coin")

col4, col5, col6 = st.columns(3)
with col4: crypto_card("ADA-USD", "Cardano")
with col5: crypto_card("XRP-USD", "Ripple")
with col6: crypto_card("SOL-USD", "Solana")
