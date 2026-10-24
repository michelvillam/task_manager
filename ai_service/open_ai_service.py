import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))


def create_task_with_ai(name, description):
    prompt = f"Create a task with the following details:\nName: {name}\nDescription: {description}\n"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()  

