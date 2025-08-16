import streamlit as st

# Page config
st.set_page_config(page_title="Crypto Exchange", page_icon="🪙", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f0f0f, #1a1a1a, #141e30);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        max-width: 400px;
        margin: auto;
    }
    .login-title {
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        color: #00ffcc;
        margin-bottom: 20px;
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        border: none;
        border-radius: 12px;
        color: white;
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        outline: none;
        border: 2px solid #00ffcc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #00ffcc, #0077ff);
        color: black;
        font-weight: 600;
        padding: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0077ff, #00ffcc);
        color: white;
    }
    .link {
        text-align: center;
        margin-top: 15px;
        font-size: 14px;
    }
    .link a {
        color: #ffcc00;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "login"

def go_to(page):
    st.session_state.page = page

# --- Login Page ---
def show_login():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Login</div>', unsafe_allow_html=True)

    username = st.text_input("Username", key="login_user", placeholder="Enter username", label_visibility="collapsed")
    password = st.text_input("Password", key="login_pass", placeholder="Enter password", type="password", label_visibility="collapsed")

    if st.button("Login"):
        if username == "satoshi" and password == "bitcoin123":
            st.success("✅ Welcome back, Satoshi!")
        else:
            st.error("❌ Invalid credentials")

    st.markdown('<div class="link"><a href="#" onclick="window.location.reload()">Forgot Password?</a></div>', unsafe_allow_html=True)
    if st.button("Forgot Password?"):
        go_to("forgot")

    st.markdown('<div class="link">New here?</div>', unsafe_allow_html=True)
    if st.button("Sign Up"):
        go_to("signup")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Forgot Password Page ---
def show_forgot():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔑 Reset Password</div>', unsafe_allow_html=True)

    st.write("Choose a method to reset your password:")
    if st.button("📧 Reset via Email"):
        st.info("A reset link has been sent to your email.")
    if st.button("📱 Reset via SMS"):
        st.info("A reset code has been sent to your phone.")
    if st.button("🌐 Sign in with Google"):
        st.success("Redirecting to Google login...")
    if st.button("🔗 Sign in with MetaMask"):
        st.success("Connecting to your crypto wallet...")

    if st.button("⬅ Back to Login"):
        go_to("login")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Signup Page ---
def show_signup():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">📝 Sign Up</div>', unsafe_allow_html=True)

    new_user = st.text_input("New Username", key="signup_user", placeholder="Choose a username", label_visibility="collapsed")
    new_pass = st.text_input("New Password", key="signup_pass", placeholder="Choose a password", type="password", label_visibility="collapsed")
    email = st.text_input("Email", key="signup_email", placeholder="Enter your email", label_visibility="collapsed")

    if st.button("Create Account"):
        if new_user and new_pass and email:
            st.success(f"✅ Account created for {new_user}! Please login.")
            go_to("login")
        else:
            st.error("⚠ Please fill all fields.")

    if st.button("⬅ Back to Login"):
        go_to("login")

    st.markdown('</div>', unsafe_allow_html=True)

# --- Router ---
if st.session_state.page == "login":
    show_login()
elif st.session_state.page == "forgot":
    show_forgot()
elif st.session_state.page == "signup":
    show_signup()
