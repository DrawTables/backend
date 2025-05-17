import re


def remove_code_markers(text):
    pattern = r"^```(?:dbml|sql)\n(.*?)```$"
    result = re.sub(pattern, r"\1", text, flags=re.DOTALL)
    return result
