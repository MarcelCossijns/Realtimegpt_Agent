import logging
import openai

_LOGGER = logging.getLogger(__name__)

def synthesize_speech(text: str, api_key: str):
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    return response.content  # MP3-Bytes

