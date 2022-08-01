from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from GetElement import GetElement


class CompleteForms(GetElement):

    def __init__(self, URL):
        GetElement.__init__(self, URL)

    def completeSelectForm(self, value, element, el_type=By.ID):
        selectFrom = Select(self.wait_and_return(element, el_type))
        selectFrom.select_by_value(value)

    def completeInputForm(self, value, element, el_type=By.ID):
        inputForm = self.wait_and_return(element, el_type)
        inputForm.clear()
        inputForm.send_keys(value)

    def completeInputFormReadOnly(self, value, element, el_type=By.ID):
        inputForm = self.wait_and_return(element, el_type)
        selector: str = ""
        isMulty: bool = False
        if el_type == By.ID:
            selector = "getElementById"
        elif el_type == By.TAG_NAME:
            selector = "getElementsByTagName"
        elif el_type == By.CSS_SELECTOR:
            isMulty = True
            selector = "querySelectorAll"
        elif el_type == By.CLASS_NAME:
            selector = "getElementsByClassName"
        elif el_type == By.XPATH:
            assert Exception("eee")

        query: str = ""

        if isMulty:
            query = "document." + selector + "('" + element + "')[0]"
        else:
            query = "document." + selector + "('" + element + "')"

        self.driver.execute_script(query + ".removeAttribute('readonly')")
        inputForm.clear()
        inputForm.send_keys(value)

    def completeRadio(self, value, element, el_type=By.ID):
        radioForm = self.wait_and_returns(element, el_type)
        radioForm[value].click()

    def completeCheckBox(self, element, el_type=By.ID):
        checkBoxForm = self.wait_and_return(element, el_type)
        checkBoxForm.click()

    def clickBtn(self, element, el_type=By.ID):
        pageLink = self.wait_and_return(element, el_type)
        pageLink.click()
