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

if "page" not in st.session_state:
    st.session_state.page = "login"

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

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username]["password"] == password:
                st.session_state.current_user = username
                if username == "admin":  # Special case for admin
                    send_otp(st.session_state.users[username]["email"])
                    st.session_state.page = "otp_page"   # 👈 go to OTP PAGE
                else:
                    st.success(f"✅ Welcome {username}!")
                    st.session_state.page = "home"
            else:
                st.error("❌ Invalid username or password")

    with col2:
        if st.button("Forgot Password?"):
            st.session_state.page = "forgot_password"

    with col3:
        if st.button("Sign Up"):
            st.session_state.page = "signup"


# ----------------------
# OTP VERIFICATION PAGE
# ----------------------
def otp_page():
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
            st.session_state.page = "home"
        else:
            st.error("❌ Invalid OTP")

    if st.button("Resend OTP"):
        send_otp(st.session_state.users["admin"]["email"])
        st.success("🔄 New OTP sent!")


# ----------------------
# FORGOT PASSWORD PAGE
# ----------------------
def forgot_password_page():
    st.title("🔑 Forgot Password")

    username = st.text_input("Enter your username")

    if st.button("Send Reset Link"):
        if username in st.session_state.users:
            st.success(f"📧 Reset link sent to {st.session_state.users[username]['email']}")
        else:
            st.error("❌ Username not found")

    if st.button("⬅ Back to Login"):
        st.session_state.page = "login"


# ----------------------
# SIGN UP PAGE
# ----------------------
def signup_page():
    st.title("📝 Sign Up")

    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    new_email = st.text_input("Enter your email")

    if st.button("Create Account"):
        if new_username in st.session_state.users:
            st.error("⚠ Username already exists")
        elif new_username and new_password and new_email:
            st.session_state.users[new_username] = {"password": new_password, "email": new_email}
            st.success("✅ Account created! You can now login.")
            st.session_state.page = "login"
        else:
            st.error("❌ Please fill all fields")

    if st.button("⬅ Back to Login"):
        st.session_state.page = "login"


# ----------------------
# HOME PAGE
# ----------------------
def home_page():
    st.success(f"🎉 Logged in as {st.session_state.current_user}")
    if st.button("Logout"):
        st.session_state.page = "login"
        st.session_state.current_user = None


# ----------------------
# ROUTER
# ----------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "otp_page":
    otp_page()
elif st.session_state.page == "forgot_password":
    forgot_password_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "home":
    home_page()
