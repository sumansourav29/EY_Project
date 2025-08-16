import streamlit as st

# ----------------------
# Login Page
# ----------------------
def login_page():
    st.title("🔑 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.page = "otp"
        else:
            st.error("Invalid username or password")

    st.markdown(
        """
        <div style="text-align:center; margin-top:15px;">
            <a href="?signup=true" style="margin-right:20px; font-weight:bold;">Sign Up</a>
            <a href="?forgot=true" style="font-weight:bold;">Forgot Password?</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Handle query params
    query_params = st.query_params
    if "signup" in query_params:
        st.session_state.page = "signup"
        st.query_params.clear()
    if "forgot" in query_params:
        st.session_state.page = "forgot"
        st.query_params.clear()


# ----------------------
# Sign Up Page
# ----------------------
def signup_page():
    st.title("📝 Sign Up")

    new_user = st.text_input("New Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password == confirm_password:
            st.success("✅ Account created successfully! Please login.")
            st.session_state.page = "login"
        else:
            st.error("❌ Passwords do not match.")

    st.markdown('<a href="?back=true">⬅️ Back to Login</a>', unsafe_allow_html=True)

    query_params = st.query_params
    if "back" in query_params:
        st.session_state.page = "login"
        st.query_params.clear()


# ----------------------
# Forget Password Page
# ----------------------
def forgot_password_page():
    st.title("🔒 Forgot Password")

    email = st.text_input("Enter your registered Email")

    if st.button("Send Reset Link"):
        st.success(f"📩 Reset link sent to {email}")

    st.markdown('<a href="?back=true">⬅️ Back to Login</a>', unsafe_allow_html=True)

    query_params = st.query_params
    if "back" in query_params:
        st.session_state.page = "login"
        st.query_params.clear()


# ----------------------
# OTP Page
# ----------------------
def otp_page():
    st.title("🔐 Email Verification")
    st.write("OTP has been sent to **su.....@gmail.com**")

    CORRECT_OTP = "291004"

    if "otp_popup" not in st.session_state:
        st.session_state.otp_popup = None

    st.markdown(
        """
        <style>
        .otp-input input {
            text-align: center;
            font-size: 22px !important;
            font-weight: bold;
            width: 50px !important;
            height: 50px !important;
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
        .resend { color:#00ccaa; }
        .back { color:#ff4b4b; }
        .popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: black;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            z-index: 9999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(6)
    otp_digits = []
    for i, col in enumerate(cols):
        with col:
            digit = st.text_input(
                "", max_chars=1, key=f"otp{i}", label_visibility="collapsed"
            )
            otp_digits.append(digit)

    otp_entered = "".join(otp_digits)

    # Auto-focus script
    st.markdown(
        """
        <script>
        const inputs = window.parent.document.querySelectorAll("input[type='text']");
        inputs.forEach((input, index) => {
            input.addEventListener("input", () => {
                if (input.value.length === 1 && index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            });
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    verify_disabled = len(otp_entered) < 6
    if st.button("Verify OTP", disabled=verify_disabled):
        if otp_entered == CORRECT_OTP:
            st.session_state.otp_popup = '<div class="popup">✅ Login Successful!</div>'
        else:
            st.session_state.otp_popup = '<div class="popup" style="color:red;">❌ Wrong OTP, try again</div>'

    if st.session_state.otp_popup:
        st.markdown(st.session_state.otp_popup, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="link-container">
            <a href="?resend=true" class="resend">🔄 Resend OTP</a> &nbsp;&nbsp;|&nbsp;&nbsp;
            <a href="?back=true" class="back">⬅️ Back to Login</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    query_params = st.query_params
    if "resend" in query_params:
        st.info("📩 New OTP has been sent! (For testing: 291004)")
        st.query_params.clear()
    if "back" in query_params:
        st.session_state.page = "login"
        st.query_params.clear()


# ----------------------
# Main App
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "forgot":
    forgot_password_page()
elif st.session_state.page == "otp":
    otp_page()
