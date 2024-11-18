from typing import Optional

import aiopg.sa
from aiohttp import web
from sqlalchemy import Column, Integer, MetaData, String, Table

from hw.utils import UriAsDict

meta = MetaData()

users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(254), nullable=False),
    Column("last_name", String(254), nullable=False),
)


async def close_db(app: web.Application) -> None:
    """
    Close connection with database.

    :param app: application instance.
    :return: None
    """
    db = app["db"]
    db.close()
    await db.wait_closed()


async def init_db(app: web.Application):
    conf: Optional[UriAsDict] = app["config"]["DATABASE"]
    if not conf:
        raise Exception

    engine = await aiopg.sa.create_engine(
        database=conf["DBNAME"],
        user=conf["USER"],
        password=conf["PASSWORD"],
        host=conf["HOST"],
        port=conf["PORT"],
    )
    app["db"] = engine

    app.on_cleanup.append(close_db)
