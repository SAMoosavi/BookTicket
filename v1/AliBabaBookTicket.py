import time
from selenium.webdriver.common.by import By

from globalClass.CompleteForms import CompleteForms
from globalClass.globalVariable import cities, months
from v1.BookTicket import BookTicket


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
        self.__go_to_login_form()
        self.complete_input_form(data['username'], "/html/body/div/div[2]/div/div/form/div[1]/span/input",
                                 By.XPATH)
        self.complete_input_form(data['password'], "/html/body/div/div[2]/div/div/form/div[2]/span/input",
                                 By.XPATH)
        self.click_btn("/html/body/div/div[2]/div/div/form/div[3]/button", By.XPATH)

    def __go_to_login_form(self):
        self.click_btn("//header/div[1]/div/div/div/button", By.XPATH)
        self.click_btn("/html/body/div/div[2]/div/div/form/div[2]/button[2]", By.XPATH)

    # Search
    def search(self, data):
        self.__go_to_search_page()
        self.__complete_form_search(data)
        find: bool = False
        while not find:
            self.__btn_search()
            try:
                self.__get_trains()
                if data['groupWay'] == 1:
                    self.__get_trains()
                find = True
            except:
                self.click_btn("/html/body/div/div[1]/header/div[2]/div/div/div/div/div/button",
                               By.XPATH)

    def __get_trains(self):
        self.__min_train()
        self.click_btn("//section/div[2]/div[1]/div[2]/button",
                       By.XPATH)

    def __min_train(self):
        t = self.wait_and_return("//section/div[1]/ul/li[3]/a",
                                 By.XPATH)
        time.sleep(2)
        t.click()
        self.complete_check_box(
            "//aside/div/div/div[5]/div/details/div/div/label", By.XPATH)

    def __btn_search(self):
        self.click_btn(
            "//form/div[2]/div[4]/button", By.XPATH)

    def __go_to_search_page(self):
        time.sleep(2)
        self.click_btn('//a[@href="/train-ticket"]', By.XPATH)

    def __complete_form_search(self, data):
        self.__group_way(data['groupWay'])
        self.__wagon(data['wagon'])
        self.__sex(data['sex'])
        self.__from(data['from'])
        self.__to(data['to'])
        self.__date(data['fromd'])
        if data['groupWay'] == 1:
            self.__date(data['tod'])
        self.__set_date()
        self.__traveler(data['adult'], data['child'], data['infant'])

    def __traveler(self, adult, child, infant):
        self.click_btn(
            "//form/div[2]/div[3]/div/div[1]", By.XPATH)
        for i in range(1, int(adult)):
            self.click_btn(
                "//form/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/button[1]",
                By.XPATH)
        for i in range(0, int(child)):
            self.click_btn(
                "//form/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/button[1]",
                By.XPATH)
        for i in range(0, int(infant)):
            self.click_btn(
                "//form/div[2]/div[3]/div/div[2]/div/div[3]/div[2]/button[1]",
                By.XPATH)

    def __set_date(self):
        self.click_btn(
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
        city = self.__get_city(data)
        self.complete_input_form(city,
                               "//form/div[2]/div[1]/div/div[1]/div[2]/span/input",
                                 By.XPATH)
        self.click_btn(
            "//form/div[2]/div[1]/div/div[2]/div/ul/li[1]/a",
            By.XPATH)

    def __from(self, data):
        city = self.__get_city(data)
        self.complete_input_form(city,
                               "//form/div[2]/div[1]/div/div[1]/div[1]/span[1]/input",
                                 By.XPATH)
        self.click_btn(
            "//form/div[2]/div[1]/div/div[2]/div/ul/li[1]/a",
            By.XPATH)

    def __get_city(self, date) -> str:
        return self.__cities[date]

    def __sex(self, data):
        self.click_btn(
            "//form/div[1]/span[3]/button", By.XPATH)
        if data == "1":
            self.click_btn(
                "//form/div[1]/span[3]/div/div/ul/li[3]/a",
                By.XPATH)
        elif data == "2":
            self.click_btn(
                "//form/div[1]/span[3]/div/div/ul/li[2]/a",
                By.XPATH)
        elif data == "3":
            self.click_btn(
                "//form/div[1]/span[3]/div/div/ul/li[1]/a",
                By.XPATH)

    def __wagon(self, data):
        self.click_btn(
            "//form/div[1]/span[2]/button", By.XPATH)
        if data == "0":
            self.click_btn(
                "//form/div[1]/span[2]/div/div/ul/li[2]/a",
                By.XPATH)
        elif data == "1":
            self.click_btn(
                "//form/div[1]/span[2]/div/div/ul/li[1]/a",
                By.XPATH)

    def __group_way(self, data):
        self.click_btn(
            "//form/div[1]/span[1]/button", By.XPATH)
        if data == 0:
            self.click_btn(
                "//form/div[1]/span[1]/div/div/ul/li[1]/a",
                By.XPATH)
        elif data == 1:
            self.click_btn(
                "//form/div[1]/span[1]/div/div/ul/li[2]/a",
                By.XPATH)

    # set users
    def set_users(self, dataUsers):
        for i in range(1, len(dataUsers) + 1):
            self.__set_user(i, dataUsers[i - 1])
        self.__set_users_btn()

    def __set_users_btn(self):
        self.click_btn('//main/div/div/div/div/div[3]/button', By.XPATH)

    def __set_user(self, i, data):
        self.__set_first_name(i, data['FName'])
        self.__set_last_name(i, data['LName'])
        self.__set_sex(i, data['sex'])
        self.__set_ID(i, data['id'])
        self.__set_birthday(i, data['birthday'])

    def __set_birthday(self, i, data):
        self.__set_day(i, data['day'])
        self.__set_month(i, data['month'])
        self.__set_year(i, data['year'])

    def __set_year(self, i, data):
        self.click_btn("//form/div[2]/div/div["
                       + str(i) +
                      "]/div[2]/div/div[5]/div/div[3]",
                       By.XPATH)
        self.click_btn(
            "//form/div[2]/div/div[1]/div[2]/div/div[5]/div/div[3]/div[2]/div/ul/li[@storage-value=\"13" + data + "\"]/a",
            By.XPATH)

    def __set_month(self, i, data):
        self.click_btn("//form/div[2]/div/div["
                       + str(i) +
                      "]/div[2]/div/div[5]/div/div[2]",
                       By.XPATH)
        if data[0] == 0:
            data = data[1:]
        self.click_btn("//form/div[2]/div/div["
                       + str(i) +
                      "]/div[2]/div/div[5]/div/div[2]/div[2]/div/ul/li["
                       + data +
                      "]/a", By.XPATH)

    def __set_day(self, i, data):
        self.click_btn("//form/div[2]/div/div["
                       + str(i) +
                      "]/div[2]/div/div[5]/div/div[1]",
                       By.XPATH)
        if data[0] == 0:
            data = data[1:]
        self.click_btn("//form/div[2]/div/div["
                       + str(i) +
                      "]/div[2]/div/div[5]/div/div[1]/div[2]/div/ul/li["
                       + data +
                      "]/a",
                       By.XPATH)

    def __set_ID(self, i, data):
        self.complete_input_form(data,
                               "//form/div[2]/div/div["
                                 + str(i) +
                               "]/div[2]/div/div[4]/div/span/input",
                                 By.XPATH)

    def __set_sex(self, i, data):
        self.click_btn("//form/div[2]/div/div["
                       + str(i) +
                      "]/div[2]/div/div[3]/div",
                       By.XPATH)
        if data == "1":
            self.click_btn(
                "//form/div[2]/div/div["
                + str(i) +
                "]/div[2]/div/div[3]/div/div[2]/div/ul/li[2]/a",
                By.XPATH)
        elif data == "2":
            self.click_btn(
                "//form/div[2]/div/div["
                + str(i) +
                "]/div[2]/div/div[3]/div/div[2]/div/ul/li[1]/a",
                By.XPATH)

    def __set_last_name(self, i, data):
        self.complete_input_form(data,
                               "//main/form/div[2]/div/div["
                                 + str(i) +
                               "]/div[2]/div/div[2]/div/span/input",
                                 By.XPATH)

    def __set_first_name(self, i, data):
        self.complete_input_form(data,
                               "//main/form/div[2]/div/div["
                                 + str(i) +
                               "]/div[2]/div/div[1]/div/span/input",
                                 By.XPATH)

    # buy
    def buy(self):
        self.click_btn("/html/body/div/div[1]/main/div/div[5]/div/div[1]/div[1]/div[1]/label", By.XPATH)
        self.click_btn("/html/body/div/div[1]/main/div/div[5]/div/div[2]/button[2]", By.XPATH)
        time.sleep(60)
