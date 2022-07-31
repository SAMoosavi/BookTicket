from BookTicket import BookTicket
from CompleteForms import CompleteForms
from selenium.webdriver.common.by import By
from globalVariable import cities


class MrBilitBookTicket(BookTicket, CompleteForms):
    __URL: str = "https://mrbilit.com/"

    __cities: dict = cities

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # Login
    def login(self, data):
        self.__goToLoginForm()
        self.completeInputForm(data['username'], "phonenumber")
        self.clickBtn("login-btn-step1")
        self.completeInputForm(data['password'], "//input[@type=\"password\"]", By.XPATH)
        self.clickBtn("//button[text()='ورود']", By.XPATH)

    def __goToLoginForm(self):
        self.clickBtn("///header/nav/ul/li[3]/div", By.XPATH)
