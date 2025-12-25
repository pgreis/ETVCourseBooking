# import functools
# import re
# import time
# from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
# from selenium.webdriver.common.by import By

# def retry_with_handlers(exception_handlers: dict, max_retries: int = 3, delay: float = 0.5):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             for attempt in range(1, max_retries + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     handlers = []
#                     for exc_type, exc_handlers in exception_handlers.items():
#                         if isinstance(e, exc_type):
#                             handlers.extend(exc_handlers)

#                     for handler in handlers:
#                         handler(*args, exception=e, **kwargs)

#                     if attempt < max_retries:
#                         time.sleep(delay)
#                     else:
#                         raise e
#         return wrapper
#     return decorator


# def _create_css_selector_by_regex(msg:str,
#                                   extract_regex: str=r'(?<=another element ).*(?= obscures)',
#                                   split_html_class_regex:str=r'<(\w+)\s+class=\"([^\"]+)\"') -> str|None:
    
#     if not msg:
#         return None
#     raw = re.search(extract_regex, msg)
#     if not raw:
#         return None
#     fragment = raw.group(0).strip()
#     match = re.search(split_html_class_regex, fragment)
#     if not match:
#         return None
#     tag, classes = match.groups()
#     css_selector = tag + "." + ".".join(classes.split())
#     return css_selector

# def _intercepted_exception_handling(driver, msg: str) -> None:
#     """
#     Module-level handler that uses the provided `driver` to find the blocking
#     element (parsed from the exception message) and attempts to dismiss it.
#     """
#     css_selector = _create_css_selector_by_regex(msg)
#     if not css_selector:
#         raise RuntimeError("Could not parse blocking element from message")

#     try:
#         closing_button = driver.find_element(By.CSS_SELECTOR, f"{css_selector} button")
#     except NoSuchElementException:
#         blocking_el = driver.find_element(By.CSS_SELECTOR, css_selector)
#         driver.execute_script("arguments[0].click();", blocking_el)
#         return

#     driver.execute_script("arguments[0].click();", closing_button)



# handlers = {
#     ElementClickInterceptedException: [handle_click_intercepted],
#     NoSuchElementException: [handle_no_such_element, handle_click_intercepted]  # multiple handlers
# }

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
    """Minimal decorator that extracts the WebDriver from `self.driver`.

    Designed for decorating bound instance methods (the common case in this
    project). On exception it finds handlers for the exception type and calls
    `handler.handle(self.driver, exception)`.
    """
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

                    # Expect a bound method where args[0] is `self` with `.driver`.
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