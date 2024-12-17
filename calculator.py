import streamlit as st
# import os
# from dotenv import load_dotenv
from groq import Groq
import json

# Load environment variables only to use locally
# load_dotenv(dotenv_path="api-key.env")
client = Groq(api_key=st.secrets("groq_api"))
MODEL = 'llama3-8b-8192'

def calculate(expression):
    try:
        result = eval(expression)  # Consider replacing with a safer alternative
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})

def run_conversation(user_prompt):
    messages = [
        {"role": "system", "content": "You are a helpful calculator assistant."},
        {"role": "user", "content": user_prompt}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Calculates the mathematical expression provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "A mathematical expression to evaluate."
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=False,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {"calculate": calculate}
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(
                expression=function_args.get("expression")
            )

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })

        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        return second_response.choices[0].message.content

# Streamlit UI
st.title("Interactive Calculator Chatbot")

user_prompt = st.text_input("Enter your mathematical expression:")

if st.button("Calculate"):
    if user_prompt:
        result = run_conversation(user_prompt)
        st.write(result)
    else:
        st.warning("Please enter an expression to calculate.")
