import streamlit as st
import random
import smtplib

# ----------------------
# Fake user database (for demo only!)
# ----------------------
USER_CREDENTIALS = {
    "satoshi": {"password": "bitcoin123", "email": "satoshi@email.com"},
    "vitalik": {"password": "ethereum2025", "email": "vitalik@email.com"},
    "admin": {"password": "cryptoMaster", "email": "admin@email.com"},
}

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="Crypto Exchange Login", page_icon="🪙", layout="centered")

# ----------------------
# Session State for OTP
# ----------------------
if "stage" not in st.session_state:
    st.session_state.stage = "login"   # login → otp → home
if "otp" not in st.session_state:
    st.session_state.otp = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ----------------------
# Helper: Send OTP (simulated)
# ----------------------
def send_otp(email):
    otp = random.randint(100000, 999999)
    st.session_state.otp = str(otp)
    # In real case, send via SMTP/email API
    st.info(f"(Demo) OTP sent to {email}: **{otp}**")
    return otp

# ----------------------
# LOGIN PAGE
# ----------------------
def login_page():
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🚀 Crypto Exchange Login</h1>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
                st.session_state.current_user = username
                send_otp(USER_CREDENTIALS[username]["email"])
                st.session_state.stage = "otp"
            else:
                st.error("❌ Invalid Username or Password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔒 Forgot Password?"):
            st.session_state.stage = "forgot"
    with col2:
        if st.button("📝 Sign Up"):
            st.session_state.stage = "signup"

# ----------------------
# OTP VERIFICATION PAGE
# ----------------------
def otp_page():
    st.markdown("<h2 style='text-align:center; color:#ffaa00;'>🔑 2-Step Verification</h2>", unsafe_allow_html=True)
    otp_input = st.text_input("Enter OTP sent to your email")
    if st.button("Verify OTP"):
        if otp_input == st.session_state.otp:
            st.success(f"✅ Login Successful! Welcome {st.session_state.current_user} 🚀")
            st.balloons()
            st.session_state.stage = "home"
        else:
            st.error("❌ Invalid OTP")

# ----------------------
# FORGOT PASSWORD PAGE
# ----------------------
def forgot_password_page():
    st.markdown("<h2 style='text-align:center; color:#ff4444;'>Forgot Password</h2>", unsafe_allow_html=True)
    email = st.text_input("Enter your registered email")
    if st.button("Send Reset Link"):
        st.success("✅ Password reset link has been sent to your email (simulated).")
        st.session_state.stage = "login"
    if st.button("⬅ Back to Login"):
        st.session_state.stage = "login"

# ----------------------
# SIGN UP PAGE
# ----------------------
def signup_page():
    st.markdown("<h2 style='text-align:center; color:#44ff44;'>Create Account</h2>", unsafe_allow_html=True)
    new_user = st.text_input("👤 Choose Username")
    new_email = st.text_input("📧 Email")
    new_pass = st.text_input("🔑 Password", type="password")
    if st.button("Register"):
        if new_user in USER_CREDENTIALS:
            st.error("❌ Username already exists!")
        else:
            USER_CREDENTIALS[new_user] = {"password": new_pass, "email": new_email}
            st.success("✅ Account created! Please login.")
            st.session_state.stage = "login"
    if st.button("⬅ Back to Login"):
        st.session_state.stage = "login"

# ----------------------
# HOME PAGE
# ----------------------
def home_page():
    st.success(f"🎉 Welcome {st.session_state.current_user} to Crypto Exchange Dashboard!")
    if st.button("Logout"):
        st.session_state.stage = "login"
        st.session_state.current_user = None

# ----------------------
# ROUTER
# ----------------------
if st.session_state.stage == "login":
    login_page()
elif st.session_state.stage == "otp":
    otp_page()
elif st.session_state.stage == "forgot":
    forgot_password_page()
elif st.session_state.stage == "signup":
    signup_page()
elif st.session_state.stage == "home":
    home_page()
