from selenium.webdriver.common.by import By

from CompleteForms import CompleteForms
from globalVariable import cities, months


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
