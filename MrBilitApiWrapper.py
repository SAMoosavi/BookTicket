import json
import requests

from Passenger import Passenger
from LogTrain import LogTrain
from GlobalVariables import Sex
from helper.DateFunctions import jalali_to_gregorian
from helper.SexFunctions import int_to_sex_enum, sex_enum_to_int
from helper.validation import validation_mobile
import urllib.parse


def generate_query_get_available(source: str, destination: str, date: str) -> str:
    query: str = ""
    query += "from=" + urllib.parse.quote(source) + '&'
    query += "to=" + urllib.parse.quote(destination) + '&'
    query += "date=" + urllib.parse.quote(jalali_to_gregorian(date)) + '&'
    query += "adultCount=" + "1" + '&'
    query += "childCount=" + "0" + '&'
    query += "infantCount=" + "0" + '&'
    query += "exclusive=" + "false" + '&'
    query += "availableStatus=" + "Both"
    return query


def generate_query_reserve_seat(train_ID: int | str, adult_count: int | str, child_count: int | str,
                                infant_count: str | int):
    query: str = ""
    query += "trainID=" + urllib.parse.quote(str(train_ID)) + '&'
    query += "adultCount=" + urllib.parse.quote(str(adult_count)) + '&'
    query += "childCount=" + urllib.parse.quote(str(child_count)) + '&'
    query += "infantCount=" + urllib.parse.quote(str(infant_count)) + '&'
    query += "includeOptionalServices=" + "true" + '&'
    query += "exclusive=" + "false" + '&'
    query += "genderCode=" + "3" + '&'
    query += "seatCount=" + "1"
    return query


def generate_query_login(username: int | str, password: int | str, mobile: str | int):
    mobile = validation_mobile(mobile)
    query: str = ""
    query += "Username=" + urllib.parse.quote(str(username)) + '&'
    query += "Password=" + urllib.parse.quote(str(password)) + '&'
    query += "Mobile=" + urllib.parse.quote(str(mobile)) + '&'
    query += "Source=" + "2"
    return query


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

    def get_available(self, source: str, destination: str, date: str, sex: int, listTrainId: list[int | str]) -> bool:
        self.__sex = int_to_sex_enum(sex)
        query = generate_query_get_available(source, destination, date)
        response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
        self.__get_list_of_train(json.loads(response))
        return self.__set_train(listTrainId)

    def __get_list_of_train(self, data) -> None:
        if 'Trains' not in data:
            return
        trains = data['Trains']
        LogTrain().write(trains)
        for train in trains:
            capacity: int = 0
            for b in train['Prices']:
                if b['SellType'] == sex_enum_to_int(self.__sex):
                    for c in b['Classes']:
                        capacity += c['Capacity']
                    break

            if not capacity == 0:
                self.__list_of_train.append(train)

    def __set_train(self, list_train_ID: list[int | str]) -> bool:
        if not self.__list_of_train:
            return False

        if len(self.__list_of_train) == 0:
            return False

        for ID in list_train_ID:
            if ID == 0:
                self.__train = self.__list_of_train[0]
                for price in self.__train['Prices']:
                    if price['SellType'] == sex_enum_to_int(self.__sex):
                        self.__classes_train = price['Classes']
                return True
            for train in self.__list_of_train:
                if str(ID) == str(train['TrainNumber']):
                    self.__train = train
                    for price in self.__train['Prices']:
                        if price['SellType'] == sex_enum_to_int(self.__sex):
                            self.__classes_train = price['Classes']
                    return True
        return False

    def reserve_seat(self):
        query = generate_query_reserve_seat(self.__classes_train[0]["ID"], 1, 0, 0)
        reserve_requests = requests.get('https://train.atighgasht.com/TrainService/api/ReserveSeat?' + query,
                                        headers={'Authorization': 'Bearer ' + self.__token})
        cookies = reserve_requests.cookies
        self.__reserve_data = json.loads(reserve_requests.text)
        print("reserve_seat", self.__reserve_data)

    def register_info(self, passenger: Passenger):
        register_request = requests.post('https://train.atighgasht.com/TrainService/api/RegisterInfo',
                                         json=passenger.get_dict(self.__reserve_data['BillID']),
                                         headers={'Authorization': 'Bearer ' + self.__token})
        self.__register_data = json.loads(register_request.text)
        print("register_info", self.__register_data)

    def login(self, Username: int | str, Password: int | str, Mobile: str | int):
        login_req = requests.get(
            'https://auth.mrbilit.com/api/login?' + generate_query_login(Username, Password, Mobile))
        login_data = json.loads(login_req.text)
        print("login", login_data)
        self.__token = login_data['token']

    def pay(self):
        query = 'https://payment.mrbilit.com/api/billpayment/' + str(self.__reserve_data['BillCode']) + \
                '?payFromCredit=true&access_token=' + self.__token
        pay_status = requests.get(query, headers={'Authorization': 'Bearer ' + self.__token})
        print("pay", pay_status.url)
        parsed_url = urllib.parse.urlparse(pay_status.url)
        queries = urllib.parse.parse_qs(parsed_url.query)
        self.__mac = queries['mac'][0]
        self.__bill_code = queries['billCode'][0]

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
