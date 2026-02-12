import asyncio

from app.utils.json_loader import load_json
from app.services.loader import load_videos


async def main():
    raw = load_json("videos.json")
    data = raw["videos"]
    await load_videos(data)


if __name__ == "__main__":
    asyncio.run(main())
