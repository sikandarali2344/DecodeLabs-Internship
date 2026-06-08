import streamlit as st
import os
import base64
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from PIL import Image
from io import BytesIO

from auth import load_user_data, render_login, render_signup
from sidebar import render_sidebar
from bot import render_bot

# Helper function for base64 encoding
def get_image_base64(image_path):
    """Convert image to base64 string for HTML embedding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load environment variables
load_dotenv()
key = os.getenv("API_KEY")

if not key:
    st.error("⚠️ API_KEY not found in .env file")
    st.stop()

# Chat model
chat_model = ChatGroq(
    api_key=key,
    model_name="deepseek-r1-distill-llama-70b"
)

# Load logo if exists
logo_path = "DEmo/logo.png"  # Try PNG first
if not os.path.exists(logo_path):
    logo_path = "DEmo/logo.jpg"  # Try JPG
if not os.path.exists(logo_path):
    logo_path = "assets/logo.png"  # Try assets folder
if not os.path.exists(logo_path):
    logo_path = "logo.png"  # Try root folder

# Page config with logo
if os.path.exists(logo_path):
    st.set_page_config(
        page_title="DecodeBot AI", 
        page_icon=Image.open(logo_path), 
        layout="wide"
    )
else:
    st.set_page_config(
        page_title="DecodeBot AI", 
        page_icon="🤖", 
        layout="wide"
    )

# ==========================================
# FIXED CONSISTENT CSS - SAME BACKGROUND FOR ALL PAGES
# ==========================================
st.markdown("""
    <style>
    /* FIXED BACKGROUND - NEVER CHANGES */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Sidebar styling - consistent */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0c29 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    /* Headers - white text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* All text white */
    p, span, label, div, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Button styling - consistent */
    .stButton > button {
        background: linear-gradient(90deg, #4A90E2, #9013FE) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(74,144,226,0.3) !important;
    }
    
    /* Input fields - consistent */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 10px rgba(74,144,226,0.3) !important;
    }
    
    /* Success/Error/Warning messages */
    .stAlert {
        background: rgba(255,255,255,0.1) !important;
        border: none !important;
        border-radius: 12px !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 16px !important;
        padding: 15px !important;
    }
    
    [data-testid="stMetric"] label {
        color: #4A90E2 !important;
    }
    
    [data-testid="stMetric"] .stMetricValue {
        color: white !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Circle logo styling */
    .logo-container {
        text-align: center;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .circle-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid rgba(255,255,255,0.5);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        display: block;
        margin: 0 auto;
    }
    
    .circle-logo:hover {
        transform: scale(1.05);
    }
    
    .logo-title {
        font-size: 55px;
        font-weight: 800;
        color: white;
        margin-top: 15px;
        margin-bottom: 5px;
        text-align: center;
    }
    
    .logo-subtitle {
        font-size: 18px;
        color: rgba(255,255,255,0.85);
        margin-top: 0;
        text-align: center;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4A90E2;
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: rgba(255,255,255,0.5);
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CENTERED CIRCLE LOGO + TITLE SECTION
# ==========================================

if os.path.exists(logo_path):
    # Display centered circular logo
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    
    # Center the logo using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Load and display logo as circle using HTML/CSS
        logo = Image.open(logo_path)
        
        # Resize if needed to maintain good quality
        if logo.size[0] > 200:
            logo = logo.resize((200, 200))
        
        # Save temporarily to display with custom styling
        temp_path = "temp_circle_logo.png"
        logo.save(temp_path)
        
        # Display as circle using HTML/CSS
        if os.path.exists(temp_path):
            st.markdown(f'''
            <img src="data:image/png;base64,{get_image_base64(temp_path)}" class="circle-logo" alt="DecodeBot Logo">
            ''', unsafe_allow_html=True)
            
            # Clean up temp file
            os.remove(temp_path)
    
    # Title below logo
    st.markdown('<div class="logo-title">DecodeBot AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-subtitle">Advanced Rule-Based Chatbot System | Created by Sikandar 2026</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Fallback when no logo image exists
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(145deg, #f0f0ff, #dedeff); display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 60px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
            🤖
        </div>
        <h1 style="font-size: 55px; color: white; margin-top: 15px;">DecodeBot AI</h1>
        <p style="color: rgba(255,255,255,0.85);">Advanced Rule-Based Chatbot System | Created by Sikandar 2026</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Session state
if "page_option" not in st.session_state:
    st.session_state.page_option = "Login"

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Load users
user_data = load_user_data()

# Sidebar
sidebar_option = render_sidebar()
if sidebar_option:
    st.session_state.page_option = sidebar_option

# Auto route if logged in
if st.session_state.logged_in_user:
    st.session_state.page_option = "Chat with Bot"

# Routing
if st.session_state.page_option == "Sign Up":
    render_signup(user_data)

elif st.session_state.page_option == "Login":
    render_login(user_data)

elif st.session_state.page_option == "Chat with Bot":
    if not st.session_state.logged_in_user:
        st.warning("⚠️ Please log in first.")
        st.session_state.page_option = "Login"
        st.rerun()
    else:
        render_bot(chat_model)

else:
    st.warning("🔄 Invalid state reset...")
    st.session_state.page_option = "Login"
    st.rerun()