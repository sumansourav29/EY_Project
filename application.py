import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Crypto Exchange Login", layout="centered")

# ---- CSS STYLING ----
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
            color: white;
        }
        .box {
            background-color: #0f1a2b;
            padding: 30px;
            border-radius: 15px;
            max-width: 400px;
            margin: auto;
            box-shadow: 0 0 15px rgba(0,0,0,0.6);
        }
        .stButton button {
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            color: white;
            border-radius: 25px;
            height: 45px;
            width: 100%;
            border: none;
            font-size: 16px;
        }
        .link {
            color: #00c6ff;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)


# ---- SESSION STATE ----
if "page" not in st.session_state:
    st.session_state.page = "login"


# ---- LOGIN PAGE ----
def login_page():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🔐 Login to Crypto Exchange")

    st.text_input("Username", key="login_user", placeholder="Enter username")
    st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")

    if st.button("Login"):
        st.success("✅ Logged in successfully!")

    if st.button("Forgot Password?"):
        st.session_state.page = "forgot"

    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.page = "signup"

    st.markdown("</div>", unsafe_allow_html=True)


# ---- SIGNUP PAGE ----
def signup_page():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📝 Create New Account")

    st.text_input("Full Name")
    st.text_input("Email Address")
    st.text_input("Password", type="password")
    st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        st.success("✅ Account created! Please login.")
        st.session_state.page = "login"

    if st.button("Back to Login"):
        st.session_state.page = "login"

    st.markdown("</div>", unsafe_allow_html=True)


# ---- FORGOT PASSWORD PAGE ----
def forgot_page():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🔑 Recover Password")

    st.write("Choose a method to reset your password:")
    if st.button("Reset via Email"):
        st.info("📧 Password reset link sent to your email!")
    if st.button("Reset via SMS"):
        st.info("📱 SMS sent to your registered phone number!")
    if st.button("Sign in with Google"):
        st.success("✅ Signed in with Google!")

    if st.button("Back to Login"):
        st.session_state.page = "login"

    st.markdown("</div>", unsafe_allow_html=True)


# ---- ROUTING ----
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "forgot":
    forgot_page()
