FROM python:3.11

ARG WORKERS=2

RUN apt-get update

RUN apt-get install ffmpeg git build-essential -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY ./requirements.txt ./

RUN pip install -r requirements.txt  \
    && mkdir /files

RUN pip3 install scipy sentencepiece langchain

COPY . .

CMD ["uvicorn", "--workers", WORKERS, "--host", "0.0.0.0", "--port", "8000", "main:app"]