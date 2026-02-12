from sqlalchemy import text
from app.db.session import AsyncSessionLocal


async def count_all_videos() -> int:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM videos"))
        return int(result.scalar_one())
