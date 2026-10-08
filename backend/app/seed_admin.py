"""
DAST Platform — Seed Admin User
Run: python -m app.seed_admin
"""

import asyncio
from sqlalchemy import select
from app.database import async_session_factory, init_db
from app.models.user import User
from app.core.security import hash_password


async def seed_admin():
    await init_db()

    async with async_session_factory() as session:
        # Check if admin already exists
        result = await session.execute(
            select(User).where(User.email == "mulugeta237@gmail.com")
        )
        existing = result.scalar_one_or_none()

        if existing:
            print("✓ Admin user already exists")
            return

        admin = User(
            email="mulugeta237@gmail.com",
            username="mulugeta",
            hashed_password=hash_password("Admin@1234"),  # change this password
            full_name="Mulugeta Ababi",
            is_active=True,
            is_admin=True,
        )
        session.add(admin)
        await session.commit()
        print("✓ Admin user created successfully")
        print("  Email:    mulugeta237@gmail.com")
        print("  Password: Admin@1234  ← CHANGE THIS after first login")


if __name__ == "__main__":
    asyncio.run(seed_admin())
