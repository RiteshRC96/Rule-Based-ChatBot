🤖 GenAI SmartBot with Sidebar (updatedBot Branch)

Welcome to the enhanced version of GenAI SmartBot, now with a feature-rich interface! This branch (updatedBot) includes a chat history sidebar and the ability to download your conversation.

✨ What's New in this Version

🗂️ Sidebar for viewing chat history

📄 Button to download full chat as a .txt file

👤 Avatars for user & bot

🎨 Custom styling with chat bubbles

🧪 Still supports pytest testing via test_chatbot.py

---


📂 Project Structure

.
├── chatbot.py             # Rule-based logic
├── test_chatbot.py        # Pytest unit tests
├── chatbot_app_sidebar.py # Streamlit chatbot with sidebar
├── static/
│   ├── user.png           # User avatar
│   └── bot.png            # Bot avatar
└── README.md              # You're here!

---


🚀 Getting Started

1. Switch to Updated Branch

git checkout updatedBot

2. Install Dependencies

pip install -r requirements.txt

3. Run the Enhanced Chatbot

streamlit run chatbot_app_sidebar.py

---


🧪 Run Unit Tests

pytest test_chatbot.py

---


📸 Live Demo

![Chatbot Demo](/static/chatbot_demo.gif)

---


🔄 Back to Basic Version

You can switch back to the clean UI (without sidebar) on the main branch:

git checkout main

---


📃 License

MIT License

---


👨‍💻 Author

Created by Your Name

