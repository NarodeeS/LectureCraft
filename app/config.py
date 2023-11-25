import os

BASE_OUTPUT_FILES = "/output_files"
WHISPER_DIR = "whisper"
TERMINS_DIR = "termins"
SUMMARY_DIR = "summary"
RESULT_DIR = "result"


MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "base")
SAIGA_BASE_PATH = os.environ.get("SAIGA_PATH", "/saiga/model-q4_K.gguf")
