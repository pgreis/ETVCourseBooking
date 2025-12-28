from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class DriverInitialization:

    def __init__(self, settings:dict, arguments:list=list(), full_screen:bool=True):
        self.settings = settings
        self.arguments = arguments
        self.options = Options()
        if self.settings:
            self.add_settings()
        if self.arguments:
            self.add_firefox_arguments()

    def add_settings(self):
        for pref, value in self.settings.items():
            self.options.set_preference(pref, value)

    def add_firefox_arguments(self):
        for argument in self.arguments:
            self.options.add_argument(argument)

    def create_firefox_driver(self, is_remote:bool=False, remote_url:str=None, is_headless:bool=True):
        if is_headless:
            self.options.add_argument("--headless")

        if is_remote:
            return webdriver.Remote(command_executor=remote_url, options=self.options).maximize_window()

        return webdriver.Firefox(options=self.options).maximize_window()