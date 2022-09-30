import json
import requests

from Passenger import Passenger
from LogTrain import LogTrain
from GlobalVariables import Sex
from helper.DateFunctions import jalali_to_gregorian
from helper.SexFunctions import int_to_sex_enum, sex_enum_to_int
from helper.validation import validation_mobile
import urllib.parse


class MrBilitApiWrapper:
    __train: dict | None = None
    __list_of_train: list = []
    __sex: Sex | None = None
    __classes_train: dict | None = None
    __reserve_data: dict | None = None
    __register_data: dict | None = None
    __token: str = ""
    __mac: str = ""
    __bill_code: str | int = ""
    __status: dict = {}

    __headers = {}

    def __init__(self, Username: int | str, Password: int | str, Mobile: str | int):
        self.__login(Username, Password, Mobile)

    def __login(self, Username: int | str, Password: int | str, Mobile: str | int):
        login_req = requests.get('https://auth.mrbilit.com/api/login', params={
            "Username": Username,
            "Password": Password,
            "Mobile": Mobile,
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
        params = {
            "trainID": train_ID,
            "adultCount": adult_count,
            "childCount": child_count,
            "infantCount": infant_count,
            "includeOptionalServices": True,
            "exclusive": "3",
            "seatCount": "1"
        }
        reserve_requests = requests.get('https://train.atighgasht.com/TrainService/api/ReserveSeat',
                                        params=params,
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

    def get_status(self) -> bool:
        status = requests.get(
            "https://finalize.mrbilit.com/api/workflow/bill/" + str(self.__bill_code) + "/status?mac=" + self.__mac)
        print("status", status.text)
        self.__status = json.loads(status.text)
        return len(self.__status["ticketFiles"]) > 0

    def get_pdf(self):
        print("list of blit:")
        for ticket_file in self.__status["ticketFiles"]:
            print(ticket_file["url"])
