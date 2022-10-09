from dataclasses import dataclass


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
