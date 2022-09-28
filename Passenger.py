from Person import Person
from helper.validation import validation_email, validation_mobile


class Passenger:
    __email: str
    __mobile: str
    __people: list[Person]
    __phone: str

    def __init__(self, email: str, mobile: str, people: list[Person], phone: str):
        if validation_email(email):
            mobile = validation_mobile(mobile)
            if len(phone):
                phone = validation_mobile(phone)

            self.__email = email
            self.__mobile = mobile
            self.__people = people
            self.__phone = phone

    def get_dict(self, bill_ID) -> dict:
        return {
            "Email": self.__email,
            "Mobile": self.__mobile,
            "People": self.__get_people(),
            "Phone": self.__phone,
            "BillID": bill_ID
        }

    def __get_people(self) -> list[dict]:
        people = []
        for person in self.__people:
            people.append(person.get_dict())
        return people
