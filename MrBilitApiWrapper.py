import json
import time

import requests

from GlobalVariables import Sex
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
        while True:
            try:
                login_req = requests.get('https://auth.mrbilit.com/api/login', params={
                    "Username": user.username,
                    "Password": user.password,
                    "Mobile": user.mobile,
                    "Source": 2
                })
                break
            except:
                pass
        login_data = json.loads(login_req.text)
        # print("login", login_data)
        self.__token = login_data['token']
        self.__headers = {'Authorization': 'Bearer ' + login_data['token']}

    def get_available(self, source: str, destination: str, date: str, sex: Sex):
        while True:
            try:
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
                break
            except:
                print("err")
                time.sleep(20)
        return self.__get_list_of_train(json.loads(response), sex)

    def __get_list_of_train(self, data, sex: Sex):
        print("data", data)
        if 'Trains' not in data:
            return []
        list_of_train = [
            train for train in data['Trains']
            if any(
                c['Capacity'] > 0
                for b in train['Prices']
                for c in b['Classes']
                if b['SellType'] == sex.value
            )
        ]

        LogTrain().write(list_of_train)
        return list_of_train

    def reserve_seat(self, train_ID, sex: Sex):
        while True:
            try:
                reserve_requests = requests.get('https://train.atighgasht.com/TrainService/api/ReserveSeat',
                                                params={
                                                    "trainID": train_ID,
                                                    "adultCount": "1",
                                                    "childCount": "0",
                                                    "infantCount": "0",
                                                    "includeOptionalServices": True,
                                                    "exclusive": False,
                                                    "genderCode": sex.value,
                                                    "seatCount": "1"
                                                },
                                                headers=self.__headers)
                break
            except:
                print("err")
                time.sleep(20)
        reserve_data = json.loads(reserve_requests.text)
        print("reserve_seat", reserve_data)
        return reserve_data

    def __get_dict(self, passenger: Passenger, bill_ID) -> dict:
        return {
            "Email": passenger.email,
            "Mobile": passenger.mobile,
            "People": [
                {
                    "PersianFirstName": passenger.persian_first_name,
                    "PersianLastName": passenger.persian_last_name,
                    "Male": passenger.male,
                    "BirthDay": jalali_to_gregorian(passenger.birth_day),
                    "NationalCode": passenger.national_code,
                    "TrainCars": passenger.train_cars,
                    "TrainCapacityOptionalService": passenger.train_capacity_optional_service
                }
            ],
            "Phone": passenger.phone,
            "BillID": bill_ID
        }

    def register_info(self, bill_ID, passenger: Passenger):
        while True:
            try:
                register_request = requests.post('https://train.atighgasht.com/TrainService/api/RegisterInfo',
                                                 json=self.__get_dict(passenger, bill_ID),
                                                 headers=self.__headers)
                break
            except:
                print("err")
                # time.sleep(20)
        register_data = json.loads(register_request.text)
        print("register_info", register_data)

    def pay(self, bill_code):
        while True:
            try:
                pay_status = requests.get('https://payment.mrbilit.com/api/billpayment/' + str(bill_code),
                                          params={
                                              "payFromCredit": True,
                                              "access_token": self.__token
                                          },
                                          headers=self.__headers)
                break
            except:
                print("err")
                # time.sleep(20)
        print("pay", pay_status.url)
        parsed_url = urllib.parse.urlparse(pay_status.url)
        queries = urllib.parse.parse_qs(parsed_url.query)
        return queries['mac'][0]

    def get_status(self, bill_code, mac):
        while True:
            try:
                status = requests.get(
                    "https://finalize.mrbilit.com/api/workflow/bill/" + str(bill_code) + "/status"
                    , params={"mac": mac}
                ).text
                break
            except:
                print("err")
                # time.sleep(20)
        print("status", status)
        status = json.loads(status)
        return status["ticketFiles"]
