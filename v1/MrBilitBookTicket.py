import json
import time
import requests
import jdatetime
from BookTicket import BookTicket
from globalClass.CompleteForms import CompleteForms
from selenium.webdriver.common.by import By
from globalClass.globalVariable import cities, months
from globalClass.LogTrain import LogTrain


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
        if data['groupWay'] == 1:
            self.__hasTo = True
        self.__completeFormSearch(data)
        self.__btnSearch()
        self.__setTrain()
        self.__btnVerify()

    def searchS(self, data, listId):
        if data['groupWay'] == 1:
            self.__hasTo = True
        self.__firstSearch(data, listId)
        self.__completeFormSearch(data)
        self.__btnSearch()
        self.__setTrain()
        self.__btnVerify()

    def __btnVerify(self):
        r = self.wait_and_return("/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[8]/button[2]", By.XPATH)
        r.location_once_scrolled_into_view
        time.sleep(0.5)
        r.click()

    def __setTrain(self):
        self.__minTrain()
        self.__clickTicket(self.__fromTime)
        if self.__hasTo:
            self.__minTrain()
            self.__clickTicket(self.__toTime)

    def __clickTicket(self, dataTime: str):
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
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[3]/div/section[1]/div/div["
            + str(num) +
            "]/div/section[2]/div[2]/button",
            By.XPATH)

    def __minTrain(self):
        self.clickBtn("/html/body/div/div/div/div[2]/div[3]/aside/div/div[4]/div[1]/div/div[2]/div[1]/div/label[2]",
                      By.XPATH)
        time.sleep(1)

    def __btnSearch(self):
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[4]/button", By.XPATH)

    def __completeFormSearch(self, data):
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

    def __openDate(self):
        self.clickBtn("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[1]/div[1]", By.XPATH)

    def __to(self, data):
        city = self.__getCity(data)
        self.completeInputForm(city,
                               "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[1]/div/label/input",
                               By.XPATH)
        time.sleep(1)
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
        time.sleep(1)
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
        while not findFrom:
            query: str = self.__getQuery(data, True)
            response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
            findFrom = self.__getTrain(response, listId[0], True)
        if self.__hasTo:
            findFrom: bool = False
            while not findFrom:
                query: str = self.__getQuery(data, False)
                response = requests.get("https://train.atighgasht.com/TrainService/api/GetAvailable/v2?" + query).text
                findFrom = self.__getTrain(response, listId[1], False)

    def __getTrain(self, data, listId, isFrom: bool) -> bool:
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

    # setUsers
    def setUsers(self, dataUsers):
        hasService: bool = True
        for i in range(1, len(dataUsers) + 1):
            hasService = self.__setUser(i, dataUsers[i - 1], hasService)
        self.__setUsersBtn()

    def __setUsersBtn(self):
        r = self.wait_and_return('form-next-button')
        r.location_once_scrolled_into_view
        time.sleep(0.5)
        r.click()

    def __setUser(self, i, data, hasService):
        baseLocation = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[" + str(i) + "]"
        self.wait_and_return(baseLocation, By.XPATH).location_once_scrolled_into_view
        time.sleep(0.5)
        self.__setFName(baseLocation, data['FName'])
        self.__setLName(baseLocation, data['LName'])
        self.__setSex(baseLocation, data['sex'])
        self.__setId(baseLocation, data['id'])
        self.__setBirthday(baseLocation, data['birthday'])
        try:
            if hasService:
                self.__setService(baseLocation, data['service'])
                return True
        except:
            return False

    def __setService(self, baseLocation, data):
        if data is None or data == "":
            r = self.wait_and_return(baseLocation + "/div/form/span/div/div[1]/div[2]/label", By.XPATH)
            r.click()
        else:
            self.completeInputForm(data, baseLocation + "/div/form/span/div/div[1]/div[2]/label/input", By.XPATH)
        time.sleep(1)
        self.clickBtn(baseLocation + "/div/form/span/div/div[2]/div/div/div[2]/div[1]", By.XPATH)

    def __setBirthday(self, baseLocation, data):
        self.__setDay(baseLocation, data['day'])
        self.__setMonth(baseLocation, data['month'])
        self.__setYear(baseLocation, data['year'])

    def __setYear(self, baseLocation, data):
        data = "13" + data
        self.completeInputForm(data,
                               baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[3]/div[1]/div[2]/label/input",
                               By.XPATH)
        time.sleep(1)
        self.clickBtn(baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[3]/div[2]/div/div/div[2]/div", By.XPATH)

    def __setMonth(self, baseLocation, data):
        if data[0] == "0":
            data = data[1:]
        self.clickBtn(baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[2]/div/div[2]/label", By.XPATH)
        self.clickBtn(
            baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[2]/div[2]/div/div/div[2]/div["
            + data +
            "]",
            By.XPATH)

    def __setDay(self, baseLocation, data):
        if data[0] == "0":
            data = data[1:]
        self.completeInputForm(data,
                               baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[1]/div[1]/div[2]/label/input",
                               By.XPATH)
        time.sleep(1)
        self.clickBtn(baseLocation + "/div/form/div[5]/div/div[2]/div[3]/div[1]/div[2]/div/div/div[2]/div", By.XPATH)

    def __setId(self, baseLocation, data):
        self.completeInputForm(data, baseLocation + "/div/form/div[4]/div[2]/label/input", By.XPATH)

    def __setLName(self, baseLocation, data):
        self.completeInputForm(data, baseLocation + "/div/form/div[3]/div[2]/label/input", By.XPATH)

    def __setFName(self, baseLocation, data):
        self.completeInputForm(data, baseLocation + "/div/form/div[2]/div[2]/label/input", By.XPATH)

    def __setSex(self, baseLocation, data):
        location = (baseLocation + "/div/form/div[1]/span[1]/div/div[1]/div")
        if data == "2" or data == 2:
            self.clickBtn(location + "/label[1]", By.XPATH)
        elif data == "1" or data == 1:
            self.clickBtn(location + "/label[2]", By.XPATH)

    # buy
    def buy(self):
        self.__credentials()
        self.__clickBuy()

    def __credentials(self):
        r = self.wait_and_return("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/label", By.XPATH)
        r.location_once_scrolled_into_view
        time.sleep(0.5)
        r.click()

    def __clickBuy(self):
        self.clickBtn("btnAccept")
        time.sleep(30)
