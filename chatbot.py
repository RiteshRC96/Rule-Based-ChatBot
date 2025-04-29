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
        }

        # ✅ Updated model name to the supported one
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model="llama3-70b-8192"  # <--- Updated model name here
        )

        self.template = PromptTemplate.from_template(
            """You are a helpful AI assistant.
            Answer the following user query in a clear, friendly and accurate way.

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
