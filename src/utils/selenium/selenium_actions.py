from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.utils.selenium.error_exception_handler import ClickInterceptedHandler, SleepThreeSeconds, retry_with_handlers
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

handlers = {
    ElementClickInterceptedException: [ClickInterceptedHandler()],
    NoSuchElementException: [SleepThreeSeconds(), ClickInterceptedHandler()]
}



class ClickAction(ABC):

    def __init__(self, driver=None):
        self.driver = driver

        if driver is None:
            raise ValueError("Driver must be provided")

    @abstractmethod
    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        pass

class EnterTextAction(ABC):

    def __init__(self, driver=None):
        self.driver = driver

        if driver is None:
                raise ValueError("Driver must be provided")

    @abstractmethod
    def execute(self, locator: tuple, text: str, seconds_to_wait: float = 3) -> None:
        pass

class GetAttributeAction(ABC):

    def __init__(self, driver=None):
        self.driver = driver

        if driver is None:
                raise ValueError("Driver must be provided")

    @abstractmethod
    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> str:
        pass


# click
class ClickWhenVisible(ClickAction):

    @retry_with_handlers(exception_handlers=handlers, max_retries=3, delay=0.5)
    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        element = WebDriverWait(driver=self.driver,
                                timeout=seconds_to_wait).until(EC.visibility_of_element_located(locator = locator))
        element.click()

class ClickWhenClickable(ClickAction):

    @retry_with_handlers(exception_handlers=handlers, max_retries=3, delay=0.5)
    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> None:
        element = WebDriverWait(driver=self.driver,
                                timeout=seconds_to_wait).until(EC.element_to_be_clickable(mark = locator))
        element.click()

# enter text
class EnterTextWhenVisible(EnterTextAction):

    @retry_with_handlers(exception_handlers=handlers, max_retries=3, delay=0.5)
    def execute(self, locator: tuple, text: str, seconds_to_wait: float = 3) -> None:
        element = WebDriverWait(driver=self.driver,
                                timeout=seconds_to_wait).until(EC.visibility_of_element_located(locator = locator))
        element.clear()
        element.send_keys(text)

# get
class GetHrefWhenVisible(GetAttributeAction):

    @retry_with_handlers(exception_handlers=handlers, max_retries=3, delay=0.5)
    def execute(self, locator: tuple, seconds_to_wait: float = 3) -> str:
        element = WebDriverWait(driver=self.driver,
                                timeout=seconds_to_wait).until(EC.visibility_of_element_located(locator = locator))
        href_link = element.get_attribute("href")
        return href_link
    
