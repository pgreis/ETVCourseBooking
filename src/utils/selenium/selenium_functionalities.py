from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC




class ClickFunctionalities(ABC):
     
    def __init__(self, driver=None):
        self.driver = driver

    @abstractmethod
    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        pass

class ClickWhenLocated(ClickFunctionalities):

    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        WebDriverWait(driver=self.driver,
                      timeout=seconds_to_wait).until(EC.presence_of_element_located(locator = locator))
        self.driver.find_element(*locator).click()

class ClickWhenVisible(ClickFunctionalities):

    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        WebDriverWait(driver=self.driver,
                      timeout=seconds_to_wait).until(EC.visibility_of_element_located(locator = locator))
        self.driver.find_element(*locator).click()

class ClickWhenClickable(ClickFunctionalities):

    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        WebDriverWait(driver=self.driver,
                      timeout=seconds_to_wait).until(EC.element_to_be_clickable(locator = locator))
        self.driver.find_element(*locator).click()
    




class SeleniumFunctionalities:

    def __init__(self, driver=None):
        self.driver = driver
     
    def _wait_until_located(self, locator, seconds_to_wait: float = 3) -> None:
        WebDriverWait(driver=self.driver,
                      timeout=seconds_to_wait).until(EC.presence_of_element_located(locator = locator))
        
    def _wait_until_visible(self, locator, seconds_to_wait: float = 3) -> None:
            WebDriverWait(driver=self.driver,
                          timeout=seconds_to_wait).until(EC.visibility_of_element_located(locator = locator))

    def _wait_until_clickable(self, locator, seconds_to_wait: float = 3) -> None:
            WebDriverWait(driver=self.driver,
                          timeout=seconds_to_wait).until(EC.element_to_be_clickable(locator = locator))
            
            
    def enter_text_when_visible(self,locator: tuple,text: str,seconds_to_wait: float = 3) -> None:
        self._wait_until_visible(locator=locator,
                                 seconds_to_wait=seconds_to_wait)
        self.driver.find_element(*locator).send_keys(text)

    def click_when_visible(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        self._wait_until_visible(locator=locator,
                                 seconds_to_wait=seconds_to_wait)
        self.driver.find_element(*locator).click()

    def is_element_selected(self, xpath: str) -> bool: 
        return self.driver.find_element(By.XPATH, xpath).is_selected()    
    
    








# msg = 'Element <button class="kgr-postfix__fixed kgr-text kgr-text--uppercase kgr-text--bold kgr-clickable kgr-clickable--touchy" type="button"> is not clickable at point (1858,159) because another element <div class="kgr-modal is-open"> obscures it; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#elementclickinterceptedexception'

# _click_intercepted_exeption_handling(msg)