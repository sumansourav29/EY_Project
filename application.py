import streamlit as st

# -- INITIALIZE --
if "USER_CREDENTIALS" not in st.session_state:
    st.session_state.USER_CREDENTIALS = {"satoshi": "bitcoin123"}

if "page" not in st.session_state:
    st.session_state.page = "login"

st.set_page_config(page_title="Crypto Exchange", page_icon="🪙", layout="centered")

# -- CSS STYLING --
st.markdown("""
<style>
    body {
        background: #020202;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .glass {
        background: rgba(20, 20, 30, 0.6);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.2);
        backdrop-filter: blur(8px);
        margin: auto;
    }

    .neon-input input {
        background: transparent;
        color: white;
        border: 2px solid #00ffcc;
        border-radius: 12px;
        padding: 10px;
        font-size: 1em;
    }

    .neon-input input:focus {
        box-shadow: 0 0 8px #00ffcc;
        outline: none;
    }

    .neon-btn>button {
        background: linear-gradient(90deg, #00ffcc, #599edb);
        border: none;
        color: black;
        font-size: 1em;
        padding: 0.6em 1.4em;
        border-radius: 12px;
        font-weight: bold;
        text-shadow: 0 0 4px rgba(0,0,0,0.5);
        transition: transform .2s, box-shadow .2s;
    }

    .neon-btn>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 12px #00ffcc;
    }

    h1 { color: #00ffcc; font-family: 'Orbitron', sans-serif; text-align: center; }
    p { text-align: center; color: #888; }
</style>
""", unsafe_allow_html=True)

# -- PAGES --
def show_login():
    st.markdown("<div class='glass'><h1>Crypto Login</h1><p>Secure access to your assets</p></div>", unsafe_allow_html=True)
    with st.form("login_form"):
        st.text_input("Username", key="login_user", placeholder="Enter username", label_visibility="collapsed", **{"class":"neon-input"})
        st.text_input("Password", type="password", key="login_pass", placeholder="Enter password", label_visibility="collapsed", **{"class":"neon-input"})
        if st.form_submit_button("Login", **{"class":"neon-btn"}):
            u, p = st.session_state.login_user, st.session_state.login_pass
            if u in st.session_state.USER_CREDENTIALS and st.session_state.USER_CREDENTIALS[u] == p:
                st.success(f"Welcome back, **{u}**! 🚀")
                st.balloons()
            else:
                st.error("Invalid credentials")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forgot Password?", key="fp_btn"):
            st.session_state.page = "forgot"; st.rerun()
    with col2:
        if st.button("Sign Up", key="su_btn"):
            st.session_state.page = "signup"; st.rerun()

def show_forgot():
    st.markdown("<div class='glass'><h1>Recover Account</h1><p>Pick a recovery option</p></div>", unsafe_allow_html=True)
    option = st.radio("", ["Email", "Mobile OTP", "Auth App", "Security Qs"], label_visibility="collapsed")
    if st.button("Proceed"):
        st.success(f"Recovery via **{option}** triggered!")
    if st.button("Back to Login"):
        st.session_state.page = "login"; st.rerun()

def show_signup():
    st.markdown("<div class='glass'><h1>Sign Up</h1><p>Create your crypto account</p></div>", unsafe_allow_html=True)
    with st.form("signup_form"):
        st.text_input("Username", key="su_user", placeholder="Pick a username", label_visibility="collapsed", **{"class":"neon-input"})
        st.text_input("Email", key="su_email", placeholder="you@example.com", label_visibility="collapsed", **{"class":"neon-input"})
        st.text_input("Password", type="password", key="su_pass", placeholder="Password", label_visibility="collapsed", **{"class":"neon-input"})
        st.text_input("Confirm Password", type="password", key="su_pass2", placeholder="Confirm Password", label_visibility="collapsed", **{"class":"neon-input"})
        if st.form_submit_button("Create Account", **{"class":"neon-btn"}):
            u, p1, p2 = st.session_state.su_user, st.session_state.su_pass, st.session_state.su_pass2
            if u in st.session_state.USER_CREDENTIALS: st.error("Username already taken")
            elif p1 != p2: st.error("Passwords do not match")
            else:
                st.session_state.USER_CREDENTIALS[u] = p1
                st.success(f"Account created for **{u}**!")
                st.snow()
                st.session_state.page = "login"; st.rerun()
    if st.button("Back to Login"):
        st.session_state.page = "login"; st.rerun()

# -- ROUTE --
if st.session_state.page == "login":
    show_login()
elif st.session_state.page == "forgot":
    show_forgot()
elif st.session_state.page == "signup":
    show_signup()
