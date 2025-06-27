import json
import time

from aiohttp import web
from aiohttp.web import Application
from aiohttp_apispec import docs, request_schema, response_schema, validation_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage


from src.schemas import auth as auth_schema
from src.schemas import user as user_schema
from src.core.db import Session
from src.api.json_resp import error_json_response, json_response
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity, HTTPInternalServerError, HTTPForbidden
from src.core.service import user as user_orm
from aiohttp_apispec import setup_aiohttp_apispec
from src.main import setup_sub_main
from aiohttp_session import setup as setup_session, new_session, get_session
from src.auth.authorization import check_user_data


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
    return response


@web.middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(htt_status=400, status="bad request", message=e.reason, data=json.loads(e.text))
    except HTTPException as e:
        return error_json_response(htt_status=e.status, status="error", message=str(e))
    except Exception as e:
        return error_json_response(htt_status=500, status="internal server error", message=str(e))


class Registration(web.View):
    @request_schema(schema=user_schema.User)
    @response_schema(schema=user_schema.ResponseUser)
    @docs(tags=['Registration'], summary='Add user', description='this method added user')
    async def post(self):
        data = await self.request.json()
        result = await user_orm.add_user(self.request["session"], data)
        if result:
            return json_response(data={"user": user_schema.ResponseUser().dump(result)})
        else:
            raise HTTPInternalServerError


class LogIn(web.View):
    @request_schema(schema=auth_schema.Login)
    @docs(tags=['login'], summary='Login user', description='this method login user')
    async def post(self):
        data = await self.request.json()
        result = await check_user_data(self.request["session"], data)
        if not result:
            raise web.HTTPUnauthorized(
                text=json.dumps({"error": "Invalid login or password"}),
            )
        session_cookie = await new_session(request=self.request)
        session_cookie['user'] = data
        return json_response()


class LogOut(web.View):
    @docs(tags=['LogOut'], summary='LoginOut in user', description='this method login user')
    async def get(self):
        session_cookie = await get_session(request=self.request)
        session_cookie.invalidate()
        return json_response()


def setup_middlewares(app: web.Application):
    app.middlewares.append(session_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)


def setup_routes(app: web.Application):
    app.add_routes([web.view('/login', LogIn)])
    app.add_routes([web.view('/registration', Registration)])
    app.add_routes([web.view('/logout', LogOut)])


def setup_api_docs(app: web.Application):
    setup_aiohttp_apispec(
        app=app,
        title="Dog Sitter",
        version="v1",
        url_prefix='/api/docs/swagger.json',
        swagger_path="/api/docs"
    )


if __name__ == '__main__':
    app = Application()
    setup_middlewares(app)
    setup_api_docs(app)
    setup_session(app, EncryptedCookieStorage(
        secret_key='SuperSecretKEY',
        cookie_name="SuperCookieName",
        max_age=43200)
    )
    setup_routes(app)
    sub_main = setup_sub_main()
    app.add_subapp("/sub-main/", sub_main)
    web.run_app(app, host='0.0.0.0', port=8080)
