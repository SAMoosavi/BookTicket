from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetElement:
    driver = None

    def __init__(self, URL):
        self.driver = webdriver.Firefox()
        self.driver.get(URL)

    def wait_and_return(self, element, el_type=By.ID):
        return WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((el_type, element))
        )

    def wait_and_returns(self, element, el_type=By.ID):
        return WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((el_type, element))
        )
