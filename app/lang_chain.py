from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Splitter:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Splitter, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3072, chunk_overlap=0
        )

    def process(self, lecture_text):
        return self.text_splitter.split_text(lecture_text)
