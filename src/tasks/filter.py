
import time
from src.utils.selenium.selenium_actions import (ClickAction,
                                                 #EnterTextAction,
                                                 ClickWhenClickable,
                                                 #EnterTextWhenVisible
                                                 )
from logger import get_logger


class Filter:
    def __init__(self, driver, course_overview_url, filter_locators_filled, click_action=ClickWhenClickable, logger=None):
        self.driver = driver
        self.course_overview_url = course_overview_url
        self.filter_locators_filled = filter_locators_filled
        self.click_action = click_action(driver=self.driver)
        self.logger = logger or get_logger("etvcourse.filter")

        self.ctx = {}

    def run_filter(self):
        self.logger.debug("Starting filter flow for url: %s", self.course_overview_url)
        self.go_to_course_overview_page(course_overview_url=self.course_overview_url)
        self.click_filter(filter_locator=self.filter_locators_filled["FILTER"],
                          click_action=self.click_action)
        time.sleep(2)
        self.click_location(location_locator=self.filter_locators_filled["LOCATION"],
                            click_action=self.click_action)
        time.sleep(2)
        self.click_weekday(weekday_locator=self.filter_locators_filled["WEEKDAY"],
                           click_action=self.click_action)
        time.sleep(2)
        self.click_apply_button(apply_button_locator=self.filter_locators_filled["APPLY_FILTER"],
                                click_action=self.click_action)
        time.sleep(10) 
        self.get_applied_filter_number(applied_filter_locator=self.filter_locators_filled["FILTERNUMBER"])
        self.logger.debug("Completed filter flow for url: %s", self.course_overview_url)

    # step 1
    def go_to_course_overview_page(self, course_overview_url) -> None:
        self.logger.debug("Navigating to course page: %s", course_overview_url)
        self.driver.get(course_overview_url) 
        self.logger.debug("Navigation complete to course page")

    # step 2
    def click_filter(self, filter_locator: tuple, click_action: ClickAction) -> None:
        self.logger.debug("Clicking filter %s", filter_locator)
        click_action.execute(locator=filter_locator)
        self.logger.debug("Clicked filter")

    # step 3
    def click_location(self, location_locator: tuple, click_action: ClickAction) -> None:
        self.logger.debug("Clicking location %s", location_locator)
        click_action.execute(locator=location_locator)
        self.logger.debug("Clicked location")

    # step 4
    def click_weekday(self, weekday_locator: tuple, click_action: ClickAction) -> None:
        self.logger.debug("Clicking weekday %s", weekday_locator)
        click_action.execute(locator=weekday_locator)
        self.logger.debug("Clicked weekday")

    # step 5
    def click_apply_button(self, apply_button_locator: tuple, click_action: ClickAction) -> None:
        self.logger.debug("Clicking apply button %s", apply_button_locator)
        click_action.execute(locator=apply_button_locator)
        self.logger.debug("Clicked apply button")

    def get_applied_filter_number(self, applied_filter_locator: tuple) -> None:
        self.logger.debug("Getting applied filter number from %s", applied_filter_locator)
        element = self.driver.find_element(*applied_filter_locator)
        filter_number = element.text
        self.logger.debug("Got applied filter number: %s", filter_number)
        self.ctx["applied_filter_number"] = int(filter_number)