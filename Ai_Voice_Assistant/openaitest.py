import os

import openai
from config import apikey
from main import say

chatStr = ""


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nAssistant: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chatStr}
            ],
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"].strip()
        say(answer)
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        print("Error:", e)
        return "I encountered an error. Please try again."


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"].strip()
        text += answer
        os.makedirs("Openai", exist_ok=True)
        file_name = ''.join(prompt.split(' ')[1:]).strip() or "default_prompt"
        with open(f"Openai/{file_name}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print("Error:", e)
