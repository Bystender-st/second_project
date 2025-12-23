import asyncio
from app.seeds.package_types import seed_package_types
from app.db.base import engine


async def main():
    await seed_package_types()
    print("Seeds applied successfully")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
