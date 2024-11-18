from aiohttp import web


async def list_users(request: web.Request) -> web.Response:
    db = request.app["db"]
    async with db.acquire() as conn:
        cursor = await conn.execute(db.users.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        return web.json_response(users)


async def create_user(request: web.Request) -> web.Response:
    data = await request.json()
    db = request.app["db"]
    async with db.acquire() as conn:
        cursor = await conn.execute(db.users.insert().values(**data))
        user_id = await cursor.fetchone()
        data.update({"id": user_id})
        return web.json_response(data, status=201)


async def get_user(request: web.Request) -> web.Response:
    user_id = request.match_info["user_id"]
    if not user_id.digit():
        raise Exception
    db = request.app["db"]
    async with db.acquire() as conn:
        cursor = await conn.execute(db.users.select().where(db.users.id == user_id))
        records = await cursor.fetchone()
        users = [dict(q) for q in records]
        return web.json_response(users)


async def update_user(request: web.Request) -> web.Response:
    pass


async def delete_user(request: web.Request) -> web.Response:
    pass
