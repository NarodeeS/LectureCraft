import os
from config import BASE_OUTPUT_FILES, TERMINS_DIR, SUMMARY_DIR, RESULT_DIR


def create_markdown(file_name: str) -> None:
    file_content = "## Термины\n"

    with open(os.path.join(BASE_OUTPUT_FILES, TERMINS_DIR, file_name), "r") as file:
        file_content += "\n".join(file.readlines())

    file_content += "\n\n## Конспект\n"

    with open(
        os.path.join(BASE_OUTPUT_FILES, SUMMARY_DIR, file_name),
        "r",
    ) as file:
        file_content += "\n".join(file.readlines())

    with open(os.path.join(BASE_OUTPUT_FILES, RESULT_DIR, file_name), "w") as file:
        file.writelines(file_content)
