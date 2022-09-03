import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from globalClass.CompleteForms import CompleteForms
from globalClass.globalVariable import cities, months, Sex
from v2.Passenger import Passenger
from v2.Person import Person
from v2.PlayAlarm import PlayAlarm
from helper.DateFunctions import int_to_month_of_number
from helper.SexFunctions import int_to_sex_enum


class GetTicket(CompleteForms):
    __URL: str = "https://mrbilit.com/train-ticket"

    __cities: dict = cities
    __month: dict = months

    __hasTo: bool = False

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    # login
    def login(self, username: str, password: str):
        self.__go_to_login_form()
        self.complete_input_form(username, "phonenumber")
        self.click_btn("login-btn-step1")
        self.complete_input_form(password, "//input[@type='password']", By.XPATH)
        self.click_btn("//form/div[4]/button[2]", By.XPATH)
        try:
            self.__close_login_form()
        except:
            pass

    def __go_to_login_form(self):
        self.click_btn("//header/nav/ul/li[3]/div", By.XPATH)

    def __close_login_form(self):
        self.click_btn("/html/body/div[2]/div/div/div[2]/div/span/span", By.XPATH, 1)

    def get_tickets(self, beginning: int, ending: int, date: str, adultNum: int | str, childNum: int | str,
                    sex: int) -> list[WebElement]:
        self.__complete_form_search(beginning, ending, date, adultNum, childNum, sex)
        self.__btn_search()
        self.__min_train()
        return self.__tickets()

    # search
    def __complete_form_search(
            self,
            beginning: int, ending: int,
            date: str,
            adultNum: int | str, childNum: int | str,
            sex: int
    ):
        self.__beginning(beginning)
        self.__ending(ending)
        self.__date(date)
        self.__person_number(adultNum, childNum)
        self.__sex(sex)

    def __sex(self, data: int):
        sex = int_to_sex_enum(data)
        if sex == Sex.WOMAN:
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[3]",
                By.XPATH)
        elif sex == Sex.MAN:
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[2]",
                By.XPATH)
        elif sex == Sex.BOTH:
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[1]",
                By.XPATH)

    def __person_number(self, adult: str | int, child: str | int):
        self.click_btn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[1]/div/label", By.XPATH)
        for i in range(1, int(adult)):
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/button[2]",
                By.XPATH)
        for i in range(0, int(child)):
            self.click_btn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/button[2]",
                By.XPATH)

    def __date(self, data: str):
        self.__open_date()
        self.__set_date(data)
        self.__save_date()

    def __save_date(self):
        self.click_btn(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[3]/div[2]/button[2]",
            By.XPATH)

    def __set_date(self, data: str):
        date = data.split('/')
        day = int(date[2])
        index = "1" \
            if self.__month[date[1]] in self.wait_and_return(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]",
            By.XPATH).text \
            else "2"
        btnsPath = "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[" \
                   + index + \
                   "]/div[3]/div[not(contains(@class, 'empty'))]"
        self.click_btn_on_list(btnsPath, day - 1, By.XPATH)

    def __open_date(self):
        self.click_btn("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[1]/div[1]",
                       By.XPATH)

    def __ending(self, cityNumber: int):
        inputPath = "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[1]/div/label/input"
        btnPath = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div"
        self.__set_city(cityNumber, inputPath, btnPath)

    def __beginning(self, cityNumber: int):
        inputPath = "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div/div[1]/div/label/input"
        btnPath = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div"
        self.__set_city(cityNumber, inputPath, btnPath)

    def __set_city(
            self, cityNumber: int,
            inputPath: str, btnPath: str,
            elTypeInput: By = By.XPATH, elTypeBtn: By = By.XPATH,
            timeSleep: int = 1
    ):
        city = self.__cities[cityNumber]
        self.complete_input_scroll(city, inputPath, elTypeInput)
        time.sleep(timeSleep)
        self.click_btn(btnPath, elTypeBtn)

    def __btn_search(self):
        self.click_btn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[4]/button", By.XPATH)

    # ticket
    def __min_train(self):
        self.click_btn("/html/body/div/div/div/div[2]/div[3]/aside/div/div[4]/div[1]/div/div[2]/div[1]/div/label[2]",
                       By.XPATH)
        time.sleep(1)

    def __tickets(self) -> list[WebElement]:
        return self.wait_and_returns(
            "/html/body/div/div/div/div[2]/div[3]/div/section[1]/div/*[contains(@class, 'trip-card-wrapper')]",
            By.XPATH, 1)

    def sel_ticket(self, ticket: WebElement, passengers: list[dict]):
        self.__book_ticket(ticket)
        self.__btn_verify()
        self.__set_passengers(passengers)
        self.__credentials()
        self.__check_price()
        self.__click_buy()

    def __book_ticket(self, ticket: WebElement):
        btn = ticket.find_element(By.XPATH, "//div/section[2]/div[2]/button")
        ticket.location_once_scrolled_into_view
        time.sleep(1)
        btn.click()

    def __btn_verify(self):
        self.click_btn_scroll("//div[contains(@class, 'btn-container')]/button[2]", By.XPATH)

    def __set_passengers(self, passengers: list[dict]):
        Pas = Passenger()
        for index in (1, len(passengers)):
            person = Pas.get_person_by_ID(passengers[index - 1]['ID'])
            self.__set_passenger(index, person, passengers[index - 1]['service'])

    def __set_passenger(self, index: int, passenger: Person, service: str):
        baseLocation = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[" + str(index) + "]"
        self.wait_and_return(baseLocation, By.XPATH).location_once_scrolled_into_view
        time.sleep(0.5)
        self.__set_first_name(baseLocation, passenger.get_first_name())
        self.__set_last_name(baseLocation, passenger.get_last_name())
        self.__set_sex(baseLocation, passenger.get_sex())
        self.__set_ID(baseLocation, passenger.get_ID())
        self.__set_day(baseLocation, passenger.get_day())
        self.__set_month(baseLocation, passenger.get_month())
        self.__set_year(baseLocation, passenger.get_year())
        self.__set_service(baseLocation, service)

    def __set_service(self, baseLocation, service: str):
        try:
            if service is None or service == "":
                self.click_btn(baseLocation + "/div/form/span/div/div[1]/div[2]/label", By.XPATH, 0.1)
            else:
                self.complete_input_form(service, baseLocation + "/div/form/span/div/div[1]/div[2]/label/input", By.XPATH,
                                         0.1)
            time.sleep(1)
            self.click_btn(baseLocation + "/div/form/span/div/div[2]/div/div/div[2]/div[1]", By.XPATH)
        except:
            pass

    def __set_first_name(self, baseLocation, data: str):
        self.complete_input_form(data, baseLocation + "/div/form/div[2]/div[2]/label/input", By.XPATH)

    def __set_last_name(self, baseLocation, data: str):
        self.complete_input_form(data, baseLocation + "/div/form/div[3]/div[2]/label/input", By.XPATH)

    def __set_sex(self, baseLocation, data: Sex):
        location = baseLocation + "/div/form/div[1]/span[1]/div/div[1]/div"
        if data == Sex.MAN:
            self.click_btn(location + "/label[1]", By.XPATH)
        elif data == Sex.WOMAN:
            self.click_btn(location + "/label[2]", By.XPATH)

    def __set_ID(self, baseLocation, data: str):
        self.complete_input_form(data, baseLocation + "/div/form/div[4]/div[2]/label/input", By.XPATH)

    def __set_day(self, baseLocation, data: int):
        self.complete_input_form(str(data),
                                 baseLocation + "/div/form/div[5]/div/div[3]/div[1]/div/div[2]/label/input",
                                 By.XPATH)
        time.sleep(1)
        self.click_btn(baseLocation + "/div/form/div[5]/div/div[3]/div[1]/div[2]/div/div/div[2]/div", By.XPATH)

    def __set_month(self, baseLocation, data: int):
        month = self.__month[int_to_month_of_number(data)]
        self.complete_input_form(month,
                                 baseLocation + "/div/form/div[5]/div/div[3]/div[2]/div[1]/div[2]/label/input",
                                 By.XPATH)
        time.sleep(1)
        self.click_btn(baseLocation + "/div/form/div[5]/div/div[3]/div[2]/div[2]/div/div/div[2]/div", By.XPATH)

    def __set_year(self, baseLocation, data: int):
        self.complete_input_form(str(data),
                                 baseLocation + "/div/form/div[5]/div/div[3]/div[3]/div[1]/div[2]/label/input",
                                 By.XPATH)
        time.sleep(1)
        self.click_btn(baseLocation + "/div/form/div[5]/div/div[3]/div[3]/div[2]/div/div/div[2]/div", By.XPATH)

    def __credentials(self):
        self.click_btn_scroll("form-next-button")

    def __check_price(self):
        self.click_btn_scroll("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/label", By.XPATH)
        price = self.wait_and_return(
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[1]/div[4]/div[2]/span",
            By.XPATH).text
        if int(price) != 0:
            PlayAlarm()

    def __click_buy(self):
        self.click_btn("btnAccept")
        time.sleep(30)
