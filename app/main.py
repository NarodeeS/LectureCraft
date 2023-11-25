from fastapi import FastAPI

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from routers.lecture_router import lecture_router
from routers.synopsis_router import synopsis_router


openapi_tags = [
    {"name": "lecture", "description": "Operations with lectures"},
    {"name": "synopsis", "description": "Operations on synopsis from lectures"},
]


app = FastAPI(
    title="LectureCraft API",
    description="API for creating synopsis from audio lectures",
    openapi_tags=openapi_tags,
)
origins = ["http://localhost", "http://localhost:8080", "http://87.236.81.236:13980"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lecture_router, prefix="/api")
app.include_router(synopsis_router, prefix="/api")
