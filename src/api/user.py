import json
from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from src.schemas import user as user_schema
from src.core.service import user as user_orm


class Users(web.View):
    @docs(tags=['user'], summary='Get user by id', description='this method return user by user id')
    @querystring_schema(user_schema.UserByID)
    @response_schema(schema=user_schema.ResponseUser)
    async def get(self):
        data = self.request.get("querystring")
        result = await user_orm.get_user_by_id(self.request["session"], data["id"])
        if result is None:
            raise web.HTTPNotFound(
                text=json.dumps({"error": "user not found"}),
                content_type="application/json"
            )
        return web.json_response(user_schema.ResponseUser().dump(*result))

    @request_schema(schema=user_schema.UpdateUserInfo)
    @response_schema(schema=user_schema.ResponseUser)
    @docs(tags=['user'], summary='Add user', description='this method added user')
    async def post(self):
        data = await self.request.json()
        result = await user_orm.add_user(self.request["session"], data)
        return web.json_response(user_schema.ResponseUser().dump(result))

    @request_schema(schema=user_schema.UpdateUserInfo)
    @response_schema(schema=user_schema.ResponseUser)
    @docs(tags=['user'], summary='Update user', description='this method update user by user id')
    async def put(self):
        data = await self.request.json()
        result = await user_orm.put_user(self.request["session"], data)
        return web.json_response(user_schema.ResponseUser().dump(result))

    @querystring_schema(schema=user_schema.UserByID)
    @docs(tags=['user'], summary='Delete user', description='this method delete user by user id')
    async def delete(self):
        data = self.request.get("querystring")
        result = await user_orm.delete_user(self.request["session"], data["id"])
        if not result:
            raise web.HTTPNotFound(
                text=json.dumps({"error": "user not found"}),
                content_type="application/json"
            )
        return web.json_response({"status": "success"})
