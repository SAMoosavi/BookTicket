import re


class User:
    username: str
    password: str
    mobile: str
    email: str

    def __init__(self, username: str, password: str, mobile: str | int, email: str):
        self.username = username
        self.password = password
        self.__set_mobile(mobile)
        self.__set_email(email)

    def __set_mobile(self, mobile: str | int):
        mobile = self.__validation_mobile(mobile)
        self.mobile = mobile

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
            self.email = email

    def __validation_email(self, email: str):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat, email):
            return True
        raise "email not correct"

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_mobile(self):
        return self.mobile

    def get_email(self):
        return self.email
