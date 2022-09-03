import json
import time
import requests
import jdatetime
from selenium.webdriver.common.by import By

from globalClass.CompleteForms import CompleteForms
from globalClass.LogTrain import LogTrain
from globalClass.globalVariable import cities, months
from helper.DateFunctions import j_to_g
from v1.BookTicket import BookTicket


# CompleteForms
class MrBilitBookTicket(BookTicket, CompleteForms):
    __URL: str = "https://mrbilit.com/train-ticket"

    __cities: dict = cities
    __month: dict = months

    __hasTo: bool = False

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # Login
    def login(self, data):
        self.__go_to_login_form()
        self.complete_input_form(data['username'], "phonenumber")
        self.click_btn("login-btn-step1")
        self.complete_input_form(data['password'], "//input[@type='password']", By.XPATH)
        self.click_btn("//form/div[4]/button[2]", By.XPATH)
        try:
            self.__close_login_form()
        except:
            pass

    def __close_login_form(self):
        self.click_btn("/html/body/div[2]/div/div/div[2]/div/span/span", By.XPATH)

    def __go_to_login_form(self):
        self.click_btn("//header/nav/ul/li[3]/div", By.XPATH)

    # search
    __fromTime: str = ""
    __toTime: str = ""

    def search(self, data):
        if data['groupWay'] == 1:
            self.__hasTo = True
        self.__complete_form_search(data)
        self.__btn_search()
        self.__set_train()
        self.__btn_verify()

    def super_search(self, data, listId):
        if data['groupWay'] == 1:
            self.__hasTo = True
        self.__first_search(data, listId)
        self.__complete_form_search(data)
        self.__btn_search()
        self.__set_train()
        self.__btn_verify()

    def __btn_verify(self):
        r = self.wait_and_return("/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[8]/button[2]", By.XPATH)
        r.location_once_scrolled_into_view
        time.sleep(0.5)
        r.click()

    def __set_train(self):
        self.__min_train()
        self.__click_ticket(self.__fromTime)
        if self.__hasTo:
            self.__min_train()
            self.__click_ticket(self.__toTime)

    def __click_ticket(self, dataTime: str):
        num = 1
        if dataTime != "":
            r = self.wait_and_returns("/html/body/div/div/div/div[2]/div[3]/div/section[1]/div/*", By.XPATH)
            for i in range(1, len(r) + 1):
                try:
                    a = self.wait_and_return(
                        "/html/body/div/div/div/div[2]/div[3]/div/section[1]/div/div["
                        + str(i) +
                        "]/div/section[1]/div[1]/section/div[1]/div[1]",
                        By.XPATH)
                    if a.text in dataTime:
                        num = i
                        break
                except:
                    continue
        self.click_btn(
            "/html/body/div/div/div/div[2]/div[3]/div/section[1]/div/div["
            + str(num) +
            "]/div/section[2]/div[2]/button",
            By.XPATH)

    def __min_train(self):
        self.click_btn("/html/body/div/div/div/div[2]/div[3]/aside/div/div[4]/div[1]/div/div[2]/div[1]/div/label[2]",
                       By.XPATH)
        time.sleep(1)

    def __btn_search(self):
        self.click_btn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[4]/button", By.XPATH)

    def __complete_form_search(self, data):
        self.__wagon(data['wagon'])
        self.__group_way(data['groupWay'])
        self.__from(data['from'])
        self.__to(data['to'])
        self.__open_date()
        self.__date(data['fromd'])
        if self.__hasTo:
            self.__date(data['tod'])
        self.__set_date()
        self.__traveler(data['adult'], data['child'], data['infant'])
        self.__sex(data['sex'])

    def __sex(self, data):
        if data == "1":
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[3]",
                By.XPATH)
        elif data == "2":
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[2]",
                By.XPATH)
        elif data == "3":
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[1]",
                By.XPATH)

    def __traveler(self, adult, child, infant):
        self.click_btn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[1]/div/label", By.XPATH)
        for i in range(1, int(adult)):
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/button[2]",
                By.XPATH)
        for i in range(0, int(child) + int(infant)):
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/button[2]",
                By.XPATH)

    def __set_date(self):
        self.click_btn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[3]/div[2]/button[2]",
            By.XPATH)

    def __date(self, data):
        date: list[str] = data.split('/')
        day: str = date[2] if not date[2][0] == "0" else date[2][1]
        index = "1" if self.__month[date[1]] in self.wait_and_return(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]",
            By.XPATH).text else "2"
        self.wait_and_returns(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div["
            + index +
            "]/div[3]/div[not(contains(@class, 'empty'))]",
            By.XPATH)[int(day) - 1].click()

    def __open_date(self):
        self.click_btn("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[1]/div[1]", By.XPATH)

    def __to(self, data):
        city = self.__get_city(data)
        self.complete_input_form(city,
                                 "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[1]/div/label/input",
                                 By.XPATH)
        time.sleep(1)
        self.click_btn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div",
            By.XPATH)

    def __from(self, data):
        city = self.__get_city(data)
        inp = self.wait_and_return(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div/div[1]/div/label/input",
            By.XPATH)
        inp.location_once_scrolled_into_view
        inp.send_keys(city)
        time.sleep(1)
        self.click_btn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div",
            By.XPATH)

    def __get_city(self, date) -> str:
        return self.__cities[date]

    def __group_way(self, data):
        if data == 1:
            self.click_btn("/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/label[2]", By.XPATH)
        else:
            self.click_btn("/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/label[1]", By.XPATH)

    def __wagon(self, data):
        if data == "1":
            self.click_btn("/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[1]/label", By.XPATH)

    def __first_search(self, data, listId):
        findFrom: bool = False
        while not findFrom:
            query: str = self.__get_query(data, True)
            response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
            findFrom = self.__get_train(response, listId[0], True)
        if self.__hasTo:
            findFrom: bool = False
            while not findFrom:
                query: str = self.__get_query(data, False)
                response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
                findFrom = self.__get_train(response, listId[1], False)

    def __get_train(self, data, listId, isFrom: bool) -> bool:
        unavailables: list = []
        availables: list = []
        enCodedData = json.loads(data)
        if not 'Trains' in enCodedData:
            return False
        trains = enCodedData['Trains']
        LogTrain().write(trains)
        for train in trains:
            capacity: int = 0
            for b in train['Prices'][0]['Classes']:
                capacity += b['Capacity']

            if not capacity == 0:
                availables.append(train)
            else:
                unavailables.append(train)
        for Id in listId:
            if Id == 0:
                break
            for available in availables:
                if Id == available['TrainNumber']:
                    if isFrom:
                        self.__fromTime = available['DepartureTime']
                    else:
                        self.__toTime = available['DepartureTime']
                    return True
        if listId[-1] == 0 and len(availables) > 0:
            return True
        return False

    def __get_query(self, data, isFrom: bool) -> str:
        query: str = ""
        query += "from=" + (data['from'] if isFrom else data['to']) + '&'
        query += "to=" + (data['to'] if isFrom else data['from']) + '&'
        query += "date=" + j_to_g(data['fromd'] if isFrom else data['tod']) + '&'
        query += "adultCount=" + data['adult'] + '&'
        query += "childCount=" + data['child'] + '&'
        query += "infantCount=" + data['infant'] + '&'
        query += "exclusive=" + ("false" if data['wagon'] == "0" else "true") + '&'
        query += "availableStatus=" + "Both"
        return query

    # setUsers
    def set_users(self, dataUsers):
        hasService: bool = True
        for i in range(1, len(dataUsers) + 1):
            hasService = self.__set_user(i, dataUsers[i - 1], hasService)
        self.__set_users_btn()

    def __set_users_btn(self):
        r = self.wait_and_return('form-next-button')
        r.location_once_scrolled_into_view
        time.sleep(0.5)
        r.click()

    def __set_user(self, i, data, hasService):
        baseLocation = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[" + str(i) + "]"
        self.wait_and_return(baseLocation, By.XPATH).location_once_scrolled_into_view
        time.sleep(0.5)
        self.__set_first_name(baseLocation, data['FName'])
        self.__set_last_name(baseLocation, data['LName'])
        self.__set_sex(baseLocation, data['sex'])
        self.__set_ID(baseLocation, data['id'])
        self.__set_birthday(baseLocation, data['birthday'])
        try:
            if hasService:
                self.__set_service(baseLocation, data['service'])
                return True
        except:
            return False

    def __set_service(self, baseLocation, data):
        if data is None or data == "":
            r = self.wait_and_return(baseLocation + "/div/form/span/div/div[1]/div[2]/label", By.XPATH, 1)
            r.click()
        else:
            self.complete_input_form(data, baseLocation + "/div/form/span/div/div[1]/div[2]/label/input", By.XPATH, 1)
        time.sleep(1)
        self.click_btn(baseLocation + "/div/form/span/div/div[2]/div/div/div[2]/div[1]", By.XPATH, 1)

    def __set_birthday(self, baseLocation, data):
        self.__set_day(baseLocation, data['day'])
        self.__set_month(baseLocation, data['month'])
        self.__set_year(baseLocation, data['year'])

    def __set_year(self, baseLocation, data):
        data = "13" + data
        self.complete_input_form(data,
                                 baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[3]/div[1]/div[2]/label/input",
                                 By.XPATH)
        time.sleep(1)
        self.click_btn(baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[3]/div[2]/div/div/div[2]/div", By.XPATH)

    def __set_month(self, baseLocation, data):
        if data[0] == "0":
            data = data[1:]
        self.click_btn(baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/label", By.XPATH)
        self.click_btn(
            baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[2]/div[2]/div/div/div[2]/div["
            + data +
            "]",
            By.XPATH)

    def __set_day(self, baseLocation, data):
        if data[0] == "0":
            data = data[1:]
        self.complete_input_form(data,
                                 baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[1]/div[1]/div[2]/label/input",
                                 By.XPATH)
        time.sleep(1)
        self.click_btn(baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[1]/div[2]/div/div/div[2]/div", By.XPATH)

    def __set_ID(self, baseLocation, data):
        self.complete_input_form(data, baseLocation + "/div/form/div[4]/div[2]/label/input", By.XPATH)

    def __set_last_name(self, baseLocation, data):
        self.complete_input_form(data, baseLocation + "/div/form/div[3]/div[2]/label/input", By.XPATH)

    def __set_first_name(self, baseLocation, data):
        self.complete_input_form(data, baseLocation + "/div/form/div[2]/div[2]/label/input", By.XPATH)

    def __set_sex(self, baseLocation, data):
        location = (baseLocation + "/div/form/div[1]/span[1]/div/div[1]/div")
        if data == "2" or data == 2:
            self.click_btn(location + "/label[1]", By.XPATH)
        elif data == "1" or data == 1:
            self.click_btn(location + "/label[2]", By.XPATH)

    # buy
    def buy(self):
        self.__credentials()
        self.__click_buy()

    def __credentials(self):
        r = self.wait_and_return("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/label", By.XPATH)
        r.location_once_scrolled_into_view
        time.sleep(0.5)
        r.click()

    def __click_buy(self):
        self.click_btn("btnAccept")
        time.sleep(30)
