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

    # Fixed OTP for verification
    CORRECT_OTP = "291004"

    # CSS for square OTP boxes + auto focus
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

        /* Popup modal */
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

        <script>
        document.addEventListener("DOMContentLoaded", function(){
            const inputs = document.querySelectorAll("input[type='text']");
            inputs.forEach((input, index) => {
                input.addEventListener("input", () => {
                    if (input.value.length === 1 && index < inputs.length - 1) {
                        inputs[index + 1].focus();
                    }
                });
            });
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    # OTP input fields
    cols = st.columns(6)
    otp_digits = []
    for i, col in enumerate(cols):
        with col:
            digit = st.text_input("", max_chars=1, key=f"otp{i}", label_visibility="collapsed")
            otp_digits.append(digit)

    otp_entered = "".join(otp_digits)

    # Verify OTP button (disabled until all boxes filled)
    verify_disabled = len(otp_entered) < 6
    if st.button("Verify OTP", disabled=verify_disabled):
        if otp_entered == CORRECT_OTP:
            st.markdown('<div class="popup">✅ Login Successful!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="popup" style="color:red;">❌ Wrong OTP, try again</div>', unsafe_allow_html=True)

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

    # Handle link clicks with st.query_params
    query_params = st.query_params
    if "resend" in query_params:
        st.info("📩 New OTP has been sent! (For testing: 291004)")
        st.query_params.clear()
    if "back" in query_params:
        st.session_state.page = "login"
        st.query_params.clear()




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


