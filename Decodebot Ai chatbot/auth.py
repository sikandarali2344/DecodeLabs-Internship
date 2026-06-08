import streamlit as st
import json
import os
import pandas as pd
from PIL import Image

USER_DATA_FILE = "user/users.csv"

def load_user_data():
    os.makedirs("user", exist_ok=True)
    expected_columns = ["username", "email", "password"]
    
    if not os.path.isfile(USER_DATA_FILE):
        df = pd.DataFrame(columns=expected_columns)
        df.to_csv(USER_DATA_FILE, index=False)
        return df

    try:
        df = pd.read_csv(USER_DATA_FILE)
        if df.empty or df.shape[1] == 0:
            df = pd.DataFrame(columns=expected_columns)
            df.to_csv(USER_DATA_FILE, index=False)
            return df
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        return df
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=expected_columns)
        df.to_csv(USER_DATA_FILE, index=False)
        return df

def load_logo():
    """Load logo from various possible locations"""
    logo_paths = [
        
        "assets/logo.png",
        "assets/logo.jpg",
        "logo.png",
        "logo.jpg"
    ]
    
    for path in logo_paths:
        if os.path.exists(path):
            try:
                logo = Image.open(path)
                # Resize logo for better display
                if logo.size[0] > 80:
                    logo = logo.resize((80, 80))
                return logo
            except:
                pass
    return None

# ---------------------- COMMON STYLES ----------------------
def render_background_style():
    st.markdown("""
        <style>
        body, .main, .block-container {
            width: 100%;
            height: 100%;
            margin: 0;
            background: linear-gradient(-45deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 400% 400%;
            animation: gradientAnimation 12s ease infinite;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }

        @keyframes gradientAnimation {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        /* Main container styling */
        .main-container {
            max-width: 450px;
            margin: 0 auto;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Title styling */
        .logo-center {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-weight: 800;
            font-size: 2.5rem;
            margin-bottom: 0.3rem;
            text-align: center;
            background: linear-gradient(135deg, #fff, #a8c0ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline {
            text-align: center;
            color: rgba(255,255,255,0.85);
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }
        
        h2 {
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            text-align: center;
            color: #ffffff;
        }
        
        .subtitle {
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }

        /* Stylish button */
        .stButton>button {
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: #fff;
            border: none;
            border-radius: 50px;
            padding: 0.6rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            background: linear-gradient(90deg, #764ba2, #667eea);
        }

        /* Input field styling */
        .stTextInput>div>div>input {
            background: rgba(255,255,255,0.95);
            border: 2px solid transparent;
            border-radius: 50px;
            padding: 0.6rem 1.2rem;
            font-size: 0.95rem;
            color: #333;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            background: white;
        }
        
        /* Label styling */
        .stTextInput label {
            font-weight: 500;
            color: #fff !important;
            margin-bottom: 0.3rem;
            display: block;
            font-size: 0.9rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.7);
        }

        a {
            color: #fff;
            text-decoration: underline;
            font-weight: 500;
        }
        
        a:hover {
            color: #a8c0ff;
        }
        
        /* Error/Success message styling */
        .stAlert {
            border-radius: 10px;
            border: none;
        }
        
        /* Divider */
        .divider {
            text-align: center;
            margin: 1.2rem 0;
            color: rgba(255,255,255,0.5);
            font-size: 0.8rem;
        }
        
        /* Bot icon animation */
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .bot-icon {
            text-align: center;
            font-size: 3.5rem;
            animation: float 3s ease-in-out infinite;
            margin-bottom: 0.5rem;
        }
        
        /* Info box styling */
        .info-box {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 0.8rem;
            margin-top: 1rem;
            font-size: 0.8rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)


# ---------------------- SIGN UP PAGE ----------------------
def render_signup(user_data):
    user_data = load_user_data()
    render_background_style()
    
    # Display Logo
    logo = load_logo()
    if logo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, width=80)
    
    st.markdown("<h1>DecodeBot AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Your Intelligent AI Assistant | Created by Sikandar 2026</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='bot-icon'>🔐</div>", unsafe_allow_html=True)
    st.markdown("<h2>Create Account</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Join DecodeBot AI and start your intelligent conversation journey</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        
        st.markdown("<label>👤 Username</label>", unsafe_allow_html=True)
        username = st.text_input("Username", key="signup_username", label_visibility="collapsed", placeholder="Choose a username")
        
        st.markdown("<label>📧 Email Address</label>", unsafe_allow_html=True)
        email = st.text_input("Email", key="signup_email", label_visibility="collapsed", placeholder="your@email.com")
        
        st.markdown("<label>🔒 Password</label>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", key="signup_password", label_visibility="collapsed", placeholder="Create a strong password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ Sign Up", key="signup_btn"):
            if not username.strip() or not email.strip() or not password.strip():
                st.error("🚫 All fields are required!")
            elif username in user_data["username"].values:
                st.error("🚫 Username already taken. Please choose another.")
            elif "@" not in email or "." not in email:
                st.error("🚫 Please enter a valid email address!")
            elif len(password) < 4:
                st.error("🚫 Password must be at least 4 characters long!")
            else:
                new_user = pd.DataFrame({
                    "username": [username],
                    "email": [email],
                    "password": [password]
                })
                user_data = pd.concat([user_data, new_user], ignore_index=True)
                user_data.to_csv(USER_DATA_FILE, index=False)
                st.success("✅ Account created successfully! You can now log in.")
                st.balloons()
                st.session_state.page_option = "Login"
                st.rerun()
        
        st.markdown("<div class='divider'>────────── Already have an account? ──────────</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔐 Login Here", use_container_width=True):
                st.session_state.page_option = "Login"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='footer'>Made with ❤️ by Sikandar 2026 | © 2026 DecodeBot AI. All rights reserved.</div>", unsafe_allow_html=True)


# ---------------------- LOGIN PAGE ----------------------
def render_login(user_data):
    user_data = load_user_data()
    render_background_style()
    
    # Display Logo
    logo = load_logo()
    if logo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, width=80)
    
    st.markdown("<h1>DecodeBot AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Your Intelligent AI Assistant | Created by Sikandar 2026</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='bot-icon'>🤖</div>", unsafe_allow_html=True)
    st.markdown("<h2>Welcome Back!</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Login to continue your conversation with DecodeBot AI</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        
        st.markdown("<label>📧 Username or Email</label>", unsafe_allow_html=True)
        login_input = st.text_input("Username or Email", key="login_user_input", label_visibility="collapsed", placeholder="Enter your username or email")
        
        st.markdown("<label>🔑 Password</label>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", key="login_password", label_visibility="collapsed", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔐 Login to DecodeBot AI", key="login_btn"):
            if login_input.strip() == "" or password.strip() == "":
                st.error("⚠️ All fields are required!")
            else:
                user_row = user_data[(user_data['email'] == login_input) | (user_data['username'] == login_input)]
                
                if user_row.empty:
                    st.error("❌ Username or Email not found. Please sign up first.")
                elif user_row['password'].values[0] != password:
                    st.error("❌ Incorrect password. Please try again.")
                else:
                    st.session_state.logged_in_user = user_row['email'].values[0] 
                    st.session_state.logged_in_user_email = user_row['email'].values[0]
                    st.session_state.logged_in_username = user_row['username'].values[0]
                    st.success(f"✅ Welcome back, {user_row['username'].values[0]}!")
                    st.balloons()
                    st.session_state.page_option = "Chat with Bot"
                    st.rerun()
        
        st.markdown("<div class='divider'>────────── Don't have an account? ──────────</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📝 Sign Up Here", use_container_width=True):
                st.session_state.page_option = "Sign Up"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Demo credentials info
    with st.expander("ℹ️ Demo Credentials (for testing)"):
        st.markdown("""
        - **Username:** `demo_user` or **Email:** `demo@example.com`
        - **Password:** `demo123`
        """)
    
    st.markdown("<div class='footer'>Made with ❤️ by Sikandar 2026 | © 2026 DecodeBot AI. All rights reserved.</div>", unsafe_allow_html=True)