import re


class User:
    __username: str
    __password: str
    __mobile: str
    __email: str

    def __init__(self, username: str, password: str, mobile: str | int, email: str):
        self.__username = username
        self.__password = password
        self.__set_mobile(mobile)
        self.__set_email(email)

    def __set_mobile(self, mobile: str | int):
        mobile = self.__validation_mobile(mobile)
        self.__mobile = mobile

    def __validation_mobile(self, mobile: str | int):
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

    def __set_email(self, email: str):
        if self.__validation_email(email):
            self.__email = email

    def __validation_email(self, email: str):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat, email):
            return True
        raise "email not correct"

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_mobile(self):
        return self.__mobile

    def get_email(self):
        return self.__email
