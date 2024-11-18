from aiohttp import web
from hw.views.users import create_user, delete_user, update_user, get_user, list_users
from hw.views.health import health_handler


def init_routes(app):
    app.add_routes(
        [
            web.get("/api/v1/health", health_handler, name="health"),
            # users
            web.post("/api/v1/users", create_user),
            web.get("/api/v1/users", list_users),
            web.get("/api/v1/users/{user_id}", get_user),
            web.patch("/api/v1/users/{user_id}", update_user),
            web.delete("/api/v1/users/{user_id}", delete_user),
        ]
    )
