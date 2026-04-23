from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..database import get_db
from ..services.face_service import FaceService
from ..schemas.face import FaceEnroll, RecognizeResponse
from ..utils.image_utils import validate_image

router = APIRouter(prefix="/faces", tags=["faces"])

face_service = FaceService()

@router.post("/enroll")
async def enroll_face(enroll: FaceEnroll, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    image = validate_image(await file.read())
    face = await face_service.enroll_face(image, enroll.name, enroll.department_id, db)
    return {"face_id": str(face.id), "message": "Enrolled"}

@router.post("/recognize", response_model=RecognizeResponse)
async def recognize_face(file: UploadFile = File(...), zone_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    image = validate_image(await file.read())
    result = await face_service.recognize_face(image, db, zone_id=zone_id)
    return result