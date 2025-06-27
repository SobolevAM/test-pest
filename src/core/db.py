from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

base = "postgresql+asyncpg://postgres:postgres@localhost:5432/dog-sitter"

engine = create_async_engine(base, echo=False, pool_size=20, max_overflow=5, pool_timeout=30)

Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
