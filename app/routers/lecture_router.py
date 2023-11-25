import aiofiles

import hashlib
from fastapi import APIRouter, File, UploadFile, Body, Response, status

from worker import transcribe_lecture


lecture_router = APIRouter(prefix="/lecture", tags=["lecture"])


@lecture_router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_lecture(lecture: UploadFile = File()):
    lecture_content = await lecture.read()
    file_path = f"/files/{hashlib.sha1(lecture_content).hexdigest()}"

    async with aiofiles.open(file_path, "wb") as file:
        await file.write(lecture_content)

    transcribe_lecture.delay(file_path)
