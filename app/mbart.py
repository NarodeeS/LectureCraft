from transformers import MBartTokenizer, MBartForConditionalGeneration

MODEL_NAME = "IlyaGusev/mbart_ru_sum_gazeta"


class MBARTModel:
    # __instance = None

    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super(MBARTModel, cls).__new__(cls)
    #     return cls.__instance

    def __init__(self):
        self.tokenizer = MBartTokenizer.from_pretrained(MODEL_NAME)
        self.model = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)

    def process(self, lecture_text):
        input_ids = self.tokenizer(
            [lecture_text],
            max_length=600,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )["input_ids"]

        output_ids = self.model.generate(input_ids=input_ids, no_repeat_ngram_size=4)[0]

        summary = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        return summary
