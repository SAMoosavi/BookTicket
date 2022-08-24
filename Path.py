import json

import jdatetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from LogTrain import LogTrain
from globalVariable import Sex


def sex_switch(sex: Sex):
    if Sex.MAN == sex:
        return "Man"
    elif Sex.WOMAN == sex:
        return "Woman"
    elif Sex.BOTH == sex:
        return "Both"
    else:
        raise "sex isn in Sex Enum"


def sex_enum_to_int(sex: Sex) -> int:
    if Sex.MAN == sex:
        return 1
    elif Sex.WOMAN == sex:
        return 2
    elif Sex.BOTH == sex:
        return 3
    else:
        raise "sex isn in Sex Enum"


def j_to_g(date: str, spliter='/') -> str:
    splitDate: list[str] = date.split(spliter)
    return str(jdatetime.date(day=int(splitDate[2]), month=int(splitDate[1]), year=int(splitDate[0])).togregorian())


def get_query(beginning: str, ending: str, date: str) -> str:
    query: str = ""
    query += "from=" + beginning + '&'
    query += "to=" + ending + '&'
    query += "date=" + j_to_g(date) + '&'
    query += "adultCount=" + "1" + '&'
    query += "childCount=" + "0" + '&'
    query += "infantCount=" + "0" + '&'
    query += "exclusive=" + "false" + '&'
    query += "availableStatus=" + "Both"
    return query


class Path:
    __train: dict | None = None
    __listOfTrain: list | None = None
    __sex: Sex | None = None
    __classesTrain: list[dict] | None = None

    def is_free(self, beginning: str, ending: str, date: str, sex: Sex, listTrainId: list[int | str]) -> bool:
        self.__sex = sex
        query = get_query(beginning, ending, date)
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
        if len(self.__listOfTrain) == 0:
            return False

        for Id in listTrainId:
            if Id == 0:
                return True
            for train in self.__listOfTrain:
                if str(Id) == str(train['TrainNumber']):
                    self.__train = train
                    for Price in self.__train['Prices']:
                        if Price['SellType'] == sex_enum_to_int(self.__sex):
                            self.__classesTrain = Price['Classes']
                    return True

        return False

    def find_ticket(self, tickets: list[WebElement]) -> WebElement:
        if not self.__train:
            return tickets[0]

        tickets = self.__tickets_correct_time(tickets)
        if len(tickets) == 1:
            return tickets[0]

        tickets = self.__tickets_correct_corporation_name(tickets)
        if len(tickets) == 1:
            return tickets[0]

        tickets = self.__tickets_correct_wagon_name(tickets)
        if len(tickets) == 1:
            return tickets[0]

        tickets = self.__tickets_correct_price(tickets)
        if len(tickets) == 1:
            return tickets[0]

        raise ":("

    def __tickets_correct_time(self, tickets: list[WebElement]) -> list[WebElement]:
        result: list[WebElement] = []
        for ticket in tickets:
            if self.__is_ticket_with_time(ticket):
                result.append(ticket)
        return result

    def __is_ticket_with_time(self, ticket: WebElement) -> bool:
        DepartureTime = ticket.find_element(By.XPATH, "//div/section[1]/div[1]/section/div[1]/div[1]").text

        if DepartureTime not in self.__train['DepartureTime']:
            return False

        ArrivalTime = ticket.find_element(By.XPATH, "//div[1]/section[1]/div[1]/section/div[3]/div[1]").text
        if ArrivalTime not in self.__train['ArrivalTime']:
            return False

        return True

    def __tickets_correct_corporation_name(self, tickets: list[WebElement]) -> list[WebElement]:
        result: list[WebElement] = []
        for ticket in tickets:
            if self.__is_ticket_with_corporation_name(ticket):
                result.append(ticket)
        return result

    def __is_ticket_with_corporation_name(self, ticket: WebElement) -> bool:
        CorporationName = ticket.find_element(By.XPATH, "//div/section[1]/div[1]/div/div[2]/p[1]").text
        return CorporationName in self.__train['CorporationName']

    def __tickets_correct_wagon_name(self, tickets: list[WebElement]) -> list[WebElement]:
        result: list[WebElement] = []
        for ticket in tickets:
            if self.__is_ticket_with_wagon_name(ticket):
                result.append(ticket)
        return result

    def __is_ticket_with_wagon_name(self, ticket: WebElement) -> bool:
        wagonName = ticket.find_element(By.XPATH, "//div/section[1]/div[2]/div[2]/span").text
        for classTrain in self.__classesTrain:
            if classTrain['Capacity'] > 0:
                if wagonName in classTrain['WagonName']:
                    return True
        return False

    def __tickets_correct_price(self, tickets: list[WebElement]) -> list[WebElement]:
        result: list[WebElement] = []
        for ticket in tickets:
            if self.__is_ticket_with_price(ticket):
                result.append(ticket)
        return result

    def __is_ticket_with_price(self, ticket: WebElement) -> bool:
        price = ticket.find_element(By.XPATH, "//div/section[2]/div[2]/div").text
        for classTrain in self.__classesTrain:
            if classTrain['Capacity'] > 0:
                if price in classTrain['Price']:
                    return True

        return False
