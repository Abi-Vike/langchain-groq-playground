import streamlit as st
from groq import Groq
import json
import re
import logging
from logging.handlers import RotatingFileHandler


# Configure logging first
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
# Create a rotating file handler to manage log file size
handler = RotatingFileHandler('error_log-ai-calculator.txt', maxBytes=5*1024*1024, backupCount=2)  # 5MB per file, 2 backups
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)


# Access the API key from Streamlit's secrets
client = Groq(api_key=st.secrets["groq_api"])
MODEL = 'llama-3.1-70b-versatile'

def run_conversation(user_prompt):
    messages = [
        {"role": "system", "content": "You are an accurate calculator assistant. You answer strictly **only** to mathematical questions and decline any irrelevant questions. You always double check your work before showing the final result."},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model = MODEL,
            messages = messages,
            stream = False,
            temperature = 0.5,
            max_tokens = 4080
        )
        response_message = response.choices[0].message.content
        return response_message
    
        #nicely contained unreachable code down here - I don't need this for a while
        response_message = response.choices[0].message.content.strip()
        # Attempt to extract the numerical result using regex
        match = re.search(r"[-+]?\d*\.\d+|\d+", response_message)
        if match:
            result = match.group()
            return result
        else:
            # If no number is found, return a generic error message
            return "Could not parse the result. Please try again."

    except Groq.BadRequestError as e:
        # Log the error with user input to study user input behaviour
        logger.error(f"BadRequestError: {str(e)}\nTriggered by: {user_prompt}\n--------------")
        return "An error occurred: The input was not valid. Please limit your input to a valid mathematical expression."

    except Exception as e:
        # Log the error with user input to study user input behaviour
        logger.error(f"Unexpected error: {str(e)}\nTriggered by: {user_prompt}\n--------------")
        return "An unexpected error occurred. Please try again later."

# Streamlit UI
st.title("AI Calculator Chatbot")

user_prompt = st.text_input("You can use human language to ask your mathematical question:")

if st.button("Calculate"):
    if user_prompt:
        with st.spinner('Calculating...'):
            result = run_conversation(user_prompt)
        st.success(result)
    else:
        st.warning("Please enter an expression to calculate.")
