from re import search


def remove_turkmen_letter(string: str):
    from_to = [
        ["ň", "n"],
        ["ş", "sh"],
        ["ç", "ch"],
        ["ö", "o"],
        ["ä", "a"],
        ["ž", "zh"],
        ["ü", "u"],
        ["ý", "y"],
    ]
    for i in from_to:
        string = string.replace(i[0], i[1])
    return string


def transliterate(text):
    transliteration_table = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
    transliterated_text = "".join(
        transliteration_table.get(char, char) for char in text
    )
    return transliterated_text


def contains_cyrillic(text):
    return bool(search(r"[А-Яа-яЁё]", text))
