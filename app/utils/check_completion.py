import os

from config import BASE_OUTPUT_FILES, TERMINS_DIR, SUMMARY_DIR


def check_completion(file_name: str) -> bool:
    if os.path.exists(
        os.path.join(BASE_OUTPUT_FILES, TERMINS_DIR, file_name)
    ) and os.path.exists(os.path.join(BASE_OUTPUT_FILES, SUMMARY_DIR, file_name)):
        return True

    return False
