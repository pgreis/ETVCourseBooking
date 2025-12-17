
from src.utils.selenium_functionalities import SeleniumFunctionalities
from src.utils.locator_templates import LoginPageLocators

class Login(SeleniumFunctionalities):
    
    def __init__(self, driver, login_url, login_name, password, locators_filled):
        
        self.driver = driver
        self.login_url = login_url
        self.login_name = login_name
        self.password = password
        self.locators_filled = locators_filled

    def run_login(self):
        self.go_to_login_page(login_url=self.login_url)
        self.enter_username(username_locator=self.locators_filled["USERNAME"],
                            username=self.login_name)
        self.enter_password(password_locator=self.locators_filled["PASSWORD"],
                            password=self.password)
        self.click_checkbox()
        self.click_login_button()

    # step 1
    def go_to_login_page(self, login_url) -> None:
        self.driver.get(login_url)

    # step 2
    def enter_username(self, username_locator: tuple, username:str) -> None:
        self.enter_text_when_visible(locator=username_locator,
                                      text=username)
        
    #step 3
    def enter_password(self, password_locator: tuple, password: str) -> None:
        self.enter_text_when_visible(locator=password_locator,
                                     text=password)
        
    # step 4
    def click_checkbox(self) -> None:
        self.click_when_visible(locator=self.locators_filled["CHECKBOX"])

    # step 5
    def click_login_button(self) -> None:
        self.click_when_visible(locator=self.locators_filled["SUBMIT"])

