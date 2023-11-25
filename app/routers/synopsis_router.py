import aiofiles
import os

import hashlib
from fastapi import APIRouter, File, UploadFile, Body, Response, status
from fastapi.responses import FileResponse

from config import BASE_OUTPUT_FILES, RESULT_DIR


synopsis_router = APIRouter(prefix="/synopsis", tags=["synopsis"])


@synopsis_router.get("/", response_model=list[str])
async def get_all_synopsis():
    dir_objects = os.listdir(os.path.join(BASE_OUTPUT_FILES, RESULT_DIR))
    files_names = []
    for dir_object in dir_objects:
        if os.path.isfile(os.path.join(BASE_OUTPUT_FILES, RESULT_DIR, dir_object)):
            files_names.append(dir_object)

    return files_names


@synopsis_router.get("/download")
async def get_synopsis(file_name: str):
    return FileResponse(os.path.join(BASE_OUTPUT_FILES, RESULT_DIR, file_name))
