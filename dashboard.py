# app.py
import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st

# Plotly for charts
import plotly.graph_objects as go
import plotly.express as px

# Try live data via yfinance (optional)
try:
    import yfinance as yf
    YF_OK = True
except Exception:
    YF_OK = False

# ----------------------------
# Page Config & Basic Styles
# ----------------------------
st.set_page_config(
    page_title="NebulaX Exchange",
    page_icon="📈",
    layout="wide"
)

CUSTOM_CSS = """
<style>
/* Clean topbar */
.topbar {
  position: sticky; top: 0; z-index: 999;
  background: linear-gradient(90deg, #0B1020 0%, #0F1535 100%);
  padding: 10px 14px; border-bottom: 1px solid #1f2745; border-radius: 0 0 14px 14px;
}
.topbar h1, .topbar .right { color: #e8ebff; }
.kpi-card {
  border: 1px solid #202640; border-radius: 14px; padding: 12px; background: #0e1330;
}
.block {
  border: 1px solid #202640; border-radius: 14px; padding: 14px; background: #0b1026;
}
.section-title { font-weight: 700; margin-bottom: 8px; }
.buy { background: #0f2e1c; border: 1px solid #1c6b3e; }
.sell { background: #2e1210; border: 1px solid #7a2a24; }
.small-muted { color: #93a1c7; font-size: 12px; }
.metric-chip {
  display:inline-block; padding:4px 10px; border-radius:20px;
  border:1px solid #2b3458; background:#0c1337; margin-right:6px;
}
.login-avatar {
  width: 34px; height: 34px; border-radius: 50%; background: #1b2250;
  display:flex; align-items:center; justify-content:center; color:#e8ebff; font-weight:700;
  border:1px solid #2b3458;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------
# Session State (Auth + Data)
# ----------------------------
if "auth" not in st.session_state:
    st.session_state.auth = {"logged_in": False, "username": None}

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "cash_usd": 12500.00,
        "positions": {
            "BTC-USD": 0.225,
            "ETH-USD": 2.8,
            "SOL-USD": 35.0,
        }
    }

if "open_orders" not in st.session_state:
    st.session_state.open_orders = []  # will store dicts
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# Demo users (for example only; do NOT use in production)
DEMO_USERS = {
    "suman": "password123",
    "demo": "demo"
}

# ----------------------------
# Helper Functions
# ----------------------------
SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD"]

def gen_demo_ohlc(n=300, start_price=30000, seed=42):
    """Generate demo OHLCV data."""
    rng = np.random.default_rng(seed)
    dt_index = pd.date_range(end=datetime.utcnow(), periods=n, freq="H")
    price = np.cumsum(rng.normal(0, 50, size=n)) + start_price
    high = price + rng.uniform(10, 60, size=n)
    low = price - rng.uniform(10, 60, size=n)
    open_ = np.roll(price, 1); open_[0] = price[0]
    close = price
    vol = rng.integers(50, 500, size=n) * 10
    df = pd.DataFrame({"Open": open_, "High": high, "Low": low, "Close": close, "Volume": vol}, index=dt_index)
    return df

def load_prices(symbol, period="7d", interval="1h", source="Demo"):
    if source == "Demo":
        base = {"BTC-USD": 65000, "ETH-USD": 3300, "SOL-USD": 140, "BNB-USD": 600, "XRP-USD": 0.6, "DOGE-USD": 0.2}.get(symbol, 100)
        return gen_demo_ohlc(n=300, start_price=base)
    if source == "Live (yfinance)" and YF_OK:
        df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)
        if df.empty:
            return gen_demo_ohlc(n=300, start_price=30000)
        # yfinance uses lowercase columns sometimes; normalize
        cols = {c: c.capitalize() for c in df.columns}
        df = df.rename(columns=cols)
        if "Volume" not in df.columns:
            df["Volume"] = 0
        return df
    # fallback
    return gen_demo_ohlc(n=300, start_price=30000)

def make_candlestick(df, ma1=20, ma2=50, title=""):
    d = df.copy()
    d["MA1"] = d["Close"].rolling(ma1).mean()
    d["MA2"] = d["Close"].rolling(ma2).mean()

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=d.index, open=d["Open"], high=d["High"], low=d["Low"], close=d["Close"],
        name="Price"
    ))
    fig.add_trace(go.Scatter(x=d.index, y=d["MA1"], mode="lines", name=f"MA{ma1}"))
    fig.add_trace(go.Scatter(x=d.index, y=d["MA2"], mode="lines", name=f"MA{ma2}"))

    # Secondary y for volume
    fig.add_trace(go.Bar(x=d.index, y=d["Volume"], name="Volume", opacity=0.3, yaxis="y2"))

    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(title="Price"),
        yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False)
    )
    return fig

def make_depth_chart(mid=100, spread=0.2, levels=30, seed=7):
    rng = np.random.default_rng(seed)
    prices_bid = np.array([mid - i*spread for i in range(1, levels+1)])[::-1]  # increasing
    qtys_bid = np.cumsum(rng.integers(1, 20, size=levels))
    prices_ask = np.array([mid + i*spread for i in range(1, levels+1)])
    qtys_ask = np.cumsum(rng.integers(1, 20, size=levels))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prices_bid, y=qtys_bid, fill='tozeroy', mode='lines', name='Bids'))
    fig.add_trace(go.Scatter(x=prices_ask, y=qtys_ask, fill='tozeroy', mode='lines', name='Asks'))
    fig.update_layout(
        title="Depth Chart",
        template="plotly_dark",
        xaxis_title="Price",
        yaxis_title="Cumulative Size",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

def make_orderbook_tables(mid_price, n=12, tick=1.0, seed=9):
    rng = np.random.default_rng(seed)
    asks = []
    bids = []
    for i in range(n):
        asks.append({"Price": round(mid_price + (i+1)*tick, 2), "Size": rng.integers(1, 7), "Total": 0})
        bids.append({"Price": round(mid_price - (i+1)*tick, 2), "Size": rng.integers(1, 7), "Total": 0})
    # Cum totals
    a_df = pd.DataFrame(asks)
    b_df = pd.DataFrame(bids)
    a_df["Total"] = a_df["Size"].cumsum()
    b_df["Total"] = b_df["Size"].cumsum()
    return a_df.iloc[::-1], b_df  # show asks descending, bids ascending

def est_quote(size, price):
    try:
        return float(size) * float(price)
    except Exception:
        return 0.0

def format_usd(x):
    return f"${x:,.2f}"

# ----------------------------
# Top Bar (with Login/Profile)
# ----------------------------
with st.container():
    st.markdown('<div class="topbar">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([0.28, 0.38, 0.20, 0.14])
    with c1:
        st.markdown("### 🪐 NebulaX Exchange")
        st.markdown('<span class="small-muted">Paper-trade demo • educational use</span>', unsafe_allow_html=True)
    with c2:
        st.text_input("Search markets", placeholder="Search BTC, ETH, SOL…", label_visibility="collapsed")
    with c3:
        k1, k2, k3 = st.columns(3)
        k1.metric("24h Volume", " $1.28B", "+3.1%")
        k2.metric("Open Interest", "$842M", "-0.4%")
        k3.metric("Funding", "0.010%", " ")
    with c4:
        r1, r2 = st.columns([0.5, 0.5])
        with r1:
            st.button("🔔", key="notif", help="Notifications")
        with r2:
            if st.session_state.auth["logged_in"]:
                st.markdown('<div class="login-avatar">🙂</div>', unsafe_allow_html=True)
                st.caption(f'Logged in as **{st.session_state.auth["username"]}**')
            else:
                if st.button("Login"):
                    st.session_state.show_login = True
    st.markdown('</div>', unsafe_allow_html=True)

# Inline Login Panel
if st.session_state.auth["logged_in"] is False and st.session_state.get("show_login", False):
    with st.expander("🔐 Login to NebulaX"):
        u = st.text_input("Username", placeholder="demo / suman")
        p = st.text_input("Password", type="password")
        colA, colB = st.columns([0.3, 0.7])
        with colA:
            if st.button("Sign In"):
                if u in DEMO_USERS and DEMO_USERS[u] == p:
                    st.session_state.auth["logged_in"] = True
                    st.session_state.auth["username"] = u
                    st.success("Logged in successfully.")
                    st.session_state.show_login = False
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials (try demo/demo)")
        with colB:
            st.markdown('<span class="small-muted">For demo only. Do not use real credentials.</span>', unsafe_allow_html=True)

# ----------------------------
# Sidebar: Balances & Watchlist
# ----------------------------
with st.sidebar:
    st.image("https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/bitcoin.svg", width=28)
    st.title("NebulaX")
    st.caption("Quick navigation")
    st.divider()

    st.subheader("💼 Wallet")
    cash = st.session_state.portfolio["cash_usd"]
    st.markdown(f"**Cash**: {format_usd(cash)}")
    for sym, qty in st.session_state.portfolio["positions"].items():
        st.write(f"{sym}: **{qty}**")

    st.write("")
    c_dep, c_wd = st.columns(2)
    with c_dep: st.button("➕ Deposit", use_container_width=True)
    with c_wd:  st.button("➖ Withdraw", use_container_width=True)

    st.divider()
    st.subheader("👀 Watchlist")

    source = st.selectbox("Data Source", ["Demo", "Live (yfinance)"] if YF_OK else ["Demo"])
    period = st.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=2)
    interval = st.selectbox("Interval", ["15m", "1h", "2h", "4h", "1d"], index=2)

    rows = []
    for s in SYMBOLS:
        dfw = load_prices(s, period=period, interval=interval, source=source)
        last = float(dfw["Close"].iloc[-1])
        prev = float(dfw["Close"].iloc[-2]) if len(dfw) > 1 else last
        chg = (last - prev) / prev * 100 if prev else 0
        rows.append({"Symbol": s, "Last": last, "24h %": chg})
    watch_df = pd.DataFrame(rows)
    st.dataframe(
        watch_df.style.format({"Last": "${:,.4f}", "24h %": "{:+.2f}%"}),
        use_container_width=True, height=240
    )

    st.divider()
    auto_refresh = st.checkbox("Enable Auto-Refresh (10s)", value=False)
    if auto_refresh:
        st.experimental_set_query_params(_=str(time.time()))  # force script hash change
        time.sleep(10)
        st.experimental_rerun()

# ----------------------------
# Main Layout
# ----------------------------
left, right = st.columns([0.68, 0.32])

# LEFT: Chart + Trade Box
with left:
    st.markdown("#### 📊 Market")
    col1, col2, col3, col4, col5 = st.columns([0.22, 0.22, 0.18, 0.18, 0.20])
    with col1:
        symbol = st.selectbox("Symbol", SYMBOLS, index=0)
    with col2:
        tf = st.selectbox("Timeframe", ["15m", "1h", "2h", "4h", "1d"], index=1)
    with col3:
        ma1 = st.number_input("MA Fast", min_value=5, max_value=100, value=20)
    with col4:
        ma2 = st.number_input("MA Slow", min_value=5, max_value=200, value=50)
    with col5:
        st.write("")
        refresh_now = st.button("↻ Refresh")

    df = load_prices(symbol, period=period, interval=tf, source=source)
    last_price = float(df["Close"].iloc[-1])
    prev_price = float(df["Close"].iloc[-2]) if len(df) > 1 else last_price
    day_change = (last_price - prev_price) / prev_price * 100 if prev_price else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"{symbol} Price", format_usd(last_price))
    m2.metric("Change", f"{day_change:+.2f}%")
    m3.metric("24h High", format_usd(df['High'][-24:].max() if len(df) >= 24 else df['High'].max()))
    m4.metric("24h Low", format_usd(df['Low'][-24:].min() if len(df) >= 24 else df['Low'].min()))

    chart = make_candlestick(df, ma1=ma1, ma2=ma2, title=f"{symbol} • {source}")
    st.plotly_chart(chart, use_container_width=True, theme="streamlit")

    # Trade Box
    st.markdown("#### 💱 Trade")
    tb1, tb2 = st.columns(2)
    with tb1:
        st.markdown('<div class="block buy">', unsafe_allow_html=True)
        st.subheader("Buy")
        buy_type = st.radio("Order Type", ["Market", "Limit"], key="buy_type")
        buy_size = st.number_input("Size (units)", min_value=0.0, value=0.01, step=0.001, key="buy_size")
        buy_limit = None
        if buy_type == "Limit":
            buy_limit = st.number_input("Limit Price (USD)", min_value=0.0, value=round(last_price * 0.995, 2), step=0.01, key="buy_limit")
            est = est_quote(buy_size, buy_limit)
        else:
            est = est_quote(buy_size, last_price)
        st.caption(f"Est. Cost: **{format_usd(est)}**")
        if st.button("Place Buy Order"):
            order = {
                "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "side": "BUY", "symbol": symbol, "type": buy_type,
                "price": float(buy_limit if buy_limit else last_price),
                "size": float(buy_size), "value": float(est)
            }
            st.session_state.open_orders.append(order)
            st.success("Buy order placed (demo).")
        st.markdown('</div>', unsafe_allow_html=True)

    with tb2:
        st.markdown('<div class="block sell">', unsafe_allow_html=True)
        st.subheader("Sell")
        sell_type = st.radio("Order Type ", ["Market", "Limit"], key="sell_type")
        sell_size = st.number_input("Size (units) ", min_value=0.0, value=0.01, step=0.001, key="sell_size")
        sell_limit = None
        if sell_type == "Limit":
            sell_limit = st.number_input("Limit Price (USD) ", min_value=0.0, value=round(last_price * 1.005, 2), step=0.01, key="sell_limit")
            estv = est_quote(sell_size, sell_limit)
        else:
            estv = est_quote(sell_size, last_price)
        st.caption(f"Est. Proceeds: **{format_usd(estv)}**")
        if st.button("Place Sell Order"):
            order = {
                "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "side": "SELL", "symbol": symbol, "type": sell_type,
                "price": float(sell_limit if sell_limit else last_price),
                "size": float(sell_size), "value": float(estv)
            }
            st.session_state.open_orders.append(order)
            st.success("Sell order placed (demo).")
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT: Order Book, Trades, Depth
with right:
    st.markdown("#### 📚 Order Book & Trades")
    mid = last_price
    asks_df, bids_df = make_orderbook_tables(mid_price=mid, n=12, tick=round(max(0.01, mid * 0.0005), 2))

    ob1, ob2 = st.columns(2)
    with ob1:
        st.caption("Asks")
        st.dataframe(
            asks_df.style.format({"Price": "${:,.2f}"}), height=240, use_container_width=True
        )
    with ob2:
        st.caption("Bids")
        st.dataframe(
            bids_df.style.format({"Price": "${:,.2f}"}), height=240, use_container_width=True
        )

    # Recent Trades (simulated)
    rng = np.random.default_rng(123)
    trades = []
    for i in range(16):
        tside = "BUY" if i % 2 == 0 else "SELL"
        tprice = round(mid + rng.normal(0, max(0.02, mid*0.0003)), 2)
        tsize = round(max(0.001, rng.lognormal(mean=0, sigma=0.6)), 4)
        ttime = (datetime.utcnow() - timedelta(seconds=i*23)).strftime("%H:%M:%S")
        trades.append({"Time (UTC)": ttime, "Side": tside, "Price": tprice, "Size": tsize})
    trades_df = pd.DataFrame(trades)

    st.markdown("##### Recent Trades")
    st.dataframe(trades_df, use_container_width=True, height=220)

    # Depth chart
    st.plotly_chart(make_depth_chart(mid=round(mid, 2), spread=max(0.05, mid*0.0005), levels=40), use_container_width=True, theme="streamlit")

# ----------------------------
# Bottom: Portfolio & Orders
# ----------------------------
st.markdown("#### 🧩 Portfolio & Orders")
bot1, bot2, bot3 = st.columns([0.33, 0.33, 0.34])

with bot1:
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("Portfolio Allocation")
    # Estimate current USD value for each position
    alloc_rows = []
    total_val = st.session_state.portfolio["cash_usd"]
    for s, qty in st.session_state.portfolio["positions"].items():
        dfv = load_prices(s, period=period, interval=interval, source=source)
        px_last = float(dfv["Close"].iloc[-1])
        val = qty * px_last
        alloc_rows.append({"Asset": s, "Value": val})
        total_val += val
    alloc_rows.append({"Asset": "CASH", "Value": st.session_state.portfolio["cash_usd"]})
    alloc_df = pd.DataFrame(alloc_rows)
    pie = px.pie(alloc_df, names="Asset", values="Value", title=None, hole=0.4, template="plotly_dark")
    st.plotly_chart(pie, use_container_width=True, theme="streamlit")
    st.caption(f"Est. Portfolio Value: **{format_usd(total_val)}**")
    st.markdown('</div>', unsafe_allow_html=True)

with bot2:
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("Open Orders")
    if st.session_state.open_orders:
        odf = pd.DataFrame(st.session_state.open_orders)
        st.dataframe(odf, use_container_width=True, height=240)
        cA, cB = st.columns(2)
        with cA:
            if st.button("Cancel All"):
                st.session_state.open_orders.clear()
                st.info("All open orders canceled (demo).")
        with cB:
            if st.button("Mark All as Filled"):
                st.session_state.order_history.extend(st.session_state.open_orders)
                st.session_state.open_orders.clear()
                st.success("Orders moved to history.")
    else:
        st.info("No open orders.")
    st.markdown('</div>', unsafe_allow_html=True)

with bot3:
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("Order History")
    if st.session_state.order_history:
        hdf = pd.DataFrame(st.session_state.order_history)
        st.dataframe(hdf, use_container_width=True, height=240)
    else:
        st.info("No past orders yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Footer chips
# ----------------------------
st.write("")
fc1, fc2, fc3, fc4 = st.columns(4)
fc1.markdown('<span class="metric-chip">⚙️ API: simulated</span>', unsafe_allow_html=True)
fc2.markdown(f'<span class="metric-chip">🕒 Server time: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC</span>', unsafe_allow_html=True)
fc3.markdown(f'<span class="metric-chip">📊 Source: {source}</span>', unsafe_allow_html=True)
fc4.markdown('<span class="metric-chip">🔐 Auth: demo</span>', unsafe_allow_html=True)
