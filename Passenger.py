from Person import Person
from helper.validation import validation_email, required, validation_mobile


class Passenger:
    __Email: str
    __Mobile: str
    __People: list[Person]
    __Phone: str
    __BillID: str

    def __init__(self, Email: str, Mobile: str, People: list[Person], Phone: str, BillID: str):
        if validation_email(Email) and required(BillID):
            Mobile = validation_mobile(Mobile)
            if len(Phone):
                Phone = validation_mobile(Phone)

            self.__Email = Email
            self.__Mobile = Mobile
            self.__People = People
            self.__Phone = Phone
            self.__BillID = BillID

    def get_dict(self) -> dict:
        return {
            "Email": self.__Email,
            "Mobile": self.__Mobile,
            "People": self.__get_people(),
            "Phone": self.__Phone,
            "BillID": self.__BillID
        }

    def __get_people(self) -> list[dict]:
        people = []
        for person in self.__People:
            people.append(person.get_dict())
        return people
