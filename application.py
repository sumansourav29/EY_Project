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

# ----------------------
# Background Styling
# ----------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stTextInput > div > div > input, .stPasswordInput > div > div > input {
        background-color: #111;
        color: white;
        border: 1px solid #00ffcc;
        border-radius: 10px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00ffcc, #0066ff);
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 8px 0px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Page Routing (Session State)
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"


# ----------------------
# LOGIN PAGE
# ----------------------
def login_page():
    st.markdown(
        "<h1 style='text-align: center; color: #00ffcc;'>🚀 Crypto Exchange Login</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:gray;'>Secure access to your digital assets</p>",
        unsafe_allow_html=True
    )

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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 Forgot Password?"):
            st.session_state.page = "forgot"

    with col2:
        if st.button("📝 Sign Up"):
            st.session_state.page = "signup"


# ----------------------
# SIGNUP PAGE
# ----------------------
def signup_page():
    st.markdown(
        "<h1 style='text-align: center; color: #ffcc00;'>📝 Sign Up</h1>",
        unsafe_allow_html=True
    )
    with st.form("signup_form"):
        new_user = st.text_input("👤 Choose Username")
        new_pass = st.text_input("🔑 Choose Password", type="password")
        confirm_pass = st.text_input("🔑 Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account")

        if submitted:
            if new_user in USER_CREDENTIALS:
                st.error("⚠️ Username already exists!")
            elif new_pass != confirm_pass:
                st.error("⚠️ Passwords do not match!")
            else:
                USER_CREDENTIALS[new_user] = new_pass
                st.success("✅ Account created successfully! Please login.")
                st.session_state.page = "login"

    if st.button("⬅️ Back to Login"):
        st.session_state.page = "login"


# ----------------------
# FORGOT PASSWORD PAGE
# ----------------------
def forgot_page():
    st.markdown(
        "<h1 style='text-align: center; color: #00ffcc;'>🔑 Reset Password</h1>",
        unsafe_allow_html=True
    )
    with st.form("forgot_form"):
        email_or_user = st.text_input("📧 Enter your Email or Username")
        submitted = st.form_submit_button("Send Reset Link")

        if submitted:
            if email_or_user in USER_CREDENTIALS:
                st.success("📩 Reset link sent to your registered email!")
            else:
                st.info("ℹ️ If this account exists, a reset link has been sent.")

    if st.button("⬅️ Back to Login"):
        st.session_state.page = "login"


# ----------------------
# ROUTER
# ----------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "forgot":
    forgot_page()
