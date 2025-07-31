import logging
import openai
from .audio_output import synthesize_speech

_LOGGER = logging.getLogger(__name__)

async def process_audio(audio_bytes, api_key: str):
    client = openai.OpenAI(api_key=api_key)
    _LOGGER.info("process_audio")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": audio_bytes}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "call_home_assistant",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "service": {"type": "string"},
                        "data": {"type": "object"}
                    },
                    "required": ["domain", "service"]
                }
            }
        }],
        tool_choice="auto"
    )

    tool_call = None
    if response.choices[0].tool_calls:
        tool_call = response.choices[0].tool_calls[0]

    reply_text = response.choices[0].message["content"]
    reply_audio = synthesize_speech(reply_text, api_key)

    return {
        "text": reply_text,
        "audio": reply_audio,
        "tool_call": tool_call
    }
