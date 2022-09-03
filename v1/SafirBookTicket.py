import time

from selenium.webdriver.common.by import By

from globalClass.CompleteForms import CompleteForms
from v1.BookTicket import BookTicket


class SafirBookTicket(BookTicket, CompleteForms):
    __URL = "https://www.safirrail.ir/fa/"

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # login
    def login(self, data):
        self.complete_input_form(data['username'], 'user', By.NAME)
        self.complete_input_form(data['password'], 'pass', By.NAME)
        self.click_btn('//input[@type="submit"]', By.XPATH)

    # search
    def search(self, data):
        self.__go_to_search_page()
        self.__complete_form_search(data)
        self.__get_ticket(data)

    def __go_to_search_page(self):
        self.click_btn('//a[@href="../etrain/"]', By.XPATH)

    def __complete_form_search(self, data):
        self.complete_select_form(data['from'], 'from')
        self.complete_select_form(data['to'], 'to')
        self.complete_radio(data['groupWay'], 'groupWay', By.NAME)
        self.complete_input_form_read_only(data['fromd'], 'fromd')
        self.complete_input_form_read_only(data['tod'], 'tod')
        self.complete_select_form(data['sex'], 'sex')
        self.complete_input_form(data['adult'], 'adult')
        self.complete_input_form(data['child'], 'child')
        self.complete_input_form(data['infant'], 'infant')
        if data['wagon'] == "1":
            self.complete_check_box('wagon')

    def __get_trains(self, Id):
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

    def __str_price_to_int(self, strPrice):
        strPrice = strPrice.split(',')
        intPrice = 0
        for price in strPrice:
            intPrice *= 1000
            intPrice += int(price)
        return intPrice

    def __min_train_fromd(self, trains):
        minPrice = 0
        minTrain = None
        for train in trains:
            price = self.__str_price_to_int(train[9].text)
            if minPrice > price or minPrice == 0:
                minPrice = price
                minTrain = train
        return minTrain

    def __min_train_tod(self, trains):
        minPrice = 0
        minTrain = None
        for train in trains:
            price = self.__str_price_to_int(train[10].text)
            if minPrice > price or minPrice == 0:
                minPrice = price
                minTrain = train
        return minTrain

    def __get_ticket(self, data):
        while True:
            self.click_btn('srchB')

            ticketExisting = 0

            trainsFromd = self.__get_trains('Tbl')
            if len(trainsFromd) > 0:
                trainFromd = self.__min_train_fromd(trainsFromd)
                trainFromd[0].click()
                ticketExisting += 1

            if data['groupWay'] == 1:
                trainsTod = self.__get_trains('retTbl')
                if len(trainsTod) > 0:
                    trainTod = self.__min_train_tod(trainsTod)
                    trainTod[0].click()
                    ticketExisting += 1

            if data['groupWay'] == 1:
                if ticketExisting == 2:
                    break
            else:
                if ticketExisting == 1:
                    break
        self.click_btn('srchC')

    # set users
    def set_users(self, dataUsers):
        for i in range(0, len(dataUsers)):
            self.__set_user(dataUsers[i], i)
        self.complete_check_box('wgnVerify')

    def __set_user(self, user, i):
        self.complete_input_form(user['id'], 'pid' + str(i))
        self.complete_input_form(user['FName'], 'fn' + str(i))
        self.complete_input_form(user['LName'], 'ln' + str(i))
        self.complete_input_form(user['birthday']['day'], 'ruz' + str(i))
        self.complete_input_form(user['birthday']['month'], 'mah' + str(i))
        self.complete_input_form(user['birthday']['year'], 'sal' + str(i))

    # buy
    def buy(self):
        self.click_btn('FlatButton', By.CLASS_NAME)
        time.sleep(60)
