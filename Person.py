from helper.DateFunctions import jalali_to_gregorian
from helper.validation import required, validation_national_code


class Person:
    __pax_type: str
    __persian_first_name: str
    __persian_last_name: str
    __male: bool
    __birth_day: str
    __national_code: int | str
    __train_cars: list
    __train_capacity_optional_service: dict

    def __init__(self, pax_type: str, persian_first_name: str, persian_last_name: str, male: bool, birth_day: str,
                 national_code: int | str, train_cars: list, train_capacity_optional_service: dict):
        self.__birth_day = jalali_to_gregorian(birth_day)
        if not self.__validation(persian_first_name, persian_last_name, national_code):
            raise "not correct data"
        self.__pax_type = pax_type
        self.__persian_first_name = persian_first_name
        self.__persian_last_name = persian_last_name
        self.__male = male
        self.__national_code = national_code
        self.__train_cars = train_cars
        self.__train_capacity_optional_service = train_capacity_optional_service

    def __validation(self, persian_first_name: str, persian_last_name: str, national_code: int | str):
        return required(persian_last_name) and required(persian_first_name) and validation_national_code(national_code)

    def get_dict(self) -> dict:
        return {
            "PaxType": self.__pax_type,
            "persian_first_name": self.__persian_first_name,
            "persian_last_name": self.__persian_last_name,
            "Male": self.__male,
            "BirthDay": self.__birth_day,
            "national_code": self.__national_code,
            "TrainCars": self.__train_cars,
            "TrainCapacityOptionalService": self.__train_capacity_optional_service,
        }
