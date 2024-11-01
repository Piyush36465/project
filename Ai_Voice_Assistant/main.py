import speech_recognition as sr
import sounddevice as sd
import numpy as np
import os
import webbrowser
import openai
from config import apikey
import datetime

chatStr = ""

def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nAssistant: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"].strip()
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
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response["choices"][0]["text"]
        os.makedirs("Openai", exist_ok=True)  # Create directory if it doesn't exist
        file_name = ''.join(prompt.split(' ')[1:]).strip() or "default_prompt"
        with open(f"Openai/{file_name}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print("Error:", e)

def say(text):
    if os.name == 'posix':
        os.system(f'say "{text}"')  # For macOS
    elif os.name == 'nt':
        try:
            import pyttsx3  # For Windows
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except ImportError:
            print("Pyttsx3 library is required on Windows for text-to-speech.")
    else:
        print(text)  # Fallback for non-supported platforms

def takeCommand():
    r = sr.Recognizer()
    fs = 44100  # Sample rate
    duration = 5  # Duration of recording

    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()  # Wait until the recording is finished
    audio = np.int16(audio * 32767)  # Convert to 16-bit audio format
    audio_data = audio.tobytes()

    # Convert sounddevice audio to AudioData for recognition
    audio_data = sr.AudioData(audio_data, fs, 2)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio_data, language="en-in")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Network error."

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        query = takeCommand().lower()

        # Site-opening commands
        sites = {
            "youtube": "https://www.youtube.com",
            "wikipedia": "https://www.wikipedia.com",
            "google": "https://www.google.com",
            "Canva": "https://www.canva.com",
            "Udemy": 'https://www.udemy.com'
        }
        for site, url in sites.items():
            if f"open {site}" in query:
                say(f"Opening {site}")
                webbrowser.open(url)

        # Play specific song command
        if "play music" in query:
            musicPath = "/path/to/your/music/file.mp3"
            os.system(f"open '{musicPath}'")

        # Tell the current time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} hours and {minute} minutes.")

        # Open specific applications on Mac
        elif "open facetime" in query:
            os.system("open /System/Applications/FaceTime.app")
        elif "open pass" in query:
            os.system("open /Applications/Passkey.app")

        # AI response generation
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # Exit command
        elif "jarvis quit" in query:
            say("Goodbye!")
            break

        # Reset chat history
        elif "reset chat" in query:
            chatStr = ""
            say("Chat history reset.")

        # Default case to chat
        else:
            print("Chatting...")
            chat(query)
