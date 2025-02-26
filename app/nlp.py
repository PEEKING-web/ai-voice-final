import google.generativeai as genai
import os
import logging
import uuid
import re
from dotenv import load_dotenv
from gtts import gTTS

# Load API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Directory for storing audio files
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def clean_text(text):
    """Removes special characters, Markdown symbols, and extra spaces."""
    text = re.sub(r'[*_~`<>|]', '', text)  # Remove asterisks, underscores, tildes, etc.
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces and newlines
    return text

def process_text(text):
    """Processes user input and generates a response with TTS."""
    logging.info(f"Received input text: {text}")

    # Predefined responses
    keywords = {
        "hello": "Hi there! How can I assist you?",
        "weather": "I can check the weather for you.",
        "news": "Here are some recent news updates.",
        "time": "I can tell you the current time if you need.",
        "date": "I can provide today's date.",
        "help": "I can assist you with various tasks like answering questions or providing recommendations."
    }

    # Check for predefined responses
    for key, response in keywords.items():
        if key in text.lower():
            logging.info(f"Matched keyword '{key}', responding with: {response}")
            return generate_voice_response(response)

    # Use Gemini AI for other queries
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(text)
        ai_response = clean_text(response.text)  # CLEAN TEXT before TTS

        logging.info(f"Gemini API Response (cleaned): {ai_response}")

    except Exception as e:
        ai_response = "I'm not sure how to respond to that."
        logging.error(f"Error calling Gemini API: {e}")

    return generate_voice_response(ai_response)

def generate_voice_response(text):
    """Converts cleaned text to speech using gTTS and saves it as an audio file."""
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    try:
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)

        logging.info(f"Generated voice response: {text}")

        return {"response_text": text, "audio_file": f"/audio/{audio_filename}"}
    
    except Exception as e:
        logging.error(f"Error generating voice response: {e}")
        return {"response_text": "Error generating voice response.", "audio_file": None}
