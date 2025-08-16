import streamlit as st
import random

# ----------------------
# Store users in session (for demo)
# ----------------------
if "users" not in st.session_state:
    st.session_state.users = {}   # {username: {"password": ..., "email": ...}}

if "stage" not in st.session_state:
    st.session_state.stage = "login"

if "otp" not in st.session_state:
    st.session_state.otp = None

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ----------------------
# Helper: Send OTP (simulated)
# ----------------------
def send_otp(email):
    otp = str(random.randint(100000, 999999))
    st.session_state.otp = otp
    st.info(f"(Demo) OTP sent to {email}: **{otp}**")
    return otp


# ----------------------
# LOGIN PAGE
# ----------------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.current_user = username
            send_otp(st.session_state.users[username]["email"])
            st.session_state.stage = "otp"
        else:
            st.error("❌ Invalid username or password")

    if st.button("📝 Sign Up"):
        st.session_state.stage = "signup"

    if st.button("🔑 Forgot Password"):
        st.session_state.stage = "forgot"


# ----------------------
# SIGNUP PAGE
# ----------------------
def signup_page():
    st.title("📝 Sign Up")

    new_user = st.text_input("Choose Username")
    new_email = st.text_input("Email")
    new_pass = st.text_input("Password", type="password")

    if st.button("Register"):
        if new_user in st.session_state.users:
            st.error("❌ Username already exists")
        elif new_user.strip() == "" or new_pass.strip() == "" or new_email.strip() == "":
            st.error("⚠ Please fill all fields")
        else:
            st.session_state.users[new_user] = {"password": new_pass, "email": new_email}
            st.success("✅ Account created! Please login.")
            st.session_state.stage = "login"

    if st.button("⬅ Back to Login"):
        st.session_state.stage = "login"


# ----------------------
# OTP VERIFICATION PAGE
# ----------------------
def otp_page():
    st.title("🔑 OTP Verification")

    otp_input = st.text_input("Enter OTP sent to your email")

    if st.button("Verify OTP"):
        if otp_input == st.session_state.otp:
            st.success(f"✅ Welcome {st.session_state.current_user}!")
            st.session_state.stage = "home"
        else:
            st.error("❌ Invalid OTP")


# ----------------------
# FORGOT PASSWORD PAGE
# ----------------------
def forgot_password_page():
    st.title("🔑 Forgot Password")
    email = st.text_input("Enter your registered email")

    if st.button("Send Reset Link"):
        for user, data in st.session_state.users.items():
            if data["email"] == email:
                st.success("✅ Reset link sent to your email (demo only).")
                st.session_state.stage = "login"
                return
        st.error("❌ Email not found")

    if st.button("⬅ Back to Login"):
        st.session_state.stage = "login"


# ----------------------
# HOME PAGE
# ----------------------
def home_page():
    st.success(f"🎉 Logged in as {st.session_state.current_user}")
    if st.button("Logout"):
        st.session_state.stage = "login"
        st.session_state.current_user = None


# ----------------------
# ROUTER
# ----------------------
if st.session_state.stage == "login":
    login_page()
elif st.session_state.stage == "signup":
    signup_page()
elif st.session_state.stage == "otp":
    otp_page()
elif st.session_state.stage == "forgot":
    forgot_password_page()
elif st.session_state.stage == "home":
    home_page()
