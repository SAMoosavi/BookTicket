import json
import time
import requests
import jdatetime
from BookTicket import BookTicket
from CompleteForms import CompleteForms
from selenium.webdriver.common.by import By
from globalVariable import cities


class LogTrain:
    __unavailable: list
    __available: list

    def __init__(self, unavailable, available):
        self.__unavailable = unavailable
        self.__available = available


# CompleteForms
class MrBilitBookTicket(BookTicket, CompleteForms):
    __URL: str = "https://mrbilit.com/train-ticket"

    __cities: dict = cities

    __hasTo: bool = False

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # Login
    def login(self, data):
        self.__goToLoginForm()
        self.completeInputForm(data['username'], "phonenumber")
        self.clickBtn("login-btn-step1")
        self.completeInputForm(data['password'], "//input[@type='password']", By.XPATH)
        self.clickBtn("//form/div[4]/button[2]", By.XPATH)
        try:
            self.__closeLoginForm()
        except:
            pass

    def __closeLoginForm(self):
        self.clickBtn("/html/body/div[2]/div/div/div[2]/div/span/span", By.XPATH)

    def __goToLoginForm(self):
        self.clickBtn("//header/nav/ul/li[3]/div", By.XPATH)

    # search
    __fromTime: str = ""
    __toTime: str = ""

    def search(self, data):
        pass

    def search(self, data, listId):
        if data['groupWay'] == 1:
            self.__hasTo = True
        self.__firstSearch(data, listId)
        self.__completeFormSearch(data)
        self.__btnSearch()

    def __btnSearch(self):
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[4]/button", By.XPATH)

    def __completeFormSearch(self, data):
        time.sleep(1)
        self.__wagon(data['wagon'])
        self.__groupWay(data['groupWay'])
        self.__from(data['from'])
        self.__to(data['to'])
        self.__openDate()
        self.__date(data['fromd'])
        if self.__hasTo:
            self.__date(data['tod'])
        self.__setDate()
        self.__traveler(data['adult'], data['child'], data['infant'])
        self.__sex(data['sex'])

    def __sex(self, data):
        if data == "1":
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[3]",
                By.XPATH)
        elif data == "2":
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[2]",
                By.XPATH)
        elif data == "3":
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[1]",
                By.XPATH)

    def __traveler(self, adult, child, infant):
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[1]/div/label", By.XPATH)
        for i in range(1, int(adult)):
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/button[2]",
                By.XPATH)
        for i in range(0, int(child) + int(infant)):
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/button[2]",
                By.XPATH)

    def __setDate(self):
        self.clickBtn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[3]/div[2]/button[2]",
            By.XPATH)

    def __date(self, data):
        date = data.split('/')
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[3]/div["
            + date[2] + "]",
            By.XPATH)

    def __openDate(self):
        self.clickBtn("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[1]/div[1]", By.XPATH)

    def __to(self, data):
        city = self.__getCity(data)
        self.completeInputForm(city,
                               "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[1]/div/label/input",
                               By.XPATH)
        time.sleep(0.5)
        self.clickBtn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div",
            By.XPATH)

    def __from(self, data):
        city = self.__getCity(data)
        inp = self.wait_and_return(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div/div[1]/div/label/input",
            By.XPATH)
        inp.location_once_scrolled_into_view
        inp.send_keys(city)
        time.sleep(0.5)
        self.clickBtn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div",
            By.XPATH)

    def __getCity(self, date) -> str:
        return self.__cities[date]

    def __groupWay(self, data):
        if data == 1:
            self.clickBtn("/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/label[2]", By.XPATH)
        else:
            self.clickBtn("/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/label[1]", By.XPATH)

    def __wagon(self, data):
        if data == "1":
            self.clickBtn("/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[1]/label", By.XPATH)

    def __firstSearch(self, data, listId):
        findFrom: bool = False
        while findFrom:
            query: str = self.__getQuery(data, True)
            response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
            findFrom = self.__getTrain(response, listId, True)
        if self.__hasTo:
            findFrom: bool = False
            while findFrom:
                query: str = self.__getQuery(data, False)
                response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
                findFrom = self.__getTrain(response, listId, False)

    def __getTrain(self, data, listId, isFrom: bool) -> bool:
        unavailables: list = []
        availables: list = []
        for a in json.loads(data)['Trains']:
            capacity: int = 0
            for b in a['Prices'][0]['Classes']:
                capacity += b['Capacity']

            if not capacity == 0:
                availables.append(a)
            else:
                unavailables.append(a)
        LogTrain(unavailables, availables)
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

    def __getQuery(self, data, isFrom: bool) -> str:
        query: str = ""
        query += "from=" + (data['from'] if isFrom else data['to']) + '&'
        query += "to=" + (data['to'] if isFrom else data['from']) + '&'
        query += "date=" + self.__jToG(data['fromd'] if isFrom else data['tod']) + '&'
        query += "adultCount=" + data['adult'] + '&'
        query += "childCount=" + data['child'] + '&'
        query += "infantCount=" + data['infant'] + '&'
        query += "exclusive=" + ("false" if data['wagon'] == "0" else "true") + '&'
        query += "availableStatus=" + "Both"
        return query

    def __jToG(self, date: str, spliter='/') -> str:
        splitDate: list[str] = date.split(spliter)
        return str(jdatetime.date(day=int(splitDate[2]), month=int(splitDate[1]), year=int(splitDate[0])).togregorian())
