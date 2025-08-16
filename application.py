import streamlit as st
import random
import string

# Generate random alphanumeric OTP
def generate_otp(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# ----------------------
# Login Page
# ----------------------
def login_page():
    st.title("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.page = "otp"
            st.session_state.otp = generate_otp()
        else:
            st.error("❌ Invalid Username or Password")

    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign Up"):
            st.session_state.page = "signup"

    with col2:
        if st.button("Forgot Password"):
            st.session_state.page = "forgot"


# ----------------------
# OTP Page
# ----------------------
def otp_page():
    st.title("🔐 Email Verification")
    st.write("OTP has been sent to **su.....@gmail.com**")

    # CSS for square OTP boxes
    st.markdown(
        """
        <style>
        .otp-input input {
            text-align: center;
            font-size: 20px !important;
            font-weight: bold;
            width: 45px !important;
            height: 45px !important;
            border: 2px solid #00ccaa;
            border-radius: 8px;
            margin: 3px;
        }
        .link-container {
            text-align:center;
            margin-top: 10px;
        }
        .link-container a {
            text-decoration:none;
            font-weight:bold;
            font-size: 14px;
        }
        .resend {
            color:#00ccaa;
        }
        .back {
            color:#ff4b4b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # OTP input fields (6 boxes)
    cols = st.columns(6)
    otp_digits = []
    for i, col in enumerate(cols):
        with col:
            digit = st.text_input("", max_chars=1, key=f"otp{i}", label_visibility="collapsed")
            otp_digits.append(digit)

    otp_entered = "".join(otp_digits)

    if st.button("Verify OTP"):
        if otp_entered == st.session_state.get("otp", ""):
            st.success("✅ OTP Verified! Welcome to Crypto Exchange 🚀")
            st.balloons()
        else:
            st.error("❌ Invalid OTP. Please try again.")

    # Hyperlinks for actions
    st.markdown(
        """
        <div class="link-container">
            <a href="?resend=true" class="resend">🔄 Resend OTP</a> &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href="?back=true" class="back">⬅️ Back to Login</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Handle link clicks using new query_params API
    query_params = st.query_params  # ✅ new method
    if "resend" in query_params:
        st.session_state.otp = generate_otp()
        st.info(f"📩 New OTP has been sent! (For testing: {st.session_state.otp})")
        st.query_params.clear()  # clear params
    if "back" in query_params:
        st.session_state.page = "login"
        st.query_params.clear()  # clear params



# ----------------------
# Signup Page
# ----------------------
def signup_page():
    st.title("📝 Sign Up")

    new_user = st.text_input("Choose Username")
    new_email = st.text_input("Enter Email")
    new_pass = st.text_input("Choose Password", type="password")

    if st.button("Create Account"):
        st.success("✅ Account created successfully! Please login.")
        st.session_state.page = "login"

    if st.button("Back to Login"):
        st.session_state.page = "login"


# ----------------------
# Forgot Password Page
# ----------------------
def forgot_password_page():
    st.title("🔒 Forgot Password")

    email = st.text_input("Enter your registered email")

    if st.button("Reset Password"):
        st.info("📩 Password reset link sent to your email!")
        st.session_state.page = "login"

    if st.button("Back to Login"):
        st.session_state.page = "login"


# ----------------------
# Main Navigation
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "otp":
    otp_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "forgot":
    forgot_password_page()

