import time

from BookTicket import BookTicket
from CompleteForms import CompleteForms
from selenium.webdriver.common.by import By


class SafirBookTicket(BookTicket, CompleteForms):
    __URL = "https://www.safirrail.ir/fa/"

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # login
    def login(self, data):
        self.completeInputForm(data['username'], 'user', By.NAME)
        self.completeInputForm(data['password'], 'pass', By.NAME)
        self.clickBtn('//input[@type="submit"]', By.XPATH)

    # search
    def search(self, data):
        self.__goToSearchPage()
        self.__completeFormSearch(data)
        self.__getTicket(data)

    def __goToSearchPage(self):
        self.clickBtn('//a[@href="../etrain/"]', By.XPATH)

    def __completeFormSearch(self, data):
        self.completeSelectForm(data['from'], 'from')
        self.completeSelectForm(data['to'], 'to')
        self.completeRadio(data['groupWay'], 'groupWay', By.NAME)
        self.completeInputFormReadOnly(data['fromd'], 'fromd')
        self.completeInputFormReadOnly(data['tod'], 'tod')
        self.completeSelectForm(data['sex'], 'sex')
        self.completeInputForm(data['adult'], 'adult')
        self.completeInputForm(data['child'], 'child')
        self.completeInputForm(data['infant'], 'infant')
        if data['wagon'] == "1":
            self.completeCheckBox('wagon')

    def __getTrains(self, Id):
        trains = list()
        table = self.wait_and_return(Id)
        tr = table.find_elements(By.TAG_NAME, 'tr')
        for i in range(1, len(tr)):
            cols = tr[i].find_elements(By.TAG_NAME, "td")
            if id == 'Tbl':
                if cols[8].text != "0":
                    trains.append(cols)
            else:
                if cols[9].text != "0":
                    trains.append(cols)
        return trains

    def __strPriceToInt(self, strPrice):
        strPrice = strPrice.split(',')
        intPrice = 0
        for price in strPrice:
            intPrice *= 1000
            intPrice += int(price)
        return intPrice

    def __minTrainFromd(self, trains):
        minPrice = 0
        minTrain = None
        for train in trains:
            price = self.__strPriceToInt(train[9].text)
            if minPrice > price or minPrice == 0:
                minPrice = price
                minTrain = train
        return minTrain

    def __minTrainTod(self, trains):
        minPrice = 0
        minTrain = None
        for train in trains:
            price = self.__strPriceToInt(train[10].text)
            if minPrice > price or minPrice == 0:
                minPrice = price
                minTrain = train
        return minTrain

    def __getTicket(self, data):
        while True:
            self.clickBtn('srchB')

            ticketExisting = 0

            trainsFromd = self.__getTrains('Tbl')
            if len(trainsFromd) > 0:
                trainFromd = self.__minTrainFromd(trainsFromd)
                trainFromd[0].click()
                ticketExisting += 1

            if data['groupWay'] == 1:
                trainsTod = self.__getTrains('retTbl')
                if len(trainsTod) > 0:
                    trainTod = self.__minTrainTod(trainsTod)
                    trainTod[0].click()
                    ticketExisting += 1

            if data['groupWay'] == 1:
                if ticketExisting == 2:
                    break
            else:
                if ticketExisting == 1:
                    break
        self.clickBtn('srchC')

    # set users
    def setUsers(self, dataUsers):
        for i in range(0, len(dataUsers)):
            self.__setUser(dataUsers[i], i)
        self.completeCheckBox('wgnVerify')

    def __setUser(self, user, i):
        self.completeInputForm(user['id'], 'pid' + str(i))
        self.completeInputForm(user['FName'], 'fn' + str(i))
        self.completeInputForm(user['LName'], 'ln' + str(i))
        self.completeInputForm(user['birthday']['day'], 'ruz' + str(i))
        self.completeInputForm(user['birthday']['month'], 'mah' + str(i))
        self.completeInputForm(user['birthday']['year'], 'sal' + str(i))

    # buy
    def buy(self):
        self.clickBtn('FlatButton', By.CLASS_NAME)
        time.sleep(60)
