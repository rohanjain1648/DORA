import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables at the start
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Function to record audio from the microphone and save it as an MP3 file.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
            return True

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False

def transcribe_with_groq(audio_filepath):
    """
    Transcribe audio file using Groq API.
    """
    if not os.path.exists(audio_filepath):
        raise FileNotFoundError(f"Audio file not found: {audio_filepath}")
        
    client = Groq(api_key=GROQ_API_KEY)
    stt_model = "whisper-large-v3"
    
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

if __name__ == "__main__":
    audio_filepath = "test_speech_to_text.mp3"
    
    # First record the audio
    if record_audio(audio_filepath):
        # Then transcribe it
        try:
            transcription = transcribe_with_groq(audio_filepath)
            print("Transcription:", transcription)
        except Exception as e:
            print(f"Error during transcription: {e}")
    else:
        print("Failed to record audio")