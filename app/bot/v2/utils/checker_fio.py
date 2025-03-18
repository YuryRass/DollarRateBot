"""Проверка на правильный ввод ФИО Tg пользователем"""

import re


def check_fullname(full_name: str) -> str:
    fio_pattern: re.Pattern = re.compile(
        r"^[А-ЯЁA-Z][а-яёa-z]+\s+[А-ЯЁA-Z][а-яёa-z]+\s+[А-ЯЁA-Z][а-яёa-z]"
    )

    if fio_pattern.match(full_name):
        return full_name
    else:
        raise ValueError
