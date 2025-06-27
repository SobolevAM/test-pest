from aiohttp import web
from src.api.user import Users


def setup_routers(app: web.Application):
    app.add_routes([web.view('/user', Users)])
