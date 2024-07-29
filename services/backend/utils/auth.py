from sqlmodel.ext.asyncio.session import AsyncSession
from passlib.context import CryptContext
from models.user import UserFull
from sqlmodel import select

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str, session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(UserFull).where(UserFull.username == username))
    user = result.scalars().first()
    if user:
        return user


async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
