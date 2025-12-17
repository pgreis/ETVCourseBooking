from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SeleniumFunctionalities:

    def __init__(self, driver=None):
        self.driver = driver
     
    def _wait_until_located(self, locator, seconds_to_wait: float = 3) -> None:
        WebDriverWait(driver=self.driver,
                      timeout=seconds_to_wait).until(EC.presence_of_element_located(locator = locator))
        
    def _wait_until_visible(self, locator, seconds_to_wait: float = 3) -> None:
            WebDriverWait(driver=self.driver,
                          timeout=seconds_to_wait).until(EC.visibility_of_element_located(locator = locator))
            
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
    