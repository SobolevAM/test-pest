from aiohttp import web
from aiohttp.web import Application, middleware
from src.api.routers import setup_routers
from aiohttp_session import get_session


@middleware
async def auth_middleware(request: web.Request, handler) -> web.Response:
    data = await get_session(request)
    if not data:
        raise web.HTTPForbidden(
            text="You are not logged in."
        )
    response = await handler(request)
    return response


def setup_sub_main():
    app = Application()
    app.middlewares.append(auth_middleware)
    setup_routers(app)
    return app



