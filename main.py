import json
import time

from GlobalVariables import Sex
from MrBilitApiWrapper import MrBilitApiWrapper
from Passenger import Passenger
from User import User

with open('data/Passenger.json', 'r') as passenger_json:
    passenger_data = json.load(passenger_json)


def set_train(list_of_train, sex: Sex, list_train_ID: list[int | str]):
    classes = []
    for ID in list_train_ID:
        train = next((t for t in list_of_train if str(ID) == str(t['TrainNumber'])), None)
        if train:
            for price in train['Prices']:
                if price['SellType'] == sex:
                    classes.append(price['Classes'])
                    break
    return classes


def get_class_train_ID(classes_train) -> int | str:
    return next((class_train["ID"] for class_train in classes_train if class_train["Capacity"] > 0), None)


def get_pdf(ticket_files):
    urls = [ticket_file["url"] for ticket_file in ticket_files]
    print("list of blit:", *urls)


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
while True:
    try:
        mr_bilit = MrBilitApiWrapper(user)
        break
    except:
        pass

my_train = {}
train_ID = ""
i = 0
j = 0
while True:
    try:
        j += 1
        print(j)
        while True:
            i += 1
            trains = mr_bilit.get_available(
                path_data['source'],
                path_data['destination'],
                path_data['date'],
                Sex(path_data['sex'])
            )
            if len(trains) != 0:
                my_train = set_train(trains, Sex(path_data['sex']), list_ID)
                if len(my_train) != 0:
                    train_ID = get_class_train_ID(my_train)
                    print("found")
                    break
            print(i, " not found")
            time.sleep(20)

        reserve_data = mr_bilit.reserve_seat(train_ID, Sex(path_data['sex']))
        mr_bilit.register_info(reserve_data['BillID'], passenger)
        mac = mr_bilit.pay(reserve_data['BillCode'])
        tickets = []
        while True:
            tickets = mr_bilit.get_status(reserve_data['BillCode'], mac)
            if len(tickets) != 0:
                get_pdf(tickets)
                break
            time.sleep(3)
    except:
        print("err")
        time.sleep(20)
