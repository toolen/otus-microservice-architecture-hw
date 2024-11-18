import os
from typing import Dict, Optional, TypedDict, Union

from aiohttp import web

from hw.utils import UriAsDict, uri_to_dict


class Config(TypedDict):
    DATABASE: Optional[UriAsDict]


def get_config(override_config: Optional[Dict[str, str]] = None) -> Config:
    config = {"DATABASE": uri_to_dict(os.getenv("DATABASE"))}

    if override_config:
        config.update(override_config)

    return config


def init_config(
    app: web.Application, override_config: Optional[Dict[str, str]] = None
) -> None:
    """
    Initialize application configuration.

    :param app: application instance.
    :param override_config: dictionary that override config.
    :return: None
    """
    config = get_config(override_config)
    app["config"] = config
