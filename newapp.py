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

# Page config
st.set_page_config(page_title="GenAI SmartBot", page_icon="🤖", layout="wide")
st.title("🤖 Rule Based Chat Bot")

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# === Sidebar for chat history & download ===
st.sidebar.title("📚 Chat History")

# Display chat history in sidebar with scrollable container
with st.sidebar:
    history_container = st.container()
    with history_container:
        for sender, message in st.session_state.messages:
            sender_name = "You" if sender == "user" else "Bot"
            st.markdown(f"**{sender_name}:** {message[:200]}...")  # Show preview in sidebar

# Download chat as .txt
if st.sidebar.button("📄 Generate Chat File"):
    chat_content = ""
    for sender, message in st.session_state.messages:
        sender_name = "You" if sender == "user" else "Bot"
        chat_content += f"{sender_name}: {message}\n\n"
    st.sidebar.download_button(
        label="Download Chat",
        data=chat_content,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Chat area
st.markdown("### 💬 Chat below:")

# Function to render a message with better handling of long content
def render_message(sender, message):
    avatar = user_avatar if sender == "user" else bot_avatar
    bg_color = "#90EE90" if sender == "user" else "#FFB6C1"
    align = "flex-end" if sender == "user" else "flex-start"
    margin = "margin-left:auto;" if sender == "user" else "margin-right:auto;"
    max_width = "60%" if sender == "user" else "75%"

    # Split long messages into paragraphs
    paragraphs = message.split('\n')
    
    st.markdown(
        f'''
        <div style="display:flex; justify-content:{align}; {margin} margin-bottom:10px;">
            <div style="background-color:{bg_color}; padding:10px 14px; border-radius:18px; max-width:{max_width}; display:flex; align-items:flex-start;">
                <img src="{avatar}" style="width:30px;height:30px;border-radius:50%; margin-right:10px; flex-shrink:0;"/>
                <div style="color:#000; word-wrap:break-word; white-space:pre-wrap;">
        ''', unsafe_allow_html=True
    )
    
    for para in paragraphs:
        if para.strip():  # Only display non-empty paragraphs
            st.markdown(para, unsafe_allow_html=True)
    
    st.markdown(
        '''
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

# Function to display typing effect for bot response with chunking
def display_typing_effect(bot_response, delay=0.01):
    bot_placeholder = st.empty()
    typed_text = ""
    
    # Split response into chunks for smoother typing effect
    chunks = [bot_response[i:i+50] for i in range(0, len(bot_response), 50)]
    
    for chunk in chunks:
        for char in chunk:
            typed_text += char
            bot_placeholder.markdown(
                f'''
                <div style="background-color:#FFB6C1; padding:10px 14px; border-radius:18px; margin-bottom:10px; max-width:75%; display:flex; align-items:flex-start;">
                    <img src="{bot_avatar}" style="width:30px;height:30px;border-radius:50%; margin-right:10px; flex-shrink:0;"/>
                    <div style="color:#000; word-wrap:break-word; white-space:pre-wrap;">{typed_text}</div>
                </div>
                ''', unsafe_allow_html=True
            )
            time.sleep(delay)
    
    return typed_text

# Handle chat
if user_input := st.chat_input("Type your message here..."):
    # Save user message
    st.session_state.messages.append(("user", user_input))

    # Clear and re-render all messages to maintain state
    st.empty()  # Clear previous content
    
    # Render all messages including the new one
    for sender, message in st.session_state.messages[:-1]:
        render_message(sender, message)
    
    # Render user's new message
    render_message("user", user_input)
    
    # Get and display bot response with typing effect
    bot_response = bot.get_response(user_input)
    full_response = display_typing_effect(bot_response)
    
    # Save bot response
    st.session_state.messages.append(("bot", full_response))
    
    # Scroll to bottom (JavaScript injection)
    st.markdown(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
        </script>
        """,
        unsafe_allow_html=True
    )
else:
    # No new input: show all messages
    for sender, message in st.session_state.messages:
        render_message(sender, message)
    
    # Scroll to bottom if there are messages
    if st.session_state.messages:
        st.markdown(
            """
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
            </script>
            """,
            unsafe_allow_html=True
        )

# Add some CSS to make the chat area scrollable
st.markdown(
    """
    <style>
        .main .block-container {
            max-height: 70vh;
            overflow-y: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)
