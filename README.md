# Jarvis A.I. Assistant

Jarvis A.I. is a voice-activated personal assistant that integrates OpenAI's GPT-3 model for intelligent conversation and performs various tasks like opening websites, playing music, and providing the current time. It is designed to be cross-platform, with specific commands tailored for macOS and Windows.

---

## Features

1. **Voice Commands**:
   - Recognizes voice commands and performs tasks using `speech_recognition` and `sounddevice`.
   
2. **AI Chat Integration**:
   - Uses OpenAI's GPT-3 (text-davinci-003) to provide intelligent responses to queries.

3. **Task Automation**:
   - Opens popular websites (YouTube, Wikipedia, Google, etc.).
   - Launches system applications (e.g., FaceTime, Passkey on macOS).
   - Plays a music file.
   - Tells the current time.

4. **Custom AI Responses**:
   - Generates AI-based responses and saves them to text files for future reference.

5. **Control Commands**:
   - Reset chat history.
   - Quit the assistant.

---

## Installation

### Prerequisites

1. **Python 3.8+**: Ensure you have Python installed.
2. **Required Libraries**: Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
