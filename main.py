import os
from dotenv import load_dotenv
import asyncio
import langchain
from groq import AsyncGroq
from groq import Groq as gr

load_dotenv()

async def main():
    client = AsyncGroq(api_key=os.environ.get("groq_api"))

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a master of coding in python a very helpful debugger."
            },
            {
                "role": "user",
                "content": "What are you?",
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        stop="Good Bye",
        stream=False,
    )
    print(chat_completion.choices[0].message.content)
asyncio.run(main())