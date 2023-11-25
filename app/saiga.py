from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch

MODEL_NAME = "IlyaGusev/saiga2_7b_lora"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>\n"
DEFAULT_SYSTEM_PROMPT = [
    """Проанализируйте следующий текст лекции и выделите все термины с их определениями. Каждый термин с его определением должен быть представлен в формате: "<Термин> - <определение>". Убедитесь, что каждый новый термин начинается с новой строки.

Ожидаемый результат:
1. <Термин 1> - <определение термина 1>.
2. <Термин 2> - <определение термина 2>.
...

Текст лекции:""",
    "Выдели основную суть из текста лекции, то есть сделай конспект, краткую выжимку на русском языке. Не добавляй ссылки на внешние источники. Не говори от первого лица. Вот текст лекции:",
]


class SaigaModel:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SaigaModel, cls).__new__(cls)
        return cls.__instance

    def __init__(
        self,
        message_template=DEFAULT_MESSAGE_TEMPLATE,
        system_prompt=DEFAULT_SYSTEM_PROMPT[0],
        start_token_id=1,
        bot_token_id=9225,
    ):
        self.message_template = message_template
        self.start_token_id = start_token_id
        self.bot_token_id = bot_token_id
        self.messages = []

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
        self.generation_config = GenerationConfig.from_pretrained(MODEL_NAME)

        config = PeftConfig.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        self.model = PeftModel.from_pretrained(
            self.model, MODEL_NAME, torch_dtype=torch.float16
        )
        self.model.eval()

    def get_start_token_id(self):
        return self.start_token_id

    def get_bot_token_id(self):
        return self.bot_token_id

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_bot_message(self, message):
        self.messages.append({"role": "bot", "content": message})

    def get_prompt(self, tokenizer):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += tokenizer.decode([self.start_token_id, self.bot_token_id])
        return final_text.strip()

    def process(self, lecture_text, stage=1):
        if stage == 1:
            self.messages = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT[0]}]
        if stage == 2:
            self.messages = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT[1]}]

        self.add_user_message(lecture_text)
        prompt = self.get_prompt(self.tokenizer)

        data = self.tokenizer(prompt, return_tensors="pt")
        data = {k: v.to(self.model.device) for k, v in data.items()}
        output_ids = self.model.generate(
            **data, generation_config=self.generation_config
        )[0]
        output_ids = output_ids[len(data["input_ids"][0]) :]
        output = self.tokenizer.decode(output_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        return output.strip()
