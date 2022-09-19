from helper.DateFunctions import j_to_g
from helper.validation import required, validation_national_code


class Person:
    __PaxType: str
    __PersianFirstName: str
    __PersianLastName: str
    __Male: bool
    __BirthDay: str
    __NationalCode: int | str
    __TrainCars: list
    __TrainCapacityOptionalService: dict

    def __init__(self, PaxType: str, PersianFirstName: str, PersianLastName: str, Male: bool, BirthDay: str,
                 NationalCode: int | str, TrainCars: list, TrainCapacityOptionalService: dict):
        self.__BirthDay = j_to_g(BirthDay)
        if not self.__validation(PersianFirstName, PersianLastName, NationalCode):
            raise "not correct data"
        self.__PaxType = PaxType
        self.__PersianFirstName = PersianFirstName
        self.__PersianLastName = PersianLastName
        self.__Male = Male
        self.__NationalCode = NationalCode
        self.__TrainCars = TrainCars
        self.__TrainCapacityOptionalService = TrainCapacityOptionalService

    def __validation(self, PersianFirstName: str, PersianLastName: str, NationalCode: int | str):
        return required(PersianLastName) and required(PersianFirstName) and validation_national_code(NationalCode)

    def get_dict(self) -> dict:
        return {
            "PaxType": self.__PaxType,
            "PersianFirstName": self.__PersianFirstName,
            "PersianLastName": self.__PersianLastName,
            "Male": self.__Male,
            "BirthDay": self.__BirthDay,
            "NationalCode": self.__NationalCode,
            "TrainCars": self.__TrainCars,
            "TrainCapacityOptionalService": self.__TrainCapacityOptionalService,
        }
