import streamlit as st
import time
from chatbot import SmartChatBot
import base64

# Load avatars
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

user_avatar = image_to_base64("static/user.png")
bot_avatar = image_to_base64("static/bot.png")

# Initialize bot
groq_api_key = "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"
bot = SmartChatBot(groq_api_key)

# Streamlit config
st.set_page_config(page_title="GenAI SmartBot", page_icon="🤖", layout="wide")
st.title("🤖 Rule Based Chat Bot")

# Sidebar
st.sidebar.title("📚 Chat History")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Download chat
if st.sidebar.button("📄 Generate Chat File"):
    chat_content = ""
    for sender, message in st.session_state.messages:
        sender_name = "You" if sender == "user" else "Bot"
        chat_content += f"{sender_name}: {message}\n"
    st.sidebar.download_button(
        label="Download Chat",
        data=chat_content,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Display chat in sidebar
for sender, message in st.session_state.messages:
    sender_name = "You" if sender == "user" else "Bot"
    st.sidebar.markdown(f"**{sender_name}:** {message}")

st.markdown("### 💬 Chat below:")

# Render a single message
def render_message(sender, message):
    avatar = user_avatar if sender == "user" else bot_avatar
    bg_color = "#90EE90" if sender == "user" else "#FFB6C1"
    align = "flex-end" if sender == "user" else "flex-start"
    margin = "margin-left:auto;" if sender == "user" else "margin-right:auto;"
    max_width = "60%" if sender == "user" else "75%"

    st.markdown(
        f'''
        <div style="display:flex; justify-content:{align}; {margin} margin-bottom:10px;">
            <div style="background-color:{bg_color}; padding:10px 14px; border-radius:18px; max-width:{max_width}; display:flex; align-items:center;">
                <img src="{avatar}" style="width:30px;height:30px;border-radius:50%; margin-right:10px;"/>
                <span style="color:#000; word-wrap:break-word;">{message}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

# Typing effect
def display_typing_effect(message):
    avatar = bot_avatar
    placeholder = st.empty()
    typed_text = ""
    for char in message:
        typed_text += char
        placeholder.markdown(
            f'''
            <div style="display:flex; justify-content:flex-start; margin-right:auto; margin-bottom:10px;">
                <div style="background-color:#FFB6C1; padding:10px 14px; border-radius:18px; max-width:75%; display:flex; align-items:center;">
                    <img src="{avatar}" style="width:30px;height:30px;border-radius:50%; margin-right:10px;"/>
                    <span style="color:#000; word-wrap:break-word;">{typed_text}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True
        )
        time.sleep(0.02)

# Chat input
user_input = st.chat_input("Type your message here...")

# Handle new input
if user_input:
    st.session_state.messages.append(("user", user_input))
    render_message("user", user_input)

    with st.spinner("Bot is typing..."):
        bot_response = bot.get_response(user_input)
        display_typing_effect(bot_response)
        st.session_state.messages.append(("bot", bot_response))
else:
    # Display entire history (no new input)
    for sender, message in st.session_state.messages:
        render_message(sender, message)
