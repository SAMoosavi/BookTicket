from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


class GetElement:
    driver = None

    def __init__(self, URL):
        self.driver = webdriver.Firefox()
        self.driver.get(URL)

    def __del__(self):
        self.driver.close()

    def wait_and_return(self, pathOfElement: str, el_type: By = By.ID, timeWAit: int = 60) -> WebElement:
        return WebDriverWait(self.driver, timeWAit).until(
            EC.presence_of_element_located((el_type, pathOfElement))
        )

    def wait_and_returns(self, pathOfElement: str, el_type: By = By.ID, timeWAit: int = 60) -> list[WebElement]:
        return WebDriverWait(self.driver, timeWAit).until(
            EC.presence_of_all_elements_located((el_type, pathOfElement))
        )
