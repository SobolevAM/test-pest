from bcrypt import checkpw, gensalt, hashpw


async def salted_password(password):
    return hashpw(password.encode(), gensalt()).decode('utf-8')


async def check_password(password, hashed) -> bool:
    check = checkpw(password.encode(), hashed.encode())
    return check
