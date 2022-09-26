import json
import time

from MrBilitApiWrapper import MrBilitApiWrapper
from Passenger import Passenger
from Person import Person
from PlayMusic import PlayMusic
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

while not mrBilit.get_available(pathData['source'], pathData['destination'], pathData['date'], pathData['sex'], listId):
    time.sleep(3)
mrBilit.login(user.get_username(), user.get_password(), user.get_mobile())
mrBilit.reserve_seat()
mrBilit.register_info(passenger)
mrBilit.pay()
while not mrBilit.get_status():
    time.sleep(3)
mrBilit.get_pdf()
PlayMusic()
