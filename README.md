# 🤖 GenAI SmartBot (Main Branch)

Welcome to **GenAI SmartBot**, a simple and efficient **rule-based chatbot** built with Python and Streamlit. This version represents the **core chatbot** **without sidebar enhancements**—ideal for those looking for a minimalistic, clean chat interface.

---

## 🚀 Features

- 🎯 Rule-based chatbot logic (via `chatbot.py`)
- 🧠 Responds to predefined patterns using regex
- 💬 Modern UI with avatars for user and bot
- ⚡ Fast and interactive using Streamlit's `chat_input`
- 🧪 Unit testing support via `pytest` in `test_chatbot.py`

---

## 📂 Project Structure

```bash
.
├── chatbot.py           # Rule-based logic for SmartBot
├── test_chatbot.py      # Pytest file to test chatbot responses
├── chatbot_app.py       # Streamlit app (without sidebar)
├── static/
│   ├── user.png         # Avatar for user
│   └── bot.png          # Avatar for bot
└── README.md            # You're here!
```

---

## 🛠️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/genai-smartbot.git
cd genai-smartbot
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Chatbot (Main Version)

```bash
streamlit run chatbot_app.py
```

---

## 🧪 Run Tests

```bash
pytest test_chatbot.py
```

---

## 🖼️ Demo
![Chatbot Demo](/static/chatbot_demo.gif)
---

## 🌱 Check Enhanced Version

> A more feature-rich version is available in the `updatedBot` branch, which includes a chat history sidebar and download functionality.

```bash
git checkout updatedBot
```

---

## 📃 License

MIT License - use freely, modify respectfully!

---

## 👨‍💻 Author

Built with ❤️ by [Ritesh Chougule](https://github.com/RiteshRC96)

