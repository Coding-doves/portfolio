import os
import shutil

from datetime import datetime
from fastapi import File, UploadFile


def upload_images(dir: str, image: UploadFile = File(...)) -> str:
    # Prepare directory and filename
    os.makedirs(f"media/images/{dir}", exist_ok=True)
    filename = f"{datetime.now().timestamp()}_{image.filename}"
    path = f"media/images/{dir}/{filename}"

    # Save image to disk
    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return path
