import time
from BookTicket import BookTicket
from CompleteForms import CompleteForms
from selenium.webdriver.common.by import By
from globalVariable import cities, months


class AliBabaBookTicket(BookTicket, CompleteForms):
    __URL: str = "https://www.alibaba.ir/"

    __cities: dict = cities
    __months: dict = months

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # Login
    def login(self, data):
        self.__goToLoginForm()
        self.completeInputForm(data['username'], "/html/body/div/div[2]/div/div/form/div[1]/span/input",
                               By.XPATH)
        self.completeInputForm(data['password'], "/html/body/div/div[2]/div/div/form/div[2]/span/input",
                               By.XPATH)
        self.clickBtn("/html/body/div/div[2]/div/div/form/div[3]/button", By.XPATH)

    def __goToLoginForm(self):
        self.clickBtn("//header/div[1]/div/div/div/button", By.XPATH)
        self.clickBtn("/html/body/div/div[2]/div/div/form/div[2]/button[2]", By.XPATH)

    # Search
    def search(self, data):
        self.__goToSearchPage()
        self.__completeFormSearch(data)
        find: bool = False
        while not find:
            self.__btnSearch()
            try:
                self.__getTrains()
                if data['groupWay'] == 1:
                    self.__getTrains()
                find = True
            except:
                self.clickBtn("/html/body/div/div[1]/header/div[2]/div/div/div/div/div/button",
                              By.XPATH)

    def __getTrains(self):
        self.__minTrain()
        self.clickBtn("//section/div[2]/div[1]/div[2]/button",
                      By.XPATH)

    def __minTrain(self):
        t = self.wait_and_return("//section/div[1]/ul/li[3]/a",
                                 By.XPATH)
        time.sleep(2)
        t.click()
        self.completeCheckBox(
            "//aside/div/div/div[5]/div/details/div/div/label", By.XPATH)

    def __btnSearch(self):
        self.clickBtn(
            "//form/div[2]/div[4]/button", By.XPATH)

    def __goToSearchPage(self):
        time.sleep(2)
        self.clickBtn('//a[@href="/train-ticket"]', By.XPATH)

    def __completeFormSearch(self, data):
        self.__groupWay(data['groupWay'])
        self.__wagon(data['wagon'])
        self.__sex(data['sex'])
        self.__from(data['from'])
        self.__to(data['to'])
        self.__date(data['fromd'])
        if data['groupWay'] == 1:
            self.__date(data['tod'])
        self.__setDate()
        self.__traveler(data['adult'], data['child'], data['infant'])

    def __traveler(self, adult, child, infant):
        self.clickBtn(
            "//form/div[2]/div[3]/div/div[1]", By.XPATH)
        for i in range(1, int(adult)):
            self.clickBtn(
                "//form/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/button[1]",
                By.XPATH)
        for i in range(0, int(child)):
            self.clickBtn(
                "//form/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/button[1]",
                By.XPATH)
        for i in range(0, int(infant)):
            self.clickBtn(
                "//form/div[2]/div[3]/div/div[2]/div/div[3]/div[2]/button[1]",
                By.XPATH)

    def __setDate(self):
        self.clickBtn(
            "//form/div[2]/div[2]/div/div[2]/div/div[3]/button",
            By.XPATH)

    def __date(self, data):
        date = data.split('/')
        day: str = date[2] if not date[2][0] == "0" else date[2][1]
        index = "1" if self.__months[date[1]] in self.wait_and_return(
            "/html/body/div/div[1]/main/div/div[2]/div[1]/div[2]/div/form/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/h5",
            By.XPATH).text else "2"
        self.wait_and_returns(
            "//form/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[" + index + "]/div/span[contains(@class, 'calendar-cell')]",
            By.XPATH)[int(day) - 1].click()

    def __to(self, data):
        city = self.__getCity(data)
        self.completeInputForm(city,
                               "//form/div[2]/div[1]/div/div[1]/div[2]/span/input",
                               By.XPATH)
        self.clickBtn(
            "//form/div[2]/div[1]/div/div[2]/div/ul/li[1]/a",
            By.XPATH)

    def __from(self, data):
        city = self.__getCity(data)
        self.completeInputForm(city,
                               "//form/div[2]/div[1]/div/div[1]/div[1]/span[1]/input",
                               By.XPATH)
        self.clickBtn(
            "//form/div[2]/div[1]/div/div[2]/div/ul/li[1]/a",
            By.XPATH)

    def __getCity(self, date) -> str:
        return self.__cities[date]

    def __sex(self, data):
        self.clickBtn(
            "//form/div[1]/span[3]/button", By.XPATH)
        if data == "1":
            self.clickBtn(
                "//form/div[1]/span[3]/div/div/ul/li[3]/a",
                By.XPATH)
        elif data == "2":
            self.clickBtn(
                "//form/div[1]/span[3]/div/div/ul/li[2]/a",
                By.XPATH)
        elif data == "3":
            self.clickBtn(
                "//form/div[1]/span[3]/div/div/ul/li[1]/a",
                By.XPATH)

    def __wagon(self, data):
        self.clickBtn(
            "//form/div[1]/span[2]/button", By.XPATH)
        if data == "0":
            self.clickBtn(
                "//form/div[1]/span[2]/div/div/ul/li[2]/a",
                By.XPATH)
        elif data == "1":
            self.clickBtn(
                "//form/div[1]/span[2]/div/div/ul/li[1]/a",
                By.XPATH)

    def __groupWay(self, data):
        self.clickBtn(
            "//form/div[1]/span[1]/button", By.XPATH)
        if data == 0:
            self.clickBtn(
                "//form/div[1]/span[1]/div/div/ul/li[1]/a",
                By.XPATH)
        elif data == 1:
            self.clickBtn(
                "//form/div[1]/span[1]/div/div/ul/li[2]/a",
                By.XPATH)

    # set users
    def setUsers(self, dataUsers):
        for i in range(1, len(dataUsers) + 1):
            self.__setUser(i, dataUsers[i - 1])
        self.__setUsersBtn()

    def __setUsersBtn(self):
        self.clickBtn('//main/div/div/div/div/div[3]/button', By.XPATH)

    def __setUser(self, i, data):
        self.__setFName(i, data['FName'])
        self.__setLName(i, data['LName'])
        self.__setSex(i, data['sex'])
        self.__setId(i, data['id'])
        self.__setBirthday(i, data['birthday'])

    def __setBirthday(self, i, data):
        self.__setDay(i, data['day'])
        self.__setMonth(i, data['month'])
        self.__setYear(i, data['year'])

    def __setYear(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[3]",
                      By.XPATH)
        self.clickBtn(
            "//form/div[2]/div/div[1]/div[2]/div/div[5]/div/div[3]/div[2]/div/ul/li[@data-value=\"13" + data + "\"]/a",
            By.XPATH)

    def __setMonth(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[2]",
                      By.XPATH)
        if data[0] == 0:
            data = data[1:]
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[2]/div[2]/div/ul/li["
                      + data +
                      "]/a", By.XPATH)

    def __setDay(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[1]",
                      By.XPATH)
        if data[0] == 0:
            data = data[1:]
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[1]/div[2]/div/ul/li["
                      + data +
                      "]/a",
                      By.XPATH)

    def __setId(self, i, data):
        self.completeInputForm(data,
                               "//form/div[2]/div/div["
                               + str(i) +
                               "]/div[2]/div/div[4]/div/span/input",
                               By.XPATH)

    def __setSex(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[3]/div",
                      By.XPATH)
        if data == "1":
            self.clickBtn(
                "//form/div[2]/div/div["
                + str(i) +
                "]/div[2]/div/div[3]/div/div[2]/div/ul/li[2]/a",
                By.XPATH)
        elif data == "2":
            self.clickBtn(
                "//form/div[2]/div/div["
                + str(i) +
                "]/div[2]/div/div[3]/div/div[2]/div/ul/li[1]/a",
                By.XPATH)

    def __setLName(self, i, data):
        self.completeInputForm(data,
                               "//main/form/div[2]/div/div["
                               + str(i) +
                               "]/div[2]/div/div[2]/div/span/input",
                               By.XPATH)

    def __setFName(self, i, data):
        self.completeInputForm(data,
                               "//main/form/div[2]/div/div["
                               + str(i) +
                               "]/div[2]/div/div[1]/div/span/input",
                               By.XPATH)

    # buy
    def buy(self):
        self.clickBtn("/html/body/div/div[1]/main/div/div[5]/div/div[1]/div[1]/div[1]/label", By.XPATH)
        self.clickBtn("/html/body/div/div[1]/main/div/div[5]/div/div[2]/button[2]", By.XPATH)
        time.sleep(60)
