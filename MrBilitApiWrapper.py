import json
import requests

from Passenger import Passenger
from LogTrain import LogTrain
from GlobalVariable import Sex
from helper.DateFunctions import j_to_g
from helper.SexFunctions import int_to_sex_enum, sex_enum_to_int
from helper.validation import validation_mobile
import urllib.parse


def generate_query_get_available(source: str, destination: str, date: str) -> str:
    query: str = ""
    query += "from=" + urllib.parse.quote(source) + '&'
    query += "to=" + urllib.parse.quote(destination) + '&'
    query += "date=" + urllib.parse.quote(j_to_g(date)) + '&'
    query += "adultCount=" + "1" + '&'
    query += "childCount=" + "0" + '&'
    query += "infantCount=" + "0" + '&'
    query += "exclusive=" + "false" + '&'
    query += "availableStatus=" + "Both"
    return query


def generate_query_reserve_seat(trainID: int | str, adultCount: int | str, childCount: int | str,
                                infantCount: str | int):
    query: str = ""
    query += "trainID=" + urllib.parse.quote(str(trainID)) + '&'
    query += "adultCount=" + urllib.parse.quote(str(adultCount)) + '&'
    query += "childCount=" + urllib.parse.quote(str(childCount)) + '&'
    query += "infantCount=" + urllib.parse.quote(str(infantCount)) + '&'
    query += "includeOptionalServices=" + "true" + '&'
    query += "exclusive=" + "false" + '&'
    query += "genderCode=" + "3" + '&'
    query += "seatCount=" + "1"
    return query


def generate_query_login(Username: int | str, Password: int | str, Mobile: str | int):
    Mobile = validation_mobile(Mobile)
    query: str = ""
    query += "Username=" + urllib.parse.quote(str(Username)) + '&'
    query += "Password=" + urllib.parse.quote(str(Password)) + '&'
    query += "Mobile=" + urllib.parse.quote(str(Mobile)) + '&'
    query += "Source=" + "2"
    return query


class MrBilitApiWrapper:
    __train: dict | None = None
    __listOfTrain: list = []
    __sex: Sex | None = None
    __classesTrain: dict | None = None
    __res_s: dict | None = None
    __reg_s: dict | None = None
    __token: str = ""
    __mac: str = ""
    __billCode: str | int = ""
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
                self.__listOfTrain.append(train)

    def __set_train(self, listTrainId: list[int | str]) -> bool:
        if not self.__listOfTrain:
            return False

        if len(self.__listOfTrain) == 0:
            return False

        for Id in listTrainId:
            if Id == 0:
                self.__train = self.__listOfTrain[0]
                for Price in self.__train['Prices']:
                    if Price['SellType'] == sex_enum_to_int(self.__sex):
                        self.__classesTrain = Price['Classes']
                return True
            for train in self.__listOfTrain:
                if str(Id) == str(train['TrainNumber']):
                    self.__train = train
                    for Price in self.__train['Prices']:
                        if Price['SellType'] == sex_enum_to_int(self.__sex):
                            self.__classesTrain = Price['Classes']
                    return True
        return False

    def reserve_seat(self):
        query = generate_query_reserve_seat(self.__classesTrain[0]["ID"], 1, 0, 0)
        res_req = requests.get('https://train.atighgasht.com/TrainService/api/ReserveSeat?' + query,
                               headers={'Authorization': 'Bearer ' + self.__token})
        cookies = res_req.cookies
        self.__res_s = json.loads(res_req.text)
        print("reserve_seat", self.__res_s)

    def register_info(self, passenger: Passenger):
        REG = 'https://train.atighgasht.com/TrainService/api/RegisterInfo'
        reg_req = requests.post(REG, json=passenger.get_dict(self.__res_s['BillID']),
                                headers={'Authorization': 'Bearer ' + self.__token})
        self.__reg_s = json.loads(reg_req.text)
        print("register_info", self.__reg_s)

    def login(self, Username: int | str, Password: int | str, Mobile: str | int):
        login_req = requests.get(
            'https://auth.mrbilit.com/api/login?' + generate_query_login(Username, Password, Mobile))
        login_data = json.loads(login_req.text)
        print("login", login_data)
        self.__token = login_data['token']

    def pay(self):
        query = 'https://payment.mrbilit.com/api/billpayment/' + str(self.__res_s['BillCode']) + \
                '?payFromCredit=true&access_token=' + self.__token
        pay_status = requests.get(query, headers={'Authorization': 'Bearer ' + self.__token})
        print("pay", pay_status.url)
        parsed_url = urllib.parse.urlparse(pay_status.url)
        queries = urllib.parse.parse_qs(parsed_url.query)
        self.__mac = queries['mac'][0]
        self.__billCode = queries['billCode'][0]

    def get_status(self) -> bool:
        status = requests.get(
            "https://finalize.mrbilit.com/api/workflow/bill/" + str(self.__billCode) + "/status?mac=" + self.__mac)
        print("status", status.text)
        self.__status = json.loads(status.text)
        return len(self.__status["ticketFiles"]) > 0

    def get_pdf(self):
        print("list of blit:")
        for ticketFile in self.__status["ticketFiles"]:
            print(ticketFile["url"])
