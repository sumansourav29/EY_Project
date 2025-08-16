import streamlit as st
import random
import string

# ----------------------
# Fake Database
# ----------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "12345", "email": "sumanuser@gmail.com"}
    }

if "stage" not in st.session_state:
    st.session_state.stage = "login"

if "otp" not in st.session_state:
    st.session_state.otp = None

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ----------------------
# Helper: Generate OTP
# ----------------------
def generate_otp(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_otp(email):
    otp = generate_otp()
    st.session_state.otp = otp
    # In real case send email. For demo:
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
            if username == "admin":  # Special case for admin
                send_otp(st.session_state.users[username]["email"])
                st.session_state.stage = "admin_otp"
            else:
                st.success(f"✅ Welcome {username}!")
                st.session_state.stage = "home"
        else:
            st.error("❌ Invalid username or password")


# ----------------------
# ADMIN OTP PAGE
# ----------------------
def admin_otp_page():
    st.title("📧 Email Verification")

    masked_email = "su.....@gmail.com"
    st.write(f"OTP has been sent to **{masked_email}**")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1: d1 = st.text_input("", max_chars=1)
    with col2: d2 = st.text_input("", max_chars=1)
    with col3: d3 = st.text_input("", max_chars=1)
    with col4: d4 = st.text_input("", max_chars=1)
    with col5: d5 = st.text_input("", max_chars=1)
    with col6: d6 = st.text_input("", max_chars=1)

    entered_otp = "".join([d1, d2, d3, d4, d5, d6])

    if st.button("Verify OTP"):
        if entered_otp == st.session_state.otp:
            st.success("✅ Email verified! Welcome Admin 🚀")
            st.session_state.stage = "home"
        else:
            st.error("❌ Invalid OTP")

    if st.button("Resend OTP"):
        send_otp(st.session_state.users["admin"]["email"])
        st.success("🔄 New OTP sent!")


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
elif st.session_state.stage == "admin_otp":
    admin_otp_page()
elif st.session_state.stage == "home":
    home_page()
