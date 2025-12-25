from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from functools import wraps
import time
import re

def _parse_blocking_element_from_msg(msg: str):
    if not msg:
        return None
    raw = re.search(r'(?<=another element ).*(?= obscures)', msg)
    if not raw:
        return None
    fragment = raw.group(0).strip()
    match = re.search(r'<(\w+)\s+class=\"([^\"]+)\"', fragment)
    if not match:
        return None
    tag, classes = match.groups()
    css_selector = tag + "." + ".".join(classes.split())
    return css_selector

def _intercepted_exception_handling(driver, msg: str) -> None:
    """
    Module-level handler that uses the provided `driver` to find the blocking
    element (parsed from the exception message) and attempts to dismiss it.
    """
    css_selector = _parse_blocking_element_from_msg(msg)
    if not css_selector:
        raise RuntimeError("Could not parse blocking element from message")

    try:
        closing_button = driver.find_element(By.CSS_SELECTOR, f"{css_selector} button")
    except NoSuchElementException:
        blocking_el = driver.find_element(By.CSS_SELECTOR, css_selector)
        driver.execute_script("arguments[0].click();", blocking_el)
        return

    driver.execute_script("arguments[0].click();", closing_button)

def retry_on_interception_decorator(retries: int = 1, wait: float = 0.2):
    """
    Decorator factory: retries the wrapped method when selenium raises
    ElementClickInterceptedException. On interception, runs the module-level
    handler passing `self.driver`, then retries the original call.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(self, *args, **kwargs)
                except ElementClickInterceptedException as e:
                    attempt += 1
                    # ensure there is a driver attribute to pass to handler
                    driver = getattr(self, "driver", None)
                    if driver is None:
                        # no driver available; re-raise original exception
                        raise
                    try:
                        _intercepted_exception_handling(driver, str(e))
                    except Exception:
                        # handler failed — re-raise original exception
                        raise
                    if attempt > retries:
                        raise
                    time.sleep(wait)
        return wrapper
    return decorator