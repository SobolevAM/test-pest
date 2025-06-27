from sqlalchemy.ext.asyncio import AsyncSession
from src.core.service.user import get_user_by_login
from src.service.hash_pswd import check_password


async def check_user_data(db: AsyncSession, data: dict) -> int:
    user = await get_user_by_login(db, data['login'])
    if user:
        if await check_password(data['password'], user.password):
            return user.id
    return False
