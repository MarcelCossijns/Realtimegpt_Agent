import asyncio
from aiohttp import web
from .llm_interface import process_audio

def start_audio_server(hass):
    app = web.Application()

    async def handle_audio(request):
        audio_data = await request.content.read()
        response_audio = await process_audio(hass, audio_data)
        return web.Response(body=response_audio, content_type='audio/mpeg')

    app.router.add_post("/api/voice_agent/audio", handle_audio)
    runner = web.AppRunner(app)

    async def start():
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8765)
        await site.start()

    hass.loop.create_task(start())