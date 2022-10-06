import json
import time

from MrBilitApiWrapper import MrBilitApiWrapper
from Passenger import Passenger
from User import User

passenger_json = open('data/Passenger.json', 'r')
passenger_data = json.loads(passenger_json.read())
passenger_json.close()
del passenger_json


def set_train(list_of_train, sex, list_train_ID: list[int | str]):
    for ID in list_train_ID:

        if ID == 0:
            train = list_of_train[0]
            for price in train['Prices']:
                if price['SellType'] == sex:
                    return price['Classes']

        for train in list_of_train:
            if str(ID) == str(train['TrainNumber']):
                for price in train['Prices']:
                    if price['SellType'] == sex:
                        return price['Classes']
    return []


def get_class_train_ID(classes_train) -> int | str:
    for class_train in classes_train:
        if class_train["Capacity"] > 0:
            return class_train["ID"]


def get_pdf(ticket_files):
    print("list of blit:")
    for ticket_file in ticket_files:
        print(ticket_file["url"])


path_json = open("data/Path.json", 'r')
data = json.loads(path_json.read())
path_json.close()
del path_json

login_data = data['login']
path_data = data['path']
list_ID = data['listId']

passenger = Passenger(
    email=passenger_data['Email'],
    mobile=passenger_data['Mobile'],
    phone=passenger_data['Phone'],
    persian_first_name=passenger_data['People'][0]["PersianFirstName"],
    persian_last_name=passenger_data['People'][0]["PersianLastName"],
    male=passenger_data['People'][0]["Male"],
    birth_day=passenger_data['People'][0]["BirthDay"],
    national_code=passenger_data['People'][0]["NationalCode"],
    train_cars=passenger_data['People'][0]["TrainCars"],
    train_capacity_optional_service=passenger_data['People'][0]["TrainCapacityOptionalService"],
)
del passenger_data

user = User(
    username=login_data['username'],
    password=login_data['password'],
    mobile=login_data['mobile'],
    email=login_data['email']
)
mr_bilit = MrBilitApiWrapper(user)

my_train = {}
train_ID = ""
i = 0
while True:
    i += 1
    trains = mr_bilit.get_available(path_data['source'], path_data['destination'], path_data['date'], path_data['sex'])
    if len(trains) != 0:
        my_train = set_train(trains, path_data['sex'], list_ID)
        if len(my_train) != 0:
            train_ID = get_class_train_ID(my_train)
            print("found")
            break
    print(i, " not found")
    time.sleep(20)

reserve_data = mr_bilit.reserve_seat(train_ID, 1, 0, 0)
mr_bilit.register_info(reserve_data['BillID'], passenger)
mac = mr_bilit.pay(reserve_data['BillCode'])
tickets = []
while True:
    tickets = mr_bilit.get_status(reserve_data['BillCode'], mac)
    if len(tickets) != 0:
        get_pdf(tickets)
        break
    time.sleep(3)
