import streamlit as st

# ----------------------
# Fake user database (for demo only!)
# ----------------------
USER_CREDENTIALS = {
    "satoshi": "bitcoin123",
    "vitalik": "ethereum2025",
    "admin": "12345"
}

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="Crypto Exchange Login", page_icon="🪙", layout="centered")

# ----------------------
# OTP Page
# ----------------------
def otp_page():
    st.title("🔐 Email Verification")
    st.write("OTP has been sent to **su.....@gmail.com**")

    # OTP input fields (6 boxes with unique keys)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1: d1 = st.text_input("", max_chars=1, key="otp1")
    with col2: d2 = st.text_input("", max_chars=1, key="otp2")
    with col3: d3 = st.text_input("", max_chars=1, key="otp3")
    with col4: d4 = st.text_input("", max_chars=1, key="otp4")
    with col5: d5 = st.text_input("", max_chars=1, key="otp5")
    with col6: d6 = st.text_input("", max_chars=1, key="otp6")

    otp_entered = "".join([d1, d2, d3, d4, d5, d6])

    if st.button("Verify OTP"):
        if otp_entered == "A1B2C3":  # Example OTP
            st.success("✅ OTP Verified! Welcome to Crypto Exchange 🚀")
            st.balloons()
        else:
            st.error("❌ Invalid OTP. Please try again.")

    st.button("🔄 Resend OTP")

    if st.button("⬅️ Back to Login"):
        st.session_state.page = "login"

# ----------------------
# Sign Up Page
# ----------------------
def signup_page():
    st.title("📝 Sign Up")

    new_user = st.text_input("👤 Choose a Username")
    new_pass = st.text_input("🔑 Choose a Password", type="password")

    if st.button("Create Account"):
        if new_user and new_pass:
            USER_CREDENTIALS[new_user] = new_pass
            st.success("✅ Account created successfully! Please login.")
            st.session_state.page = "login"
        else:
            st.error("❌ Please fill all fields")

    if st.button("⬅️ Back to Login"):
        st.session_state.page = "login"

# ----------------------
# Forgot Password Page
# ----------------------
def forgot_password_page():
    st.title("🔒 Forgot Password")
    email = st.text_input("📧 Enter your registered email")

    if st.button("Send Reset Link"):
        if email:
            st.success("✅ Password reset link has been sent to your email.")
        else:
            st.error("❌ Please enter a valid email")

    if st.button("⬅️ Back to Login"):
        st.session_state.page = "login"

# ----------------------
# Login Page
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
                if username == "admin" and password == "12345":
                    st.session_state.page = "otp"
                else:
                    st.success(f"✅ Welcome back, {username}! 🚀")
                    st.balloons()
            else:
                st.error("❌ Invalid Username or Password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 Forgot Password?"):
            st.session_state.page = "forgot_password"

    with col2:
        if st.button("📝 Sign Up"):
            st.session_state.page = "signup"

# ----------------------
# Page Router
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "forgot_password":
    forgot_password_page()
elif st.session_state.page == "otp":
    otp_page()
