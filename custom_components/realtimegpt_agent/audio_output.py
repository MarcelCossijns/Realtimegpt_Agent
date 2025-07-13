import openai

def synthesize_speech(text):
    client = openai.OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    return response.content  # MP3-Bytes
