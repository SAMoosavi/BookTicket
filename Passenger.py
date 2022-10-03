from dataclasses import dataclass

from helper.DateFunctions import jalali_to_gregorian


@dataclass
class Passenger:
    email: str
    mobile: str
    phone: str
    persian_first_name: str
    persian_last_name: str
    male: bool
    birth_day: str
    national_code: str
    train_cars: list
    train_capacity_optional_service: dict

    def get_dict(self, bill_ID) -> dict:
        return {
            "Email": self.email,
            "Mobile": self.mobile,
            "People": [
                {
                    "PersianFirstName": self.persian_first_name,
                    "PersianLastName": self.persian_last_name,
                    "Male": self.male,
                    "BirthDay": jalali_to_gregorian(self.birth_day),
                    "NationalCode": self.national_code,
                    "TrainCars": self.train_cars,
                    "TrainCapacityOptionalService": self.train_capacity_optional_service
                }
            ],
            "Phone": self.phone,
            "BillID": bill_ID
        }
