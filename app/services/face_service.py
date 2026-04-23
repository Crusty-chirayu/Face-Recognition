from PIL import Image
import os
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.face import Face
from ..models.face_photo import FacePhoto
from ..utils.image_utils import validate_image, resize_image
from ..ml.detector import FaceDetector
from ..ml.encoder import FaceEncoder
from ..ml.matcher import FaceMatcher
from ..config import settings
from .attendance_service import AttendanceService
from .watchlist_service import WatchlistService
from .notification_service import NotificationService

class FaceService:
    def __init__(self):
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.matcher = FaceMatcher()
        self.attendance_service = AttendanceService()
        self.watchlist_service = WatchlistService()
        self.notification_service = NotificationService()

    async def enroll_face(self, image: Image.Image, name: str, department_id: str = None, db: AsyncSession = None) -> Face:
        image = resize_image(image)
        np_image = np.array(image)
        faces = self.detector.detect_faces(np_image)
        if len(faces) != 1:
            raise ValueError("Must have exactly one face")
        bbox = faces[0]
        embedding = self.encoder.encode_face(np_image, bbox)
        face = Face(person_name=name, department_id=department_id, embedding=embedding.tolist())
        db.add(face)
        await db.commit()
        await db.refresh(face)
        photo_dir = os.path.join(settings.upload_dir, "faces", str(face.id))
        os.makedirs(photo_dir, exist_ok=True)
        photo_path = os.path.join(photo_dir, "photo.jpg")
        image.save(photo_path)
        face_photo = FacePhoto(face_id=face.id, photo_path=photo_path, embedding=embedding.tolist(), is_primary=True)
        db.add(face_photo)
        await db.commit()
        return face

    async def recognize_face(self, image: Image.Image, db: AsyncSession, zone_id: str | None = None) -> dict:
        image = resize_image(image)
        np_image = np.array(image)
        faces = self.detector.detect_faces(np_image)
        if not faces:
            return {"recognized": False, "name": "unknown", "confidence": 0.0}
        bbox = faces[0]
        embedding = self.encoder.encode_face(np_image, bbox)
        result = await db.execute(select(Face))
        known_faces = result.scalars().all()
        known_embeddings = [np.array(f.embedding) for f in known_faces]
        matched, confidence, index = self.matcher.match(embedding, known_embeddings, settings.recognition_threshold)
        if matched:
            face = known_faces[index]
            await self.attendance_service.log_attendance(db, face, confidence, zone_id=zone_id)
            if await self.watchlist_service.is_on_watchlist(str(face.id), db):
                title = f"⚠ {face.person_name} detected on watchlist"
                body = f"Face {face.person_name} matched in zone {zone_id or 'unknown'}."
                await self.notification_service.notify_admins(db, title, body, {"face_id": str(face.id), "zone_id": zone_id})
            return {"recognized": True, "name": face.person_name, "face_id": str(face.id), "confidence": confidence, "bbox": bbox}
        else:
            return {"recognized": False, "name": "unknown", "confidence": 0.0, "bbox": bbox}