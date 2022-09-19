import re


def validation_email(email: str):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    raise "email not correct"


def validation_mobile(mobile: str | int):
    phoneNumber: str = str(mobile)
    if not phoneNumber[0] == "0":
        if not phoneNumber[0] == "9":
            raise "mobile not correct"
        else:
            phoneNumber = "0" + phoneNumber
    else:
        if not phoneNumber[1] == "9":
            raise "mobile not correct"
    return phoneNumber


def required(val: str):
    return not len(val) is 0


def validation_national_code(NationalCode: int | str):
    nationalCodeStr = str(NationalCode)
    return len(nationalCodeStr) == 10
