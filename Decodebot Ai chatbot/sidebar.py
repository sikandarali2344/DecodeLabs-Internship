import streamlit as st
import pandas as pd

def load_user_data():
    try:
        return pd.read_csv("users.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["email", "username", "password"])

def logout_user():
    keys_to_clear = ["logged_in_user", "page_option", "chat_history", "input_question", "chat_input"]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
    st.success("✅ You have been logged out.")
    st.rerun()

def add_sidebar_footer():
    st.markdown(
        """
        <style>
        .sidebar-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 12px 15px;
            background-color: #0e1117;
            color: #ccc;
            font-size: 0.78rem;
            text-align: center;
            border-top: 1px solid #333;
            z-index: 999;
        }
        .sidebar-footer a {
            color: #66c2ff;
            text-decoration: none;
        }
        .sidebar-footer a:hover {
            text-decoration: underline;
        }
        </style>

        <div class="sidebar-footer">
            <span>Made with ❤️ by <a href="https://github.com/sikandar2026" target="_blank">Sikandar 2026</a></span>
            <span>© 2026 DecodeBot AI. All rights reserved.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_sidebar():
    st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color:#6C63FF;font-size: 35px;">🤖 DecodeBot AI</h2>
            <p style="font-size: 18px; color: gray;">Your intelligent AI assistant</p>
            <p style="font-size: 12px; color: #4A90E2;">Developed by Sikandar 2026</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    if st.session_state.get('logged_in_user'):
        username = st.session_state.get('logged_in_username', 'User')
        email = st.session_state.get('logged_in_user_email', '')
        st.sidebar.markdown("#### 👤 Profile")
        st.sidebar.markdown(f"**Username:** `{username}`")
        st.sidebar.markdown(f"**Email:** `{email}`")

        st.sidebar.markdown("---")

        # Chat Controls
        st.sidebar.markdown("### 💬 Chat Options")
        
        # New Chat Button
        if st.sidebar.button("🆕 New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.chat_history = []
            st.session_state.input_question = ""
            st.rerun()
        
        # Clear History Button
        if st.sidebar.button("🗑️ Clear History", use_container_width=True, key="clear_history_btn"):
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # Bot Status
        st.sidebar.markdown("""
        <div style="margin-top: 20px; padding: 15px; background: rgba(74,144,226,0.1); border-radius: 12px;">
            <p style="font-size: 12px; margin: 0;">🔵 Status: <span style="color: #4A90E2;">Online</span></p>
            <p style="font-size: 12px; margin: 5px 0 0;">⚡ Powered by DeepSeek</p>
            <p style="font-size: 12px; margin: 5px 0 0;">🎓 Internship Project</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        
        with st.sidebar.container():
            if st.sidebar.button("🚪 Logout", key="logout-btn", use_container_width=True):
                logout_user()

        add_sidebar_footer()
        return "Chat with Bot"

    else:
        st.sidebar.markdown("### 🧭 Navigation")
        option = st.sidebar.radio(
            "Choose an option:",
            ["📝 Sign Up", "🔐 Login"],
            label_visibility="collapsed"
        )
        
        # Bot Status for non-logged in users
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <div style="margin-top: 20px; padding: 15px; background: rgba(74,144,226,0.1); border-radius: 12px;">
            <p style="font-size: 12px; margin: 0;">🤖 <strong>DecodeBot AI</strong></p>
            <p style="font-size: 11px; margin: 5px 0 0;">Sign up or login to start chatting!</p>
        </div>
        """, unsafe_allow_html=True)
        
        add_sidebar_footer()
        
        # Return the selected option without "📝 " and "🔐 " prefixes
        if option == "📝 Sign Up":
            return "Sign Up"
        else:
            return "Login"