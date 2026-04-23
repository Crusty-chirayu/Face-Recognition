from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..database import get_db
from ..services.auth_service import authenticate_user, create_access_token, create_refresh_token, verify_token, revoke_token, create_user
from ..schemas.user import UserRead, Token, LoginRequest, RegisterRequest
from ..core.deps import get_current_user
from ..models.user import User
from ..models.session import Session
from ..config import settings
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, request.email, request.name, request.password)
    return UserRead.from_orm(user)

@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    jti = str(uuid.uuid4())
    access_token = create_access_token(data={"sub": str(user.id), "jti": jti, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "jti": jti})
    session = Session(jti=jti, user_id=user.id, expires_at=datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days))
    db.add(session)
    await db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user": UserRead.from_orm(user)}

@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = await verify_token(refresh_token, "refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = int(payload.get("sub"))
    jti = payload.get("jti")
    if await redis_client.exists(f"revoked:{jti}"):
        raise HTTPException(status_code=401, detail="Token revoked")
    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    new_access = create_access_token(data={"sub": str(user.id), "jti": jti, "role": user.role})
    new_refresh = create_refresh_token(data={"sub": str(user.id), "jti": jti})
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserRead.from_orm(current_user)