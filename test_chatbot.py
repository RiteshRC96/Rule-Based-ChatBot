import pytest
from chatbot import SimpleChatBot

# Initialize bot instance for all tests
@pytest.fixture
def bot():
    return SimpleChatBot()

# Test known pattern matches
@pytest.mark.parametrize("user_input, expected_response", [
    ("Hello", "Hello! 👋 How can I assist you today?"),
    ("What is your name?", "I'm SimpleBot 🤖, your helpful assistant."),
    ("How are you?", "I'm functioning perfectly! Thanks for asking. 😄"),
    ("bye", "Goodbye! 👋 Stay safe!"),
    ("Thanks", "You're welcome! 🙌"),
    ("Who created you?", "I was built by a talented developer! 🧑‍💻"),
    ("What is AI?", "AI stands for Artificial Intelligence — where machines learn to act smart like humans! 🤖"),
])
def test_pattern_matching(bot, user_input, expected_response):
    assert bot.get_response(user_input) == expected_response

# Test fallback response for unknown input
def test_fallback_response(bot):
    unknown_input = "Tell me a joke"
    response = bot.get_response(unknown_input)
    assert response in bot.fallback_responses

# Test empty input (should fallback too)
def test_empty_input(bot):
    empty_input = ""
    response = bot.get_response(empty_input)
    assert response in bot.fallback_responses

# Test completely random input
def test_random_input(bot):
    random_input = "asdkj1231!@#"
    response = bot.get_response(random_input)
    assert response in bot.fallback_responses
