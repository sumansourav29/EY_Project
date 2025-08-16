import streamlit as st

st.set_page_config(page_title="Crypto Exchange", layout="wide")

# ----------- Session State for Navigation -----------
if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

def change_page(page):
    st.session_state["page"] = page

# ----------- Custom CSS for Header -----------
header_css = """
<style>
/* Navbar container */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 60px;
    background: #0b1020;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 30px;
    color: white;
    font-family: "Segoe UI", sans-serif;
    z-index: 10000;
    border-bottom: 1px solid #222;
}

/* Logo */
.logo {
    font-size: 20px;
    font-weight: bold;
    color: #4ade80;
}

/* Nav items */
.nav-links {
    display: flex;
    gap: 25px;
    align-items: center;
}
.nav-item {
    cursor: pointer;
    font-size: 15px;
}
.nav-item:hover {
    color: #4ade80;
}

/* Profile circle */
.profile {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background: linear-gradient(135deg,#1f2b66,#2f7f5f);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    cursor: pointer;
    position: relative;
}

/* Dropdown */
.dropdown {
    display: none;
    position: absolute;
    top: 45px;
    right: 0;
    background: #1a1f36;
    border: 1px solid #333;
    border-radius: 8px;
    min-width: 120px;
    z-index: 9999;
}
.dropdown a {
    display: block;
    padding: 8px 12px;
    color: white;
    text-decoration: none;
    font-size: 14px;
}
.dropdown a:hover {
    background: #2d3748;
}

/* Show dropdown on hover */
.profile:hover .dropdown {
    display: block;
}
</style>
"""

# ----------- Header HTML -----------
header_html = f"""
<div class="navbar">
    <div class="logo">💹 Crypto</div>
    <div class="nav-links">
        <span class="nav-item" onclick="window.parent.postMessage({{type: 'nav', page: 'Dashboard'}}, '*')">Dashboard</span>
        <span class="nav-item" onclick="window.parent.postMessage({{type: 'nav', page: 'Charts'}}, '*')">Charts</span>
        <span class="nav-item" onclick="window.parent.postMessage({{type: 'nav', page: 'Wallet'}}, '*')">Wallet</span>
        <span class="nav-item" onclick="window.parent.postMessage({{type: 'nav', page: 'News'}}, '*')">News</span>
        <div class="profile">SS
            <div class="dropdown">
                <a href="#" onclick="window.parent.postMessage({{type: 'nav', page: 'Settings'}}, '*')">⚙️ Settings</a>
                <a href="#">🚪 Logout</a>
            </div>
        </div>
    </div>
</div>
<br><br><br>
"""

st.markdown(header_css + header_html, unsafe_allow_html=True)

# ----------- Handle Navigation Events from JS -----------

nav_event = st.query_params.get("nav", None)

# Sync JS click with session_state
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    if (event.data.type === "nav") {
        const page = event.data.page;
        const url = new URL(window.location);
        url.searchParams.set("nav", page);
        window.history.pushState({}, "", url);
        window.parent.postMessage({type: "streamlit:setComponentValue", key: "nav", value: page}, "*");
        window.location.reload();
    }
});
</script>
""", unsafe_allow_html=True)

if nav_event:
    st.session_state["page"] = nav_event

# ----------- Main Content -----------
page = st.session_state["page"]

if page == "Dashboard":
    st.subheader("📊 Dashboard Overview")
    st.write("This is the dashboard section.")

elif page == "Charts":
    st.subheader("📈 Charts Section")
    st.line_chart({"BTC": [45000, 46000, 45500, 47000, 46500]})

elif page == "Wallet":
    st.subheader("👛 Wallet Section")
    st.write("Wallet balances here.")

elif page == "News":
    st.subheader("📰 News Section")
    st.write("Latest crypto news.")

elif page == "Settings":
    st.subheader("⚙️ Settings Section")
    st.write("Change profile, preferences, etc.")
