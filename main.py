import json
import time

from MrBilitApiWrapper import MrBilitApiWrapper
from Passenger import Passenger
from User import User

passenger_json = open('data/Passenger.json', 'r')
passenger_data = json.loads(passenger_json.read())
passenger_json.close()
del passenger_json

path_json = open("data/Path.json", 'r')
data = json.loads(path_json.read())
path_json.close()
del path_json

login_data = data['login']
path_data = data['path']
list_ID = data['listId']

passenger = Passenger(
    passenger_data['Email'],
    passenger_data['Mobile'],
    passenger_data['People'],
    passenger_data['Phone']
)
del passenger_data

user = User(login_data['username'], login_data['password'], login_data['mobile'], login_data['email'])
mr_bilit = MrBilitApiWrapper()

while True:
    try:
        i = 0
        while not mr_bilit.get_available(path_data['source'], path_data['destination'], path_data['date'], path_data['sex'],
                                         list_ID):
            i += 1
            print(i, " not found please wait!")
            time.sleep(20)
        print("found")
        mr_bilit.login(user.get_username(), user.get_password(), user.get_mobile())
        mr_bilit.reserve_seat()
        mr_bilit.register_info(passenger)
        mr_bilit.pay()
        while not mr_bilit.get_status():
            time.sleep(3)
        mr_bilit.get_pdf()
        break
    except:
        time.sleep(20)
