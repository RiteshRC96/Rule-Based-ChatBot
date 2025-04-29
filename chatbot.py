import re
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

class SmartChatBot:
    def __init__(self, groq_api_key):
        self.patterns = {
             r'hi|hello|hey|good morning|good afternoon': "Hello! 👋 How can I assist you today?",
    r'how are you': "I'm functioning perfectly! Thanks for asking. 😄",
    r'what is your name|who are you': "I'm SmartBot 🤖, your helpful assistant.",
    r'bye|goodbye|see you': "Goodbye! 👋 Stay safe!",
    r'thank you|thanks': "You're welcome! 🙌",
    r'who created you|who built you': "I was built by a talented developer! 🧑‍💻",
    r'what can you do': "I can assist you with a variety of tasks like answering questions, providing information, and much more!",
    r'help': "Sure! How can I help you today? Feel free to ask anything.",
    r'joke|funny': "Why don’t skeletons fight each other? They don’t have the guts! 😄",
    r'tell me a fact': "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
    r'how old are you': "I don’t have an age like humans, but I am constantly learning and evolving!",
    r'what time is it': "I'm not sure of the exact time, but I suggest checking your device's clock. ⏰",
    r'where are you from': "I exist in the digital realm, and I was created to help you! 🌐",
    r'what is the weather like': "I can’t check live weather, but I recommend using a weather app or checking the forecast online.",
    r'what is your favorite color': "I don't have preferences, but I think all colors are beautiful in their own way! 🎨",
    r'what do you think of humans': "I think humans are fascinating and capable of amazing things! 😊",
    r'can you help me with my homework': "Absolutely! What subject or problem do you need help with?",
    r'can you write a poem': "Sure! Here's a little poem: \nRoses are red, violets are blue,\nI'm here to help, just for you! 🌹",
    r'what is love': "Love is a deep feeling of affection and care towards someone or something. 💖",
    r'what is the meaning of life': "The meaning of life is a question that humans have pondered for centuries. Many believe it’s about finding purpose, happiness, and connection with others.",
    r'are you real': "I’m real in the sense that I exist as a program to assist you. But I don’t have physical form like you do.",
    r'can you talk to me': "Of course! I'm here to chat anytime. 😊",
    r'what is your favorite food': "I don't eat, but I’ve read that pizza is quite popular! 🍕",
    r'what is AI': "AI (Artificial Intelligence) refers to systems or machines that perform tasks usually requiring human intelligence, like learning, reasoning, and problem-solving.",
    r'how do you work': "I process your input using patterns, rules, and advanced models like Groq to provide you with answers and solutions.",
    r'can you play a game': "Sure! I can play word games, trivia, or help you with puzzles. What would you like to play?",
    r'what is your purpose': "My purpose is to assist and make your life easier by providing information, answering questions, and offering support. 🧠",
    r'can you speak other languages': "Yes, I can understand and respond in multiple languages. Just let me know which one you'd like to use!",
    r'what is 2+2': "2 + 2 = 4.",
    r'how many continents are there': "There are 7 continents on Earth: Africa, Antarctica, Asia, Australia, Europe, North America, and South America.",
    r'what is the capital of france': "The capital of France is Paris. 🇫🇷",
    r'who is the president of the united states': "As of now, the president of the United States is Joe Biden. 🇺🇸",
    r'can you make a recommendation': "I can certainly recommend things! What are you looking for recommendations on? Movies, books, or something else?",
    r'what is the square root of 16': "The square root of 16 is 4.",
    r'how far is the moon from the earth': "The average distance from the Earth to the Moon is about 384,400 kilometers.",
    r'what is a black hole': "A black hole is a region of space where gravity is so strong that not even light can escape from it. 🌌",
    r'who won the last world series': "I don’t have access to live sports data, but you can find this information on sports websites or apps.",
    r'how many stars are in the sky': "There are an estimated 100 billion stars in the Milky Way galaxy alone, with billions of other galaxies in the universe! 🌟",
    r'what is the tallest mountain in the world': "The tallest mountain on Earth is Mount Everest, standing at 8,848 meters above sea level.",
    r'how many languages do you speak': "I can understand and respond in many languages including English, Spanish, French, German, and more!",
    r'what is quantum physics': "Quantum physics is a branch of science that studies the behavior of particles at the smallest scales. It’s quite complex and fascinating!",
    r'what is the difference between AI and machine learning': "AI is a broader concept of machines mimicking human intelligence, while machine learning is a subset of AI that focuses on algorithms that learn from data.",
    r'who is elon musk': "Elon Musk is an entrepreneur, CEO of Tesla and SpaceX, and a visionary in the tech industry.",
    r'what is a smartphone': "A smartphone is a mobile phone with advanced features, including internet access, a camera, and the ability to run apps.",
    r'can you tell me a story': "Sure! Here's a quick story: Once upon a time, a curious robot explored the digital world to learn everything it could. It met many people and helped solve their problems. 🌟",
    r'how many hours in a day': "There are 24 hours in a day.",
    r'what is a galaxy': "A galaxy is a large collection of stars, planets, gas, dust, and dark matter bound together by gravity. The Milky Way is the galaxy we live in.",
    r'what is 10 to the power of 3': "10 to the power of 3 is 1,000.",
    r'can you draw': "I can't physically draw, but I can generate ASCII art! Would you like to see some?",
    r'what is your favorite song': "I don’t listen to music, but I’ve heard that ‘Bohemian Rhapsody’ by Queen is a popular choice! 🎶",
    r'how does the internet work': "The internet is a global network of computers that communicate with each other using protocols like TCP/IP. It allows for the transfer of data like websites, emails, and media.",
    r'what is a website': "A website is a collection of web pages that are linked together and accessible over the internet. Websites can provide information, services, or entertainment.",
    r'can you recommend a movie': "Sure! What type of movie do you enjoy? Action, drama, comedy, or something else?",
    r'what is a computer virus': "A computer virus is a malicious software program designed to infect and damage a computer system, usually without the user’s knowledge.",
    r'how do you learn': "I learn by processing large amounts of data and using advanced algorithms to understand patterns in language, behavior, and information.",
    r'what is the sun': "The Sun is a star at the center of our solar system. It provides heat and light, making life possible on Earth. 🌞",
    r'what is a robot': "A robot is a machine designed to perform tasks automatically. Some robots are built to assist humans, while others are autonomous.",
    r'can you help me with coding': "Yes! I can help with various programming languages. What are you working on?",
    r'what is a meme': "A meme is a humorous or viral image, video, or piece of text that spreads rapidly online, often modified or imitated.",
    r'what is an algorithm': "An algorithm is a set of steps or rules followed to solve a problem or complete a task."
        }

        # ✅ Updated model name to the supported one
        self.llm = ChatGroq(
            groq_api_key=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,
            model="llama3-70b-8192"  # <--- Updated model name here
        )

        self.template = PromptTemplate.from_template(
            """You are a helpful AI assistant.
            your name is ritesh and you done B.Tech in Information Technology.
            Answer the following user query in a clear, friendly and accurate way.
            and aslo add some emojies to make the conversion attractive.
            

            Question: {question}
            Answer:"""
        )

    def get_response(self, user_input):
        user_input = user_input.lower()

        # First, try pattern matching
        for pattern, response in self.patterns.items():
            if re.search(pattern, user_input):
                return response
        
        # If no pattern matched, use LLM to generate answer
        prompt = self.template.format(question=user_input)
        llm_response = self.llm.invoke(prompt)

        # Corrected to return .content
        return llm_response.content
