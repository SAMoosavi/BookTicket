import json
import requests

from Passenger import Passenger
from LogTrain import LogTrain
from User import User
from helper.DateFunctions import jalali_to_gregorian
import urllib.parse


class MrBilitApiWrapper:
    __token: str = ""
    __headers = {}

    def __init__(self, user: User):
        self.__login(user)

    def __login(self, user: User):
        login_req = requests.get('https://auth.mrbilit.com/api/login', params={
            "Username": user.username,
            "Password": user.password,
            "Mobile": user.mobile,
            "Source": 2
        })
        login_data = json.loads(login_req.text)
        print("login", login_data)
        self.__token = login_data['token']
        self.__headers = {'Authorization': 'Bearer ' + login_data['token']}

    def get_available(self, source: str, destination: str, date: str, sex: int):
        response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2", params={
            "from": source,
            "to": destination,
            "date": jalali_to_gregorian(date),
            "adultCount": 1,
            "childCount": 0,
            "infantCount": 0,
            "exclusive": False,
            "availableStatus": "Both"
        }).text
        return self.__get_list_of_train(json.loads(response), sex)

    def __get_list_of_train(self, data, sex: int):
        list_of_train = []
        if 'Trains' not in data:
            return list_of_train
        trains = data['Trains']
        LogTrain().write(trains)

        for train in trains:
            capacity: int = 0

            for b in train['Prices']:
                if b['SellType'] == sex:
                    for c in b['Classes']:
                        capacity = c['Capacity']
                    break

            if not capacity == 0:
                list_of_train.append(train)

        return list_of_train

    def reserve_seat(self, train_ID, adult_count, child_count, infant_count):
        reserve_requests = requests.get('https://train.atighgasht.com/TrainService/api/ReserveSeat',
                                        params={
                                            "trainID": train_ID,
                                            "adultCount": adult_count,
                                            "childCount": child_count,
                                            "infantCount": infant_count,
                                            "includeOptionalServices": True,
                                            "exclusive": False,
                                            "genderCode": "3",
                                            "seatCount": "1"
                                        },
                                        headers=self.__headers)
        reserve_data = json.loads(reserve_requests.text)
        print("reserve_seat", reserve_data)
        return reserve_data

    def register_info(self, bill_ID, passenger: Passenger):
        register_request = requests.post('https://train.atighgasht.com/TrainService/api/RegisterInfo',
                                         json=passenger.get_dict(bill_ID),
                                         headers=self.__headers)
        register_data = json.loads(register_request.text)
        print("register_info", register_data)

    def pay(self, bill_code):
        pay_status = requests.get('https://payment.mrbilit.com/api/billpayment/' + str(bill_code),
                                  params={
                                      "payFromCredit": True,
                                      "access_token": self.__token
                                  },
                                  headers=self.__headers)
        print("pay", pay_status.url)
        parsed_url = urllib.parse.urlparse(pay_status.url)
        queries = urllib.parse.parse_qs(parsed_url.query)
        return queries['mac'][0]

    def get_status(self, bill_code, mac):
        status = requests.get(
            "https://finalize.mrbilit.com/api/workflow/bill/" + str(bill_code) + "/status"
            , params={"mac": mac}
        ).text
        print("status", status)
        status = json.loads(status)
        return status["ticketFiles"]
