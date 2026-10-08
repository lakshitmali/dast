"""
DAST Platform — API Dependencies
Authentication and database session injection.
"""

import uuid
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.core.security import verify_access_token
from app.models.user import User
from app.config import get_settings

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate the current user from JWT bearer token."""
    settings = get_settings()
    if credentials is None:
        if settings.DEBUG and settings.ALLOW_LOCAL_TARGETS:
            result = await db.execute(select(User).where(User.username == "local-demo"))
            user = result.scalar_one_or_none()
            if user is None:
                user = User(
                    email="local-demo@localhost",
                    username="local-demo",
                    hashed_password="local-development-only",
                    full_name="Local Demo User",
                    is_active=True,
                    is_admin=True,
                    tos_accepted_at=datetime.now(timezone.utc),
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        parsed_user_id = uuid.UUID(user_id)
    except (ValueError, AttributeError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    result = await db.execute(select(User).where(User.id == parsed_user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    return user


async def get_ws_user(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """
    Extract user from WebSocket query parameter token.
    WebSocket connections pass the token as ?token=<jwt>
    """
    token = websocket.query_params.get("token")
    if not token:
        return None

    payload = verify_access_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    )
    return result.scalar_one_or_none()
