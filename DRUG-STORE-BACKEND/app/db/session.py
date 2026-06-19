from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_ = AsyncSession,
    expire_on_commit=False
)
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()