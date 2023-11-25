import whisper
import os
import torch
from datetime import datetime
from celery import Celery
from saiga import SaigaModel
from mbart import MBARTModel
from lang_chain import Splitter

from utils.check_completion import check_completion
from utils.create_markdown import create_markdown
from pathlib import Path
from config import (
    BASE_OUTPUT_FILES,
    WHISPER_DIR,
    TERMINS_DIR,
    SUMMARY_DIR,
    RESULT_DIR,
    WHISPER_MODEL,
    CELERY_BROKER_URL,
)

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_BROKER_URL


Path(os.path.join(BASE_OUTPUT_FILES, WHISPER_DIR)).mkdir(parents=True, exist_ok=True)
Path(os.path.join(BASE_OUTPUT_FILES, SUMMARY_DIR)).mkdir(parents=True, exist_ok=True)
Path(os.path.join(BASE_OUTPUT_FILES, TERMINS_DIR)).mkdir(parents=True, exist_ok=True)
Path(os.path.join(BASE_OUTPUT_FILES, RESULT_DIR)).mkdir(parents=True, exist_ok=True)


@celery.task(name="transcribe_lecture")
def transcribe_lecture(lecture_path: str):
    torch.multiprocessing.set_start_method("spawn", force=True)

    whisper_model = whisper.load_model(WHISPER_MODEL, device="cuda")
    options = whisper.DecodingOptions(language="ru")
    result = whisper_model.transcribe(lecture_path)
    transcription = str(result["text"])

    file_name = datetime.now().isoformat()
    with open(
        os.path.join(BASE_OUTPUT_FILES, WHISPER_DIR, file_name),
        "w",
    ) as file:
        file.write(transcription)

    extract_termins.delay(file_name)
    create_summary.delay(file_name)

    # TODO send task for termins and summary


@celery.task(name="extract_termins")
def extract_termins(whisper_text_file_name: str):
    print("extract_termins")
    saiga_model = SaigaModel()

    path = os.path.join(BASE_OUTPUT_FILES, WHISPER_DIR, whisper_text_file_name)
    with open(path, "r") as file:
        text = file.read()

    splitter = Splitter()

    splits = splitter.process(text)
    saiga_texts = []
    for prompt in splits:
        res = saiga_model.process(prompt, stage=1)
        saiga_texts.append(res)
        print(res)

    with open(
        os.path.join(BASE_OUTPUT_FILES, TERMINS_DIR, whisper_text_file_name), "w"
    ) as file:
        file.write("\n".join(saiga_texts))

    if check_completion(whisper_text_file_name):
        create_markdown(whisper_text_file_name)


@celery.task(name="create_summary")
def create_summary(whisper_text_file_name: str):
    saiga_model = SaigaModel()

    path = os.path.join(BASE_OUTPUT_FILES, WHISPER_DIR, whisper_text_file_name)
    with open(path, "r") as file:
        text = file.read()

    splitter = Splitter()

    splits = splitter.process(text)
    saiga_texts = []
    for prompt in splits:
        res = saiga_model.process(prompt, stage=2)
        saiga_texts.append(res)
        print(res)

    with open(
        os.path.join(BASE_OUTPUT_FILES, SUMMARY_DIR, whisper_text_file_name), "w"
    ) as file:
        file.write("\n".join(saiga_texts))

    if check_completion(whisper_text_file_name):
        create_markdown(whisper_text_file_name)
