import re


def validation_email(email: str):
    path = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(path, email):
        return True
    raise "email not correct"


def validation_mobile(mobile: str | int):
    phone_number: str = str(mobile)
    if not phone_number[0] == "0":
        if not phone_number[0] == "9":
            raise "mobile not correct"
        else:
            phone_number = "0" + phone_number
    else:
        if not phone_number[1] == "9":
            raise "mobile not correct"
    return phone_number


def required(val: str):
    return len(val) != 0


def validation_national_code(national_code: int | str):
    national_code_str = str(national_code)
    return len(national_code_str) == 10
