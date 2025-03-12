"""Проверка на правильный ввод ФИО Tg пользователем"""

import re


def is_correct_fullname(full_name: str) -> bool:
    fio_pattern: re.Pattern = re.compile(
        r"^[А-ЯЁA-Z][а-яёa-z]+\s+[А-ЯЁA-Z][а-яёa-z]+\s+[А-ЯЁA-Z][а-яёa-z]"
    )

    return fio_pattern.match(full_name)
