from PIL import Image
import io
from ..config import settings

def validate_image(image_bytes: bytes) -> Image.Image:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))
        if image.format not in ['JPEG', 'PNG', 'WEBP']:
            raise ValueError("Invalid format")
        if image.width < 80 or image.height < 80:
            raise ValueError("Too small")
        return image
    except Exception:
        raise ValueError("Invalid image")

def resize_image(image: Image.Image, max_size: int = 1280) -> Image.Image:
    if max(image.width, image.height) > max_size:
        image.thumbnail((max_size, max_size))
    return image