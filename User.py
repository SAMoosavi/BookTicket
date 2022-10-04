from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str
    mobile: str
    email: str
