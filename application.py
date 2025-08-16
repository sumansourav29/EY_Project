import streamlit as st

# ----------------------
# Fake user database (in memory only for demo)
# ----------------------
if "USER_CREDENTIALS" not in st.session_state:
    st.session_state.USER_CREDENTIALS = {
        "satoshi": "bitcoin123",
        "vitalik": "ethereum2025",
        "admin": "cryptoMaster"
    }

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="Crypto Exchange", page_icon="🪙", layout="centered")

# ----------------------
# Navigation state
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ----------------------
# LOGIN PAGE
# ----------------------
if st.session_state.page == "login":
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 Crypto Exchange Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Secure access to your digital assets</p>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in st.session_state.USER_CREDENTIALS and st.session_state.USER_CREDENTIALS[username] == password:
                st.success(f"✅ Welcome back, {username}! 🚀")
                st.balloons()
            else:
                st.error("❌ Invalid Username or Password")

    # Links
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔒 Forgot Password?"):
            st.session_state.page = "forgot"
            st.rerun()

    with col2:
        if st.button("📝 Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

# ----------------------
# FORGOT PASSWORD PAGE
# ----------------------
elif st.session_state.page == "forgot":
    st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🔒 Recover Your Account</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Choose a method to reset your password</p>", unsafe_allow_html=True)

    option = st.radio(
        "Select recovery option:",
        ["📧 Reset via Email", "📱 Reset via Mobile OTP", "🔐 Google Authenticator", "❓ Security Questions"]
    )

    if option == "📧 Reset via Email":
        email = st.text_input("Enter your registered email:")
        if st.button("Send Reset Link"):
            st.success(f"📨 Password reset link sent to {email}")

    elif option == "📱 Reset via Mobile OTP":
        phone = st.text_input("Enter your mobile number:")
        if st.button("Send OTP"):
            st.success(f"📲 OTP sent to {phone}")

    elif option == "🔐 Google Authenticator":
        code = st.text_input("Enter 6-digit Authenticator Code:")
        if st.button("Verify"):
            st.success("✅ Authenticator verified! You can reset your password now.")

    elif option == "❓ Security Questions":
        q1 = st.text_input("What is the name of your first pet?")
        q2 = st.text_input("What city were you born in?")
        if st.button("Submit Answers"):
            st.success("✅ Security questions verified! You can reset your password.")

    if st.button("⬅ Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ----------------------
# SIGN UP PAGE
# ----------------------
elif st.session_state.page == "signup":
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>📝 Create New Account</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Join the crypto revolution today 🚀</p>", unsafe_allow_html=True)

    with st.form("signup_form"):
        new_user = st.text_input("👤 Choose a Username")
        new_pass = st.text_input("🔑 Choose a Password", type="password")
        confirm_pass = st.text_input("🔑 Confirm Password", type="password")
        email = st.text_input("📧 Email Address")

        submitted = st.form_submit_button("Create Account")

        if submitted:
            if new_user in st.session_state.USER_CREDENTIALS:
                st.error("⚠️ Username already exists. Please choose another.")
            elif new_pass != confirm_pass:
                st.error("❌ Passwords do not match.")
            elif new_user == "" or new_pass == "" or email == "":
                st.error("⚠️ All fields are required.")
            else:
                st.session_state.USER_CREDENTIALS[new_user] = new_pass
                st.success(f"✅ Account created successfully for {new_user}!")
                st.session_state.page = "login"
                st.rerun()

    if st.button("⬅ Back to Login"):
        st.session_state.page = "login"
        st.rerun()
