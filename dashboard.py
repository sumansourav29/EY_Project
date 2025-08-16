# add this near the top of your file (with your existing imports)
import streamlit as st

# --- Footer renderer (drop into your app.py) ---
def render_bottom_footer():
    username = st.session_state.get("auth", {}).get("username") or "Guest"
    logged_in = st.session_state.get("auth", {}).get("logged_in", False)

    FOOTER_CSS = f"""
    <style>
    /* Footer container */
    .bottom-footer {{
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      height: 72px;
      background: linear-gradient(90deg, rgba(11,16,32,0.98) 0%, rgba(15,21,53,0.98) 100%);
      border-top: 1px solid rgba(60,70,100,0.12);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 18px;
      z-index: 9999;
      backdrop-filter: blur(6px);
      box-shadow: 0 -6px 18px rgba(5,8,20,0.35);
      color: #e8ebff;
      font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }}

    .nav-block {{
      display:flex;
      gap: 10px;
      align-items:center;
    }}

    .nav-item {{
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      min-width:72px;
      padding:8px 10px;
      border-radius:10px;
      text-decoration: none;
      color: #cfd8ff;
      font-size:12px;
      transition: all 0.12s ease-in-out;
    }}

    .nav-item:hover {{
      transform: translateY(-4px);
      background: rgba(255,255,255,0.02);
      color: #ffffff;
    }}

    .nav-item .icon {{
      font-size:18px;
      margin-bottom:4px;
    }}

    .account-circle {{
      display:flex;
      align-items:center;
      gap:10px;
    }}

    .avatar {{
      width:44px; height:44px; border-radius:50%;
      background: linear-gradient(135deg, #1f2b66, #2f7f5f);
      display:flex; align-items:center; justify-content:center;
      color: white; font-weight:700; font-size:14px;
      box-shadow: 0 4px 12px rgba(20,30,60,0.45);
      border: 1px solid rgba(255,255,255,0.06);
    }}

    .account-name {{
      font-size:13px; color:#e8ebff; font-weight:600;
    }}

    /* Make room for the fixed footer so Streamlit content doesn't get hidden */
    .stApp > .main {{
      padding-bottom: 110px;
    }}

    /* responsive: hide labels on narrow screens */
    @media (max-width: 720px){{
      .nav-item span.label {{ display:none; }}
      .nav-item {{ min-width:56px; padding:6px; }}
      .account-name {{ display:none; }}
    }}
    </style>
    """

    FOOTER_HTML = f"""
    {FOOTER_CSS}
    <div class="bottom-footer" aria-hidden="false">
      <div class="nav-block" style="margin-left:6px;">
        <a class="nav-item" href="#dashboard" title="Dashboard">
          <div class="icon">🏠</div>
          <span class="label">Dashboard</span>
        </a>
        <a class="nav-item" href="#charts" title="Charts">
          <div class="icon">📈</div>
          <span class="label">Charts</span>
        </a>
        <a class="nav-item" href="#wallet" title="Wallet">
          <div class="icon">👛</div>
          <span class="label">Wallet</span>
        </a>
        <a class="nav-item" href="#news" title="News">
          <div class="icon">📰</div>
          <span class="label">News</span>
        </a>
        <a class="nav-item" href="#settings" title="Settings">
          <div class="icon">⚙️</div>
          <span class="label">Settings</span>
        </a>
      </div>

      <div class="account-circle">
        <div class="avatar">{ (username[:2].upper() if username else 'G') }</div>
        <div style="display:flex;flex-direction:column;align-items:flex-start;">
          <div class="account-name">{ username if logged_in else 'Guest (Sign in)' }</div>
          <div style="font-size:11px;color:#9fb0ff;">Account</div>
        </div>
      </div>
    </div>
    """

    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# --- End footer renderer ---
