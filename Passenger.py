import json

from Person import Person


class Passenger:
    __URL: str = "data/passengers.json"
    __passengers: list[dict] = []

    def __int__(self):
        file = open(self.__URL, "r")
        print("hi")
        print(file)
        self.__passengers = json.loads(file.read())

    def add_person(self, person: Person) -> None:
        personDict = person.get_dict()
        if self.__get_person_by_ID(personDict['ID']):
            print('person has in passenger list')
        else:
            self.__passengers.append(personDict)

    def __get_person_by_ID(self, ID: str | int) -> Person | None:
        for person in self.__passengers:
            if person['ID'] == str(ID):
                print(person['ID'] == str(ID))
                return Person().set(
                    person['firstName'],
                    person['lastName'], person['ID'],
                    str(person['berthDay']['year']) + "/" +
                    str(person['berthDay']['month']) + "/" +
                    str(person['berthDay']['day'])
                )
            return None

    def get_person_by_ID(self, ID: str | int) -> Person:
        result = self.__get_person_by_ID(ID)
        if result:
            return result
        raise "not found passenger"

    def __del__(self):
        file = open(self.__URL, "w")
        file.write(json.dumps(self.__passengers))
