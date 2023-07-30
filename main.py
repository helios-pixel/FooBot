import textbase
from textbase.message import Message
from textbase import models
import os,random
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Set the new name for the bot
BOT_NAME = "Foo-Bot"

# Prompt for GPT-3.5 Turbo with the new bot name
SYSTEM_PROMPT = f"""You are chatting with {BOT_NAME}. There are no specific prefixes for responses, so you can ask or talk about anything you like. {BOT_NAME} will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""
TRIVIA_QUESTIONS = [
    {
        "question": "What is the main ingredient in guacamole?",
        "answer": "Avocado",
    },
    {
        "question": "Which spice is made from the dried stigma of a flower and is one of the most expensive spices by weight?",
        "answer": "Saffron",
    },
    {
        "question": "What is the Italian word for 'cooked al dente' pasta, meaning it is firm to the bite?",
        "answer": "Pasta",
    },
    {
        "question": "What is the primary ingredient in traditional Japanese miso soup?",
        "answer": "Miso paste",
    },
    {
        "question": "What is the national dish of Spain, consisting of rice, saffron, and various ingredients like seafood, chicken, or vegetables?",
        "answer": "Paella",
    },
    # Add more questions as needed...
]

RECOMMENDED_PAIRINGS = {
    "pasta": "For that dish, I'd recommend trying a side of garlic bread and a glass of red wine.",
    "steak": "For that dish, I'd recommend trying mashed potatoes and a crisp salad.",
    "sushi": "For that dish, I'd recommend trying miso soup and green tea.",
    # Add more pairings as needed...
}

@textbase.chatbot("foodie-adventure-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    # Initialize state if not present
    if state is None:
        state = {}

    # Extract the latest user message
    if message_history:
        user_message = message_history[-1].content.lower()
    else:
        user_message = ""

    # Check if the user input contains keywords to trigger specific actions
    if "location" in user_message or "nearby" in user_message or "restaurants near me" in user_message or "food places close by" in user_message or "local restaurants" in user_message:
        bot_response = "Great! What city are you in? I'll find some nearby restaurants for you."
    elif "features" in user_message:
       bot_response = f"""
        I can help you in various ways, like:\n
        1. I can help you find the location of nearby restaurants to you.\n
        2. Recommend dishes from the cuisine you like.\n
        3. Recommend dishes from some restaurants.\n
        4. Take you on a food adventure to explore new delicacies.\n
        5. Give you recipes for make-at-home food.\n
        6. Recommend sides for your dish or what goes good with it.\n
        7. Too bored? Let's test out your foodie knowledge!\n
        """
    elif "cuisine" in user_message:
        bot_response = "Excellent choice! What type of cuisine are you in the mood for? You can say 'Italian,' 'Mexican,' 'Chinese,' etc."
    elif "restaurant" in user_message or "dishes in restaurant" in user_message or "":
        bot_response = "Sure, let me know the name of the restaurant, and I'll recommend some dishes for you."
    elif "adventure" in user_message or "something new" in user_message:
        bot_response = "Ready for a food adventure? Tell me your preferences, like trying new cuisines or exploring desserts!"
    elif "recipe" in user_message:
        bot_response = "Feel like cooking at home? Let me know your favorite dish, and I'll share a recipe with you."
    elif "what goes well with" in user_message:
        # Check for the dish name in the user's message and provide recommended pairings
        for dish, pairing in RECOMMENDED_PAIRINGS.items():
            if dish in user_message:
                bot_response = pairing
                break
        else:
            # If the user's message doesn't match any specific dish, use a default response
            bot_response = "I'm not sure what dish you're referring to. Could you be more specific?"
    elif "trivia" in user_message or "play a game" in user_message:
            # Trigger the trivia game
            trivia_question = state.get("trivia_question")
            if trivia_question:
                # Check the user's answer against the correct answer
                correct_answer = trivia_question["answer"]
                user_answer = user_message.strip()
                if user_answer == correct_answer:
                    state["score"] = state.get("score", 0) + 1
                    bot_response = "Correct! You got it right."
                else:
                    bot_response = f"Sorry, that's incorrect. The correct answer is: {correct_answer}"
            else:
                # Start the trivia game
                trivia_question = random.choice(TRIVIA_QUESTIONS)
                state["trivia_question"] = trivia_question
                bot_response = f"Let's play a trivia game!\n\n{trivia_question['question']}"
    else:
        # If the user's message doesn't match any specific condition, use the GPT-3.5 Turbo model for a generic response.
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    return bot_response, state
