from aiohttp import web


async def health_handler(request: web.Request) -> web.Response:
    """
    Return healthcheck response.

    :return: Response
    """
    return web.json_response({"health": "ok"})
