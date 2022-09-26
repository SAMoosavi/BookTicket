"""
import json
import time

from v2.GetTicket import GetTicket
from v2.Passenger import Passenger
from v2.Path import Path
from v2.Person import Person

personJson = open("v2/data/Person.json", 'r')
personData = json.loads(personJson.read())
personJson.close()
del personJson

passenger = Passenger()

for person in personData:
    per = Person()
    per.set_on_dict(person)
    passenger.add_person(per)

pathJson = open("v2/data/Path.json", 'r')
data = json.loads(pathJson.read())
pathJson.close()
del pathJson

path = Path()
pathData = data['path']

while True:
    if path.is_free(pathData['source'], pathData['destination'], pathData['date'], pathData['sex'], data['listId']):
        getTicket = GetTicket()
        loginData = data['login']
        getTicket.login(loginData['username'], loginData['password'])
        tickets = getTicket.get_tickets(pathData['source'], pathData['destination'], pathData['date'], pathData['adult'],
                                        pathData['child'], pathData['sex'])
        getTicket.sel_ticket(path.find_ticket(tickets), data['Passengers'])
        break
    time.sleep(3)

"""
import json
import time

from MrBilitApiWrapper import MrBilitApiWrapper
from Passenger import Passenger
from Person import Person
from User import User

personJson = open('data/Person.json', 'r')
personData = json.loads(personJson.read())
personJson.close()
del personJson

people: list[Person] = []

for person in personData:
    per = Person(person['PaxType'], person['PersianFirstName'], person['PersianLastName'], person['Male'],
                 person['BirthDay'], person['NationalCode'], person['TrainCars'],
                 person['TrainCapacityOptionalService'])
    people.append(per)

pathJson = open("data/Path.json", 'r')
data = json.loads(pathJson.read())
pathJson.close()
del pathJson

loginData = data['login']
pathData = data['path']
listId = data['listId']
passengerData = data['passengers']

passenger = Passenger(passengerData['Email'], passengerData['Mobile'], people, passengerData['Phone'])
user = User(loginData['username'], loginData['password'], loginData['mobile'], loginData['email'])
mrBilit = MrBilitApiWrapper()

while True:
    if mrBilit.get_available(pathData['source'], pathData['destination'], pathData['date'], pathData['sex'], listId):
        mrBilit.login(user.get_username(), user.get_password(), user.get_mobile())
        mrBilit.reserve_seat()
        mrBilit.register_info(passenger)
        mrBilit.pay()
        mrBilit.get_status()
        break
    time.sleep(3)
