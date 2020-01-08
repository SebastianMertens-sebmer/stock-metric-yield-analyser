import json
import re


def loadConfig():
    data = None
    with open("./config.json", "r") as jsonConfig:
        data = json.load(jsonConfig)
    return data


def checkIsbn(isbn):
    match = re.match(r"(\d)-(\d{3})-(\d{5})-(\d)$", isbn)
    if match:
        digits = [int(x) for x in "".join(match.groups())]
        check_digit = digits.pop()
        return (
            check_digit == sum([(i + 1) * digit for i, digit in enumerate(digits)]) % 11
        )
    return True
