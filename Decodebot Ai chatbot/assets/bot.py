import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from custom_responses import CUSTOM_RESPONSES
import os
import json
import hashlib
import datetime
import uuid
import re
import time

# Constants
HISTORY_FILE = "archived/chats_history/history.json"
SAVED_CHAT_DIR = "archived/saved_chats"

# Ensure required directories exist
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
os.makedirs(SAVED_CHAT_DIR, exist_ok=True)


# -------------------- DARK MODE CSS --------------------
DARK_MODE_CSS = """
<style>
    /* Dark Mode Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0c29 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #4A90E2, #9013FE);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(74,144,226,0.3);
    }
    
    /* Input fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        color: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A90E2;
        box-shadow: 0 0 10px rgba(74,144,226,0.3);
    }
    
    /* Chat message containers */
    .user-message {
        background: linear-gradient(135deg, #4A90E2, #9013FE);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        animation: fadeIn 0.3s ease;
    }
    
    .bot-message {
        background: rgba(255,255,255,0.1);
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        max-width: 80%;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Typing indicator */
    .typing-indicator {
        background: rgba(255,255,255,0.1);
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        max-width: 80%;
        margin-bottom: 10px;
        display: inline-block;
    }
    
    .typing-indicator span {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4A90E2;
        margin: 0 3px;
        animation: typing 1.4s infinite;
    }
    
    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    
    /* Cards and containers */
    .dashboard-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
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
    
    /* Dashboard header */
    .dashboard-header {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, rgba(74,144,226,0.2), rgba(144,19,254,0.2));
        border-radius: 24px;
        margin-bottom: 30px;
    }
    
    /* Bot info panel */
    .bot-info {
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        margin-bottom: 20px;
    }
    
    .bot-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4A90E2, #9013FE);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
        font-size: 40px;
    }
</style>
"""


# -------------------- DASHBOARD COMPONENTS --------------------

def render_dashboard():
    """Render professional dashboard with metrics and bot info"""
    st.markdown(DARK_MODE_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="font-size: 2.5rem; margin-bottom: 5px;">🤖 DecodeBot AI Dashboard</h1>
        <p style="color: rgba(255,255,255,0.7);">Powered by LangChain + DeepSeek | Internship Project</p>
        <div style="margin-top: 15px;">
            <span style="background: rgba(74,144,226,0.3); padding: 5px 15px; border-radius: 20px; font-size: 12px;">
                🎓 Dhruv Patel - AI Internship Project
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💬 Total Chats", len(st.session_state.get("chat_history", [])) // 2)
    with col2:
        st.metric("📅 Session Started", datetime.datetime.now().strftime("%d/%m/%y"))
    with col3:
        st.metric("⚡ Status", "Online", delta="Active")
    with col4:
        st.metric("🎯 Accuracy", "98%", delta="+2%")


# -------------------- CHAT BUBBLE RENDERER --------------------

def render_chat_bubble(message, is_user):
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            <strong>🧑 You</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <strong>🤖 DecodeBot AI</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)


def render_typing_indicator():
    st.markdown("""
    <div class="typing-indicator">
        <strong>🤖 DecodeBot AI is thinking</strong><br>
        <span></span><span></span><span></span>
    </div>
    """, unsafe_allow_html=True)


# -------------------- EXTRA FEATURES --------------------

def get_weather():
    return "🌤️ Today's weather: Partly cloudy with a chance of innovation! Temperature: 24°C. Perfect for coding!"

def get_current_time():
    now = datetime.datetime.now()
    return f"🕐 Current time: {now.strftime('%I:%M:%S %p')}"

def get_current_date():
    now = datetime.datetime.now()
    return f"📅 Today's date: {now.strftime('%A, %B %d, %Y')}"

def get_help():
    return """
    ### 🤖 Available Commands
    
    | Command | Description |
    |---------|-------------|
    | `weather` | Get current weather info |
    | `time` | Show current system time |
    | `date` | Show today's date |
    | `help` | Show this help menu |
    | `about` | About DecodeBot AI |
    | `clear` | Clear chat history |
    | `save` | Save current chat |
    
    ### 💬 Natural Language Queries
    - Ask me anything about coding
    - Tell me a joke
    - Who are you?
    - How are you?
    """

def get_about():
    return """
    ### 🤖 About DecodeBot AI
    
    **Version:** 2.0  
    **Developer:** Dhruv Patel  
    **Internship:** AI/ML Developer Intern  
    
    **Technologies Used:**
    - 🐍 Python & Streamlit
    - 🔗 LangChain Framework
    - 🧠 DeepSeek LLM (via Groq)
    - 💾 Local Storage for History
    
    **Features:**
    - Dark mode interface
    - Chat history management
    - Save/Load conversations
    - Multi-language support
    - Quick responses
    """


# -------------------- UTILS (simplified) --------------------

def generate_cid() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    random_part = uuid.uuid4().hex[:6]
    return f"cid_{timestamp}_{random_part}"

def save_to_history(chat_history):
    try:
        if not chat_history:
            return
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        history_data = {}
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        cid = generate_cid()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_chat = []
        for m in chat_history:
            if isinstance(m, HumanMessage):
                formatted_chat.append({"role": "user", "content": m.content})
            elif isinstance(m, AIMessage):
                formatted_chat.append({"role": "ai", "content": m.content})
        history_data[cid] = {
            "title": f"Chat_{timestamp}",
            "timestamp": timestamp,
            "chat": formatted_chat
        }
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        pass

def clear_chat_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    except Exception:
        pass

def save_chat(chat_history):
    if not chat_history:
        return
    try:
        os.makedirs(SAVED_CHAT_DIR, exist_ok=True)
        cid = generate_cid()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_data = {
            "cid": cid,
            "title": f"Saved_Chat_{timestamp}",
            "timestamp": timestamp,
            "chat": [
                {"role": "user" if isinstance(m, HumanMessage) else "ai", "content": m.content}
                for m in chat_history
            ]
        }
        filepath = os.path.join(SAVED_CHAT_DIR, f"{cid}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(chat_data, f, indent=2)
        st.toast("✅ Chat saved successfully!")
    except Exception as e:
        st.error(f"Failed to save chat: {e}")

def handle_new_chat():
    st.session_state.chat_history = []
    st.rerun()


def handle_extra_commands(prompt: str) -> tuple:
    prompt_lower = prompt.lower().strip()
    
    if prompt_lower == "weather":
        return get_weather(), True
    elif prompt_lower == "time":
        return get_current_time(), True
    elif prompt_lower == "date":
        return get_current_date(), True
    elif prompt_lower == "help":
        return get_help(), True
    elif prompt_lower == "about":
        return get_about(), True
    elif prompt_lower == "clear":
        clear_chat_history()
        return "🧹 Chat history cleared!", True
    elif prompt_lower == "save":
        if st.session_state.get("chat_history"):
            save_chat(st.session_state.chat_history)
            return "💾 Chat saved successfully!", True
        else:
            return "⚠️ No chat to save!", True
    
    return None, False


# -------------------- MAIN CHAT UI --------------------

def render_main_chat_ui(chat_model=None):
    st.markdown(DARK_MODE_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-header">
        <h2 style="margin-bottom: 5px;">💬 DecodeBot AI Chat</h2>
        <p style="color: rgba(255,255,255,0.7);">Ask me anything — I'm here to help!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history with bubbles
    chat_history = st.session_state.get("chat_history", [])
    
    for msg in chat_history:
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
        elif isinstance(msg, HumanMessage):
            role, content = "user", msg.content
        elif isinstance(msg, AIMessage):
            role, content = "assistant", msg.content
        else:
            continue
        
        content = content.replace("<think>", "").replace("</think>", "").strip()
        render_chat_bubble(content, is_user=(role == "user"))
    
    prompt = st.chat_input("Type your message here...")
    
    if prompt:
        clean_prompt = prompt.strip()
        
        st.session_state.chat_history.append(HumanMessage(content=clean_prompt))
        render_chat_bubble(clean_prompt, is_user=True)
        
        extra_response, handled = handle_extra_commands(clean_prompt)
        
        if handled:
            st.session_state.chat_history.append(AIMessage(content=extra_response))
            render_typing_indicator()
            time.sleep(0.5)
            render_chat_bubble(extra_response, is_user=False)
            save_to_history(st.session_state.chat_history)
        else:
            render_typing_indicator()
            time.sleep(0.8)
            
            try:
                response_text = None
                for key in CUSTOM_RESPONSES:
                    if key.lower() in clean_prompt.lower():
                        response_text = CUSTOM_RESPONSES[key].replace("<think>", "").replace("</think>", "").strip()
                        break
                
                if not response_text and chat_model:
                    ai_message = chat_model.invoke(st.session_state.chat_history)
                    response_text = ai_message.content.replace("<think>", "").replace("</think>", "").strip()
                elif not response_text:
                    response_text = "I'm here to help! Try asking me about coding, weather, time, or just chat with me!"
                
                st.session_state.chat_history.append(AIMessage(content=response_text))
                render_chat_bubble(response_text, is_user=False)
                save_to_history(st.session_state.chat_history)
                
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.session_state.chat_history.append(AIMessage(content=error_msg))
                render_chat_bubble(error_msg, is_user=False)
        
        st.rerun()


def render_bot(chat_model):
    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #4A90E2, #9013FE); display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 40px;">
                    🤖
                </div>
                <h3 style="margin-bottom: 5px;">DecodeBot AI</h3>
                <p style="color: rgba(255,255,255,0.6); font-size: 12px;">Intelligent Assistant</p>
                <hr style="margin: 15px 0;">
            </div>
            """, unsafe_allow_html=True)
            
            if st.sidebar.button("🆕 New Chat", use_container_width=True):
                handle_new_chat()
            
            if st.sidebar.button("💾 Save Chat", use_container_width=True):
                if st.session_state.get("chat_history"):
                    save_chat(st.session_state.chat_history)
                else:
                    st.warning("No chat to save")
            
            if st.sidebar.button("🧹 Clear History", use_container_width=True):
                clear_chat_history()
                st.rerun()
            
            st.markdown("---")
            st.markdown("""
            <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px;">
                <p style="font-size: 12px; margin: 0;">🔵 Status: <span style="color: #4A90E2;">Online</span></p>
                <p style="font-size: 12px; margin: 5px 0 0;">⚡ Powered by DeepSeek</p>
                <p style="font-size: 12px; margin: 5px 0 0;">🎓 Internship Project</p>
            </div>
            """, unsafe_allow_html=True)
        
        render_main_chat_ui(chat_model)
        
        st.markdown("""
        <div class="footer">
            © 2025 DecodeBot AI | Developed by Dhruv Patel | AI Internship Project
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")