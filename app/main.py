import os
import logging
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.nlp import process_text
from app.database import save_interaction
from gtts import gTTS

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure 'audio' directory exists
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Mount static directory for serving audio files
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# Logging setup
logging.basicConfig(filename="logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Input model
class VoiceInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Voice Assistant API"}

@app.post("/process-voice")
async def process_voice(input_data: VoiceInput):
    try:
        user_text = input_data.text.strip().lower()
        if not user_text:
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")

        # Process text with NLP function
        response = process_text(user_text)

        response_text = response.get("response_text", "") if isinstance(response, dict) else response
        if not response_text:
            raise HTTPException(status_code=500, detail="Invalid response text.")

        # Log interaction
        logging.info(f"User: {user_text} | Response: {response_text}")

        # Save interaction to database
        await save_interaction(user_text, response_text)

        # Generate a unique filename
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)

        # Convert text to speech
        tts = gTTS(response_text, lang="en")
        tts.save(audio_path)

        # Verify file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=500, detail="Audio file was not saved correctly.")

        return {
            "response_text": response_text,
            "audio_file": f"http://127.0.0.1:8000/audio/{audio_filename}"  # ✅ Corrected URL
        }

    except Exception as e:
        logging.error(f"Error processing voice input: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """ Serves generated MP3 files correctly. """
    file_path = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return FileResponse(file_path, media_type="audio/mpeg")
