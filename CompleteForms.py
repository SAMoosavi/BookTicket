from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from GetElement import GetElement


class CompleteForms(GetElement):

    def __init__(self, URL):
        GetElement.__init__(self, URL)

    def completeSelectForm(self, value, element, el_type=By.ID, timeWait: int = 60):
        selectFrom = Select(self.wait_and_return(element, el_type, timeWait))
        selectFrom.select_by_value(value)

    def completeInputForm(self, value, element, el_type=By.ID, timeWait: int = 60):
        inputForm = self.wait_and_return(element, el_type, timeWait)
        inputForm.clear()
        inputForm.send_keys(value)

    def complete_input_scroll(self, value, element, el_type=By.ID, timeWait: int = 60):
        inputForm = self.wait_and_return(element, el_type, timeWait)
        inputForm.location_once_scrolled_into_view
        inputForm.clear()
        inputForm.send_keys(value)

    def completeInputFormReadOnly(self, value, element, el_type=By.ID, timeWait: int = 60):
        inputForm = self.wait_and_return(element, el_type, timeWait)
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

    def completeRadio(self, value, element, el_type=By.ID, timeWait: int = 60):
        radioForm = self.wait_and_returns(element, el_type, timeWait)
        radioForm[value].click()

    def completeCheckBox(self, element, el_type=By.ID, timeWait: int = 60):
        checkBoxForm = self.wait_and_return(element, el_type, timeWait)
        checkBoxForm.click()

    def clickBtn(self, element, el_type=By.ID, timeWait: int = 60):
        pageLink = self.wait_and_return(element, el_type, timeWait)
        pageLink.click()
