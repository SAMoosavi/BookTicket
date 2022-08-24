import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from CompleteForms import CompleteForms
from globalVariable import cities, months, Sex


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
        self.completeInputForm(username, "phonenumber")
        self.clickBtn("login-btn-step1")
        self.completeInputForm(password, "//input[@type='password']", By.XPATH)
        self.clickBtn("//form/div[4]/button[2]", By.XPATH)
        try:
            self.__close_login_form()
        except:
            pass

    def __go_to_login_form(self):
        self.clickBtn("//header/nav/ul/li[3]/div", By.XPATH)

    def __close_login_form(self):
        self.clickBtn("/html/body/div[2]/div/div/div[2]/div/span/span", By.XPATH, 1)

    def get_tickets(self, beginning: int, ending: int, date: str, adultNum: int | str, childNum: int | str,
                    sex: Sex) -> list[WebElement]:
        self.__complete_form_search(beginning, ending, date, adultNum, childNum, sex)
        self.__btn_search()
        self.__minTrain()
        return self.__tickets()

    # search
    def __complete_form_search(
            self,
            beginning: int, ending: int,
            date: str,
            adultNum: int | str, childNum: int | str,
            sex: Sex
    ):
        self.__beginning(beginning)
        self.__ending(ending)
        self.__date(date)
        self.__person_number(adultNum, childNum)
        self.__sex(sex)

    def __sex(self, data: Sex):
        if data == Sex.WOMAN:
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[3]",
                By.XPATH)
        elif data == Sex.MAN:
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[2]",
                By.XPATH)
        elif data == Sex.BOTH:
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[4]/label[1]",
                By.XPATH)

    def __person_number(self, adult: str | int, child: str | int):
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[1]/div/label", By.XPATH)
        for i in range(1, int(adult)):
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/button[2]",
                By.XPATH)
        for i in range(0, int(child)):
            self.clickBtn(
                "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[3]/div/div[2]/div[1]/div[2]/div/button[2]",
                By.XPATH)

    def __date(self, data: str):
        self.__open_date()
        self.__set_date(data)
        self.__save_date()

    def __save_date(self):
        self.clickBtn(
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
        self.clickBtn("/html/body/div[1]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/div/div[1]/div[1]",
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
        self.clickBtn(btnPath, elTypeBtn)

    def __btn_search(self):
        self.clickBtn(
            "/html/body/div/div/div/div[2]/div[2]/div[2]/form/div[2]/div[4]/button", By.XPATH)

    def __minTrain(self):
        self.clickBtn("/html/body/div/div/div/div[2]/div[3]/aside/div/div[4]/div[1]/div/div[2]/div[1]/div/label[2]",
                      By.XPATH)
        time.sleep(1)

    def __tickets(self) -> list[WebElement]:
        return self.wait_and_returns("/html/body/div/div/div/div[2]/div[3]/div/section[1]/div/*", By.XPATH, 1)
