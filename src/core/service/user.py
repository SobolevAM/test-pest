import json
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from aiohttp import web
from src.core.models.users import User
from src.service.hash_pswd import salted_password


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars()


async def get_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(select(User).where(User.name == login))
    return result.scalar()


async def add_user(db: AsyncSession, item: dict):
    item["password"] = await salted_password(item["password"])
    query = User(**item)
    db.add(query)
    try:
        await db.commit()
    except IntegrityError:
        raise web.HTTPConflict(
            text=json.dumps({"error": "User already exists."}),
            content_type="application/json",
        )
    await db.refresh(query)
    return query


async def put_user(db: AsyncSession, user):
    if user.get("password"):
        user["password"] = await salted_password(user["password"])
    query = update(User).where(User.id == user.id).values(**user)
    await db.execute(query)
    await db.commit()
    return query


async def delete_user(db: AsyncSession, user_id: int):
    result = (await db.execute(select(User).where(User.id == user_id))).scalar()
    if not result:
        return False
    await db.delete(result)
    await db.commit()
    return True
