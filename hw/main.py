import argparse
import asyncio
import logging
import sys
from typing import Optional

from aiohttp import web

from hw.config import Config, init_config
from hw.db import init_db
from hw.routes import init_routes

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", default=8080, type=int)


def init_logging(app: web.Application) -> None:
    """
    Initialize application logging.

    :param app: application instance.
    :return: None
    """
    log_level = app["config"]["LOG_LEVEL"]
    logging.basicConfig(
        level=log_level,
        format="[%(levelname)s %(asctime)s %(name)s] %(message)s",
        stream=sys.stdout,
    )


def init_app(config: Optional[Config] = None) -> web.Application:
    """
    Initialize application.

    :param config: dictionary.
    :return: application instance.
    """
    app = web.Application()

    init_config(app, override_config=config)
    init_logging(app)
    init_db(app)
    init_routes(app)

    return app


def main() -> None:
    """
    Run application.

    :return: None
    """
    app = init_app()
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    web.run_app(app, loop=loop, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
