from abc import ABC, abstractmethod
import functools
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import re
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

class BaseHandler(ABC):
    @abstractmethod
    def handle(self, driver: WebDriver, exception: WebDriverException) -> None:
        pass

def retry_with_handlers(exception_handlers: dict, max_retries: int = 3, delay: float = 0.5):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    handlers = []
                    for exc_type, exc_handlers in exception_handlers.items():
                        if isinstance(e, exc_type):
                            handlers.extend(exc_handlers)

                    if not args or not hasattr(args[0], "driver"):
                        raise RuntimeError(
                            "retry_with_handlers expects a bound method; ensure the decorated function is an instance method with a `.driver` attribute on self"
                        )

                    driver_arg = getattr(args[0], "driver")

                    for handler in handlers:
                        handler.handle(driver_arg, e)

                    if attempt < max_retries:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator


class ClickInterceptedHandler(BaseHandler):
    def handle(self, driver: WebDriver, exception: WebDriverException):
        # Safe because we only register this handler for the specific exception type
        if not isinstance(exception, ElementClickInterceptedException):
            raise TypeError("ClickInterceptedHandler used with wrong exception type")

        msg = str(exception)

        css_selector = self._extract_css_selector(msg)
        if not css_selector:
            raise RuntimeError("Could not parse blocking element from message")

        try:
            button = driver.find_element(By.CSS_SELECTOR, f"{css_selector} button")
        except NoSuchElementException:
            el = driver.find_element(By.CSS_SELECTOR, css_selector)
            driver.execute_script("arguments[0].click();", el)
        else:
            driver.execute_script("arguments[0].click();", button)

    @staticmethod
    def _extract_css_selector(msg: str) -> str | None:
        if not msg:
            return None
        raw = re.search(r"(?<=another element ).*(?= obscures)", msg)
        if not raw:
            return None
        fragment = raw.group(0).strip()
        match = re.search(r"<(\w+)\s+class=\"([^\"]+)\"", fragment)
        if not match:
            return None
        tag, classes = match.groups()
        return tag + "." + ".".join(classes.split())

class SleepThreeSeconds(BaseHandler):
    def handle(self, driver: WebDriver, exception: WebDriverException):
        if not isinstance(exception, NoSuchElementException):
            raise TypeError("NoSuchElementHandler used with wrong exception type")
        time.sleep(3)