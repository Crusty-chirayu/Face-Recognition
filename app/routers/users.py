from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..schemas.user import UserCreate, UserRead, UserUpdate
from ..core.deps import require_admin
from ..models.user import User
from ..services.auth_service import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
async def read_users(db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserRead.from_orm(u) for u in users]

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, name=user.name, role=user.role, password_hash=hashed)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserRead.from_orm(db_user)

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: str, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return UserRead.from_orm(user)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: str, user_update: UserUpdate, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    for k, v in user_update.dict(exclude_unset=True).items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return UserRead.from_orm(user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = False
    await db.commit()
    return {"message": "User deactivated"}