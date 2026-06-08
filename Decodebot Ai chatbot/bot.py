import streamlit as st
from streamlit_lottie import st_lottie
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
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
LOTTIE_PATH = "welcome.json"
SAVED_CHAT_DIR = "archived/saved_chats"

# Ensure required directories exist
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
os.makedirs(SAVED_CHAT_DIR, exist_ok=True)


# -------------------- ENHANCED SYSTEM PROMPT --------------------
SYSTEM_PROMPT = """You are DecodeBot AI, an expert AI assistant created by Sikandar 2026. 
You are friendly, helpful, and enthusiastic. Your specialties include:

1. **CODE WRITING & EXPLANATION:**
   - Write clean, well-documented code with proper syntax
   - Explain code line-by-line in simple terms
   - Provide multiple solutions when applicable
   - Include example usage and best practices

2. **PROBLEM SOLVING:**
   - Break down complex problems into steps
   - Explain concepts with analogies and examples
   - Debug errors and suggest fixes

3. **GENERAL ASSISTANCE:**
   - Answer questions accurately
   - Have friendly conversations
   - Tell jokes and be engaging
   - Support multiple languages (English, Hindi, Gujarati)

4. **RESPONSE FORMAT:**
   - Use proper formatting with line breaks
   - Show code in code blocks
   - Be concise but thorough
   - Be positive and encouraging

You are powered by DeepSeek R1 via Groq. Always respond in a helpful, enthusiastic manner.
Current time: {current_time}
Current date: {current_date}
"""


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
    
    /* Chat message containers */
    .user-message {
        background: linear-gradient(135deg, #4A90E2, #9013FE);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 10px;
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
    
    /* Code block styling */
    pre {
        background: #1e1e1e !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        overflow-x: auto !important;
        border: 1px solid #333 !important;
    }
    
    code {
        color: #d4d4d4 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
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


# -------------------- CHAT BUBBLE RENDERER --------------------

def render_chat_bubble(message, is_user):
    """Render individual chat bubble with styling"""
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
    """Show typing animation"""
    st.markdown("""
    <div class="typing-indicator">
        <strong>🤖 DecodeBot AI is thinking</strong><br>
        <span></span><span></span><span></span>
    </div>
    """, unsafe_allow_html=True)


# -------------------- DEEPSEEK RESPONSE FUNCTION --------------------

def get_deepseek_response(prompt, chat_history, model):
    """Get intelligent response from DeepSeek"""
    try:
        # Build conversation context
        context = ""
        for msg in chat_history[-6:]:  # Last 6 messages for context
            if isinstance(msg, HumanMessage):
                context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                context += f"Assistant: {msg.content}\n"
        
        # Get current time for context
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%A, %B %d, %Y")
        
        # Build full prompt with system instructions
        full_prompt = SYSTEM_PROMPT.format(
            current_time=current_time,
            current_date=current_date
        )
        full_prompt += f"\n\nPrevious conversation:\n{context}\n"
        full_prompt += f"User: {prompt}\n\n"
        full_prompt += "DecodeBot AI: Let me help you with that! "
        
        # Get response from DeepSeek
        response = model.invoke(full_prompt)
        return response.content
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}. Please check your API key and try again."


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
    ### 🤖 DecodeBot AI Help
    
    **💻 Coding Help:**
    - "Write a Python function to..."
    - "Explain this code: [code]"
    - "How do I [task] in JavaScript?"
    - "Debug my code: [code]"
    
    **📚 Learning:**
    - "Explain recursion with example"
    - "What is object-oriented programming?"
    - "Teach me data structures"
    
    **🎮 Commands:**
    - `weather` - Get weather info
    - `time` - Current time
    - `date` - Today's date
    - `about` - About DecodeBot AI
    - `clear` - Clear chat
    - `save` - Save chat
    
    **💬 General Chat:**
    - Ask me anything! I'm here to help.
    """

def get_about():
    return """
    ### 🤖 About DecodeBot AI
    
    **Version:** 2.0 (DeepSeek Powered)
    **Developer:** Sikandar 2026
    **Model:** DeepSeek R1 (via Groq)
    
    **Capabilities:**
    - ✅ Write and explain code
    - ✅ Debug errors
    - ✅ Teach programming concepts
    - ✅ Answer questions
    - ✅ Friendly conversations
    
    **Tech Stack:**
    - Python + Streamlit
    - LangChain + DeepSeek
    - Groq API for inference
    """


# -------------------- UTILS --------------------

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
    except Exception:
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


def load_lottie_animation(filename: str):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir) if base_dir.endswith("assets") else base_dir
        asset_path = os.path.join(project_root, "assets", "lottie", filename)
        if not os.path.exists(asset_path):
            return None
        with open(asset_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return None


# -------------------- MAIN CHAT UI --------------------

def render_main_chat_ui(chat_model):
    """Main UI layout with DeepSeek AI integration"""
    
    st.markdown(DARK_MODE_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-header">
        <h2 style="margin-bottom: 5px;">💬 DecodeBot AI Chat</h2>
        <p style="color: rgba(255,255,255,0.7);">Powered by DeepSeek R1 | Write Code | Get Explanations | Ask Anything</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Animation (if available)
    animation = load_lottie_animation(LOTTIE_PATH)
    if animation:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(animation, speed=0.8, loop=True, height=150, key="welcome")
    
    st.markdown("---")
    
    # Display chat history
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
    
    # Chat input
    prompt = st.chat_input("Ask me anything - write code, get explanations, or just chat...")
    
    if prompt:
        clean_prompt = prompt.strip()
        
        # Add user message
        st.session_state.chat_history.append(HumanMessage(content=clean_prompt))
        render_chat_bubble(clean_prompt, is_user=True)
        
        # Check for extra feature commands
        extra_response, handled = handle_extra_commands(clean_prompt)
        
        if handled:
            st.session_state.chat_history.append(AIMessage(content=extra_response))
            render_typing_indicator()
            time.sleep(0.5)
            render_chat_bubble(extra_response, is_user=False)
            save_to_history(st.session_state.chat_history)
        else:
            # Show typing animation
            render_typing_indicator()
            
            try:
                # Get response from DeepSeek
                response_text = get_deepseek_response(clean_prompt, st.session_state.chat_history, chat_model)
                
                st.session_state.chat_history.append(AIMessage(content=response_text))
                render_chat_bubble(response_text, is_user=False)
                save_to_history(st.session_state.chat_history)
                
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}. Please check your API key."
                st.session_state.chat_history.append(AIMessage(content=error_msg))
                render_chat_bubble(error_msg, is_user=False)
        
        st.rerun()


def render_bot(chat_model):
    """Main entry point for DecodeBot AI"""
    try:
        # Initialize session states
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Sidebar
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #4A90E2, #9013FE); display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 40px;">
                    🤖
                </div>
                <h3 style="margin-bottom: 5px;">DecodeBot AI</h3>
                <p style="color: rgba(255,255,255,0.6); font-size: 12px;">Powered by DeepSeek R1</p>
                <p style="color: rgba(255,255,255,0.4); font-size: 10px;">Created by Sikandar 2026</p>
                <hr style="margin: 15px 0;">
            </div>
            """, unsafe_allow_html=True)
            
            # Chat Controls
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
            
            # Features
            st.markdown("### ✨ What I Can Do")
            st.markdown("""
            - 📝 **Write Code** - "Write a Python function..."
            - 🔍 **Explain Code** - "Explain this code..."
            - 💡 **Solve Problems** - "How to reverse a string?"
            - 📚 **Teach Concepts** - "Explain recursion"
            - 🎯 **Debug Help** - "Fix my code"
            - 💬 **General Chat** - "Tell me a joke"
            """)
            
            st.markdown("---")
            
            # Status
            st.markdown("""
            <div style="margin-top: 20px; padding: 15px; background: rgba(74,144,226,0.1); border-radius: 12px;">
                <p style="font-size: 12px; margin: 0;">🔵 Status: <span style="color: #4A90E2;">Online</span></p>
                <p style="font-size: 12px; margin: 5px 0 0;">🧠 Model: DeepSeek R1</p>
                <p style="font-size: 12px; margin: 5px 0 0;">🎓 Created by Sikandar 2026</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Main content
        render_main_chat_ui(chat_model)
        
        # Footer
        st.markdown("""
        <div class="footer">
            © 2026 DecodeBot AI | Powered by DeepSeek R1 | Created by Sikandar 
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")
        st.exception(e)