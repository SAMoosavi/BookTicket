from helper.validation import validation_email, validation_mobile


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
        mobile = validation_mobile(mobile)
        self.__mobile = mobile

    def __set_email(self, email: str):
        if validation_email(email):
            self.__email = email

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_mobile(self):
        return self.__mobile

    def get_email(self):
        return self.__email
