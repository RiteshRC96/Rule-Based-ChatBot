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
groq_api_key = st.secrets["GROQ_API_KEY"]
bot = SmartChatBot(groq_api_key)

# Streamlit page config
st.set_page_config(page_title="GenAI SmartBot", page_icon="🤖", layout="wide")
st.title("🤖 GenAI SmartBot - Powered by Groq")

# Sidebar
st.sidebar.title("📚 Chat History")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar download button
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

# Sidebar chat history
for sender, message in st.session_state.messages:
    sender_name = "You" if sender == "user" else "Bot"
    st.sidebar.markdown(f"**{sender_name}:** {message}")

# Main chat area
st.markdown("### 💬 Chat below:")

# User input at bottom (Streamlit handles this natively with st.chat_input)
user_input = st.chat_input("Type your message here...")

# Function to render one message
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

# Handle input
if user_input:
    # Save user's message to session
    st.session_state.messages.append(("user", user_input))

    # Render all previous messages
    for sender, message in st.session_state.messages[:-1]:
        render_message(sender, message)

    # Render new user message
    render_message("user", user_input)

    # Bot thinking...
    with st.spinner("Bot is typing..."):
        bot_response = bot.get_response(user_input)

        # Optimized typing effect
        bot_message_placeholder = st.empty()
        batch_size = 5
        delay = 0.013

        for i in range(0, len(bot_response), batch_size):
            typed_text = bot_response[:i + batch_size]
            bot_message_placeholder.markdown(
                f'''
                <div style="display:flex; justify-content:flex-start; margin-right:auto; margin-bottom:10px;">
                    <div style="background-color:#e0f7fa; padding:10px 14px; border-radius:18px; max-width:75%; display:flex; align-items:center;">
                        <img src="{bot_avatar}" style="width:30px;height:30px;border-radius:50%; margin-right:10px;"/>
                        <span style="color:#000; word-wrap:break-word;">{typed_text}</span>
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
            time.sleep(delay)

        # Save final bot message
        st.session_state.messages.append(("bot", bot_response))

else:
    # No new input: display full history
    for sender, message in st.session_state.messages:
        render_message(sender, message)
