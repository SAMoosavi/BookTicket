import json

from Person import Person


class Passenger:
    __URL: str = "data/passengers.json"
    __passengers: list[dict] = []

    def __init__(self):
        file = open(self.__URL, "r")
        data = file.read()
        if data:
            self.__passengers = json.loads(data)

    def add_person(self, person: Person) -> None:
        personDict = person.get_dict()
        if self.__get_person_by_ID(personDict['ID']):
            print('person has in passenger list')
        else:
            self.__passengers.append(personDict)
            self.__save()

    def __get_person_by_ID(self, ID: str | int) -> Person | None:
        for person in self.__passengers:
            if person['ID'] == str(ID):
                return Person().set_on_dict(person)
            return None

    def get_person_by_ID(self, ID: str | int) -> Person:
        result = self.__get_person_by_ID(ID)
        if result:
            return result
        raise "not found passenger"

    def __save(self):
        file = open(self.__URL, "w")
        file.write(json.dumps(self.__passengers))

    def __del__(self):
        self.__save()
