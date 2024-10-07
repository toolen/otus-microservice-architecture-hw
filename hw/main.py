import uuid
from aiohttp import web

async def index(request):
    text = uuid.uuid4().hex
    return web.Response(text=text)


async def health(request):
    data = { "status": "OK" }
    return web.json_response(data)


async def create_app():
    app = web.Application()
    app.add_routes(
        [
            web.get('/', index),
            web.get('/health', health)
        ]
    )
    return app
