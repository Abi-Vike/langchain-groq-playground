import streamlit as st
from groq import Groq
import json
import ast

# Access the API key from Streamlit's secrets
client = Groq(api_key=st.secrets["groq_api"])
MODEL = 'llama3-8b-8192'

def calculate(expression):
    try:
        # Safely evaluate arithmetic expressions
        result = ast.literal_eval(expression)
        return json.dumps({"result": result})
    except Exception:
        return json.dumps({"error": "Invalid expression"})

def run_conversation(user_prompt):
    messages = [
        {"role": "system", "content": "You are a helpful calculator assistant."},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=False,
        max_tokens=4096
    )

    response_message = response.choices[0].message.content
    return response_message


# Streamlit UI
st.title("Interactive AI Calculator Chatbot")

user_prompt = st.text_input("You can use human language to ask your mathematical question:")

if st.button("Calculate"):
    if user_prompt:
        result = run_conversation(user_prompt)
        st.write(result)
    else:
        st.warning("Please enter a mathematical expression to calculate.")
