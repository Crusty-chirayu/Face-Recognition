from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate
from ..core.deps import get_current_user
from ..models.department import Department
from ..models.user import User

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/", response_model=list[DepartmentRead])
async def read_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department))
    depts = result.scalars().all()
    return [DepartmentRead.from_orm(d) for d in depts]

@router.post("/", response_model=DepartmentRead)
async def create_department(dept: DepartmentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_dept = Department(name=dept.name, description=dept.description, color=dept.color, created_by=current_user.id)
    db.add(db_dept)
    await db.commit()
    await db.refresh(db_dept)
    return DepartmentRead.from_orm(db_dept)

@router.get("/{dept_id}", response_model=DepartmentRead)
async def read_department(dept_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(404, "Department not found")
    return DepartmentRead.from_orm(dept)

@router.patch("/{dept_id}", response_model=DepartmentRead)
async def update_department(dept_id: str, dept_update: DepartmentUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(404, "Department not found")
    for k, v in dept_update.dict(exclude_unset=True).items():
        setattr(dept, k, v)
    await db.commit()
    await db.refresh(dept)
    return DepartmentRead.from_orm(dept)

@router.delete("/{dept_id}")
async def delete_department(dept_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(404, "Department not found")
    await db.delete(dept)
    await db.commit()
    return {"message": "Department deleted"}

@router.get("/{dept_id}/members")
async def read_department_members(dept_id: str, db: AsyncSession = Depends(get_db)):
    from ..models.face import Face
    result = await db.execute(select(Face).where(Face.department_id == dept_id))
    faces = result.scalars().all()
    return [{"id": str(f.id), "name": f.person_name} for f in faces]