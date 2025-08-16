import streamlit as st

# ----------------------
# Fake user database (for demo only!)
# ----------------------
USER_CREDENTIALS = {
    "satoshi": "bitcoin123",
    "vitalik": "ethereum2025",
    "admin": "cryptoMaster"
}

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="Crypto Exchange Login", page_icon="🪙", layout="centered")

# Background styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #111;
        color: white;
        border: 1px solid #00ffcc;
        border-radius: 10px;
    }
    .stPasswordInput > div > div > input {
        background-color: #111;
        color: white;
        border: 1px solid #00ffcc;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Title
# ----------------------
st.markdown(
    "<h1 style='text-align: center; color: #00ffcc;'>🚀 Crypto Exchange Login</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>Secure access to your digital assets</p>",
    unsafe_allow_html=True
)

# ----------------------
# Login Form
# ----------------------
with st.form("login_form"):
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success(f"✅ Welcome back, {username}! 🚀")
            st.balloons()
        else:
            st.error("❌ Invalid Username or Password")

# ----------------------
# Extra Options
# ----------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<p style='text-align:left;'><a href='#' style='color:#00ffcc; text-decoration:none;'>🔒 Forgot Password?</a></p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<p style='text-align:right;'>New here? <a href='#' style='color:#ffcc00; text-decoration:none;'>📝 Sign Up</a></p>",
        unsafe_allow_html=True
    )
