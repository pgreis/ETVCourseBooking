import time
from src.utils.selenium.selenium_actions import (ClickAction,
                                                 EnterTextAction,
                                                 ClickWhenClickable,
                                                 EnterTextWhenVisible)
from logger import get_logger


class Login:
    def __init__(self, driver, login_url, login_name, password, locators_filled,
                 click_action=ClickWhenClickable, enter_text_action=EnterTextWhenVisible,
                 logger=None):
        self.driver = driver
        self.login_url = login_url
        self.login_name = login_name
        self.password = password
        self.locators_filled = locators_filled
        self.click_action = click_action(driver=self.driver)
        self.enter_text_action = enter_text_action(driver=self.driver)
        self.logger = logger or get_logger("etvcourse.login")

    def run_login(self):
        self.logger.debug("Starting login flow for user: %s", self.login_name)

        self.go_to_login_page(login_url=self.login_url)

        self.enter_username(username_locator=self.locators_filled["USERNAME"],
                            username=self.login_name,
                            enter_text_action=self.enter_text_action)

        self.enter_password(password_locator=self.locators_filled["PASSWORD"],
                            password=self.password,
                            enter_text_action=self.enter_text_action)

        self.click_checkbox(checkbox_locator=self.locators_filled["CHECKBOX"],
                            click_action=self.click_action)
        self.click_login_button(login_button_locator=self.locators_filled["SUBMIT"],
                                click_action=self.click_action)
        self.logger.debug("Completed login flow for user: %s", self.login_name)
        time.sleep(5)

    # step 1
    def go_to_login_page(self, login_url) -> None:
        self.logger.debug("Navigating to login url: %s", login_url)
        self.driver.get(login_url)
        self.logger.debug("Navigation complete to login url")

    # step 2
    def enter_username(self, username_locator: tuple, username:str, enter_text_action: EnterTextAction) -> None:
        self.logger.debug("Entering username into %s", username_locator)
        enter_text_action.execute(locator=username_locator,
                                  text=username)
        self.logger.debug("Entered username")
        
    #step 3
    def enter_password(self, password_locator: tuple, password: str, enter_text_action: EnterTextAction) -> None:
        self.logger.debug("Entering password into %s", password_locator)
        enter_text_action.execute(locator=password_locator,
                                  text=password)
        self.logger.debug("Entered password")

    # step 4
    def click_checkbox(self, checkbox_locator: tuple, click_action: ClickAction) -> None:
        self.logger.debug("Clicking checkbox %s", checkbox_locator)
        click_action.execute(locator=checkbox_locator)
        self.logger.debug("Clicked checkbox")

    # step 5
    def click_login_button(self, login_button_locator: tuple, click_action: ClickAction) -> None:
        self.logger.debug("Clicking login button %s", login_button_locator)
        click_action.execute(locator=login_button_locator)
        self.logger.debug("Clicked login button")