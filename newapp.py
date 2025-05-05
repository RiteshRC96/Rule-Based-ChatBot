import streamlit as st
import time
from chatbot import SmartChatBot
import base64

# Load avatars
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"

user_avatar = image_to_base64("static/user.png")
bot_avatar = image_to_base64("static/bot.png")

# Initialize bot
groq_api_key = "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"
bot = SmartChatBot(groq_api_key)

# Page config
st.set_page_config(page_title="GenAI SmartBot", page_icon="🤖", layout="wide")
st.title("🤖 Rule Based Chat Bot")

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
st.sidebar.title("📚 Chat History")
with st.sidebar:
    for sender, message in st.session_state.messages:
        st.markdown(f"**{'You' if sender == 'user' else 'Bot'}:** {message[:150]}{'...' if len(message) > 150 else ''}")
    
    if st.button("📄 Download Chat"):
        chat_content = "\n".join([f"{'You' if m[0] == 'user' else 'Bot'}: {m[1]}" for m in st.session_state.messages])
        st.download_button("Download", chat_content, "chat_history.txt")

# --- Main Chat ---
def render_message(sender, message):
    st.markdown(f"""
    <div style='display:flex; justify-content:{"flex-end" if sender == "user" else "flex-start"}; margin-bottom:10px;'>
        <div style='background:{"#90EE90" if sender == "user" else "#FFB6C1"}; padding:10px; border-radius:18px; max-width:70%; display:flex; align-items:center;'>
            <img src='{user_avatar if sender == "user" else bot_avatar}' style='width:30px; height:30px; border-radius:50%; margin-right:10px;'>
            <div style='word-break:break-word;'>{message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Ultra-fast typing effect (5x faster)
def fast_typing_effect(response):
    placeholder = st.empty()
    full_text = ""
    
    # Type 5 characters at a time with minimal delay
    for i in range(0, len(response), 5):
        full_text += response[i:i+5]
        placeholder.markdown(f"""
        <div style='display:flex; justify-content:flex-start; margin-bottom:10px;'>
            <div style='background:#FFB6C1; padding:10px; border-radius:18px; max-width:70%; display:flex; align-items:center;'>
                <img src='{bot_avatar}' style='width:30px; height:30px; border-radius:50%; margin-right:10px;'>
                <div style='word-break:break-word;'>{full_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)  # Reduced from 0.03 to 0.02
    
    return full_text

# Handle chat input
if user_input := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append(("user", user_input))
    
    # Display all previous messages
    for sender, message in st.session_state.messages[:-1]:
        render_message(sender, message)
    
    # Display user's new message
    render_message("user", user_input)
    
    # Get and display bot response (with fast typing)
    bot_response = bot.get_response(user_input)
    final_response = fast_typing_effect(bot_response)
    st.session_state.messages.append(("bot", final_response))
    
    # Auto-scroll to bottom
    st.markdown("<script>window.parent.document.querySelector('section.main').scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

# Display all messages when no new input
else:
    for sender, message in st.session_state.messages:
        render_message(sender, message)
