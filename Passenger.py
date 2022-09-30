from helper.DateFunctions import jalali_to_gregorian
from helper.validation import validation_email, validation_mobile, required, validation_national_code


def validation_person(person: dict) -> bool:
    return \
        required(person['PersianFirstName']) and \
        required(person['PersianLastName']) and \
        validation_national_code(person['NationalCode']) and \
        required(person['BirthDay']) and \
        'TrainCars' in person and \
        'TrainCapacityOptionalService' in person and \
        'Male' in person


def validation_people(people: list[dict]) -> bool:
    for person in people:
        if not validation_person(person):
            return False
    return True


def set_birth_day_people(people: list[dict]):
    for person in people:
        person['BirthDay'] = jalali_to_gregorian(person['BirthDay'])


class Passenger:
    __email: str
    __mobile: str
    __people: list[dict]
    __phone: str

    def __init__(self, email: str, mobile: str, people: list[dict], phone: str):
        if validation_email(email) and validation_people(people):
            mobile = validation_mobile(mobile)
            if len(phone):
                phone = validation_mobile(phone)
            set_birth_day_people(people)

            self.__email = email
            self.__mobile = mobile
            self.__people = people
            self.__phone = phone
        else:
            raise "not correct data"

    def get_dict(self, bill_ID) -> dict:
        return {
            "Email": self.__email,
            "Mobile": self.__mobile,
            "People": self.__people,
            "Phone": self.__phone,
            "BillID": bill_ID
        }
