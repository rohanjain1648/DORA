import os
from dotenv import load_dotenv
import elevenlabs
from elevenlabs.client import ElevenLabs
import subprocess
import platform

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def play_audio(output_filepath):
    """Helper function to play audio files across different platforms"""
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Use the built-in Windows Media Player for MP3 files
            subprocess.run(['start', output_filepath], shell=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])  # Use mpg123 for MP3 support
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="ZF6FPAbjXT4488VcRRnw",
        model_id="eleven_multilingual_v2",
        output_format="mp3_22050_32",
    )
    elevenlabs.save(audio, output_filepath)
    play_audio(output_filepath)
    
from gtts import gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    play_audio(output_filepath)

# Test the functionality
if __name__ == "__main__":
    input_text = " This is a test for text to speech conversion"
    output_filepath = "test_text_to_speech.mp3"
    #text_to_speech_with_elevenlabs(input_text, output_filepath)
    text_to_speech_with_gtts(input_text, output_filepath)