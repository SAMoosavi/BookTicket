import json
import time

from MrBilitApiWrapper import MrBilitApiWrapper
from Passenger import Passenger
from Person import Person
from User import User

person_json = open('data/Person.json', 'r')
person_data = json.loads(person_json.read())
person_json.close()
del person_json

people: list[Person] = []

for person in person_data:
    per = Person(person['PaxType'], person['PersianFirstName'], person['PersianLastName'], person['Male'],
                 person['BirthDay'], person['NationalCode'], person['TrainCars'],
                 person['TrainCapacityOptionalService'])
    people.append(per)

path_json = open("data/Path.json", 'r')
data = json.loads(path_json.read())
path_json.close()
del path_json

login_data = data['login']
path_data = data['path']
list_ID = data['listId']
passenger_data = data['passengers']

passenger = Passenger(passenger_data['Email'], passenger_data['Mobile'], people, passenger_data['Phone'])
user = User(login_data['username'], login_data['password'], login_data['mobile'], login_data['email'])
mr_bilit = MrBilitApiWrapper()

while not mr_bilit.get_available(path_data['source'], path_data['destination'], path_data['date'], path_data['sex'], list_ID):
    time.sleep(3)
mr_bilit.login(user.get_username(), user.get_password(), user.get_mobile())
mr_bilit.reserve_seat()
mr_bilit.register_info(passenger)
mr_bilit.pay()
while not mr_bilit.get_status():
    time.sleep(3)
mr_bilit.get_pdf()
