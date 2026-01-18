import time

from src.utils.selenium.selenium_actions import (#ClickAction,
                                                 #EnterTextAction,
                                                 ClickWhenClickable,
                                                 #EnterTextWhenVisible,
                                                 GetHrefWhenVisible)
from logger import get_logger

class Booking:
    def __init__(self, driver, booking_locators_filled, click_action=ClickWhenClickable, get_href_action=GetHrefWhenVisible, logger=None):
        self.driver = driver
        self.booking_locators_filled = booking_locators_filled
        self.click_action = click_action(driver=self.driver)
        self.get_href_action = get_href_action(driver=self.driver)
        self.logger = logger or get_logger("etvcourse.booking")

        self.ctx = {}

    def run_booking(self):
        self.logger.debug("Starting booking flow")
        self.get_course_link(course_day_locator=self.booking_locators_filled["COURSE_DAY"])
        self.go_to_course_page(course_link=self.ctx["step_1/course_link"])
        time.sleep(10)  # wait for page to load
        self.check_if_bookable(bookable_locator=self.booking_locators_filled["BOOKABLE"])
        if self.ctx["step_3/is_course_bookable"]:
            time.sleep(1)
            self.book_for_person(person_locator=self.booking_locators_filled["BOOK_PERSON"])
            time.sleep(1)
            self.select_invoice_person(invoice_person_locator=self.booking_locators_filled["INVOICE_PERSON"])
            time.sleep(1)
            self.checkmark_terms_and_conditions(terms_locator=self.booking_locators_filled["AGREEGTC"])
            time.sleep(1)        
            self.book(book_locator=self.booking_locators_filled["BOOK"])
            self.logger.info("Booking flow complete")
        else:
            self.logger.info("Course is not bookable, skipping booking step")

    # step 1
    def get_course_link(self, course_day_locator: tuple) -> None:
        self.logger.debug("Getting course link from %s", course_day_locator)
        self.ctx["step_1/course_link"] = self.get_href_action.execute(locator=course_day_locator)
        self.logger.debug("Got course link")

    # step 2
    def go_to_course_page(self, course_link: str) -> None:
        self.logger.debug("Navigating to course page: %s", course_link)
        self.driver.get(course_link) 
        self.logger.debug("Navigation complete to course page")

    # step 3
    def check_if_bookable(self, bookable_locator: tuple) -> None:
        self.logger.debug("Checking if course is bookable via %s", bookable_locator)
        bookable_element = self.driver.find_elements(*bookable_locator)
        self.ctx["step_3/is_course_bookable"] = bookable_element != []
        self.logger.debug("Course is bookable")

    # step 4
    def book_for_person(self, person_locator: tuple) -> None:
        self.logger.debug("Booking course for person via %s", person_locator)
        self.click_action.execute(locator=person_locator)
        self.logger.debug("Booked course for person")

    # step 5
    def select_invoice_person(self, invoice_person_locator: tuple) -> None:
        self.logger.debug("Selecting invoice person via %s", invoice_person_locator)
        self.click_action.execute(locator=invoice_person_locator)
        self.logger.debug("Selected invoice person")

    # step 6
    def checkmark_terms_and_conditions(self, terms_locator: tuple) -> None:
        self.logger.debug("Agreeing to terms via %s", terms_locator)
        self.click_action.execute(locator=terms_locator)
        self.logger.debug("Agreed to terms")

    # step 7
    def book(self, book_locator: tuple) -> None:
        self.logger.debug("Clicking book button %s", book_locator)
        self.click_action.execute(locator=book_locator)
        self.logger.debug("Clicked book button")
