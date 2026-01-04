
import sys
import time
from logger import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

import os
from dotenv import load_dotenv

from db_handler import DatabaseHandler
from src.utils.help_functions import read_yaml_file
from src.utils.locators.locator_help_fns import fill_and_resolve_locators
from src.utils.locators.locator_templates import (LoginPageLocators,
                                                  FilterPageLocators,
                                                  BookingLocators)

from src.tasks.preparation import (get_tomorrow_weekday_abbr,
                                   get_active_courses_by_weekday)
from src.tasks.driver_initialization import DriverInitialization
from src.tasks.login import Login
from src.tasks.filter import Filter
from src.tasks.booking import Booking

load_dotenv()

def main():

    tasks_cfg = {"is_headless" : True,
                 "is_remote" : True,
                 "n_filter_tries" : 2,
                 "n_correct_filter" : 3,
                 "selenium_remote_url" : "http://selenium:4444/wd/hub",
                 "db_url": os.getenv("DB_URL"),
                 "table_name": os.getenv("TABLE_NAME"),
                 "login_name" : os.getenv("ETV_LOGIN_NAME"),
                 "login_url": os.getenv("LOGIN_URL"),
                 "login_name": os.getenv("ETV_LOGIN_NAME"),
                 "password": os.getenv("ETV_LOGIN_PW"),
                 "course_overview_url": os.getenv("COURSE_OVERVIEW_URL")}
    
    locator_fillings = read_yaml_file(os.path.join("src", "utils", "locators","locator_fillings.yaml"))
    firefox_cfg = read_yaml_file(os.path.join("config", "browser_settings.yaml"))["firefox"]

    db = DatabaseHandler(db_url=tasks_cfg["db_url"])
    db.load_table(table_name=tasks_cfg["table_name"])

    weekday_abbr=get_tomorrow_weekday_abbr()
    active_courses = get_active_courses_by_weekday(course_table=db.loaded_table,
                                                   weekday_ger_abb=weekday_abbr)

    if not active_courses:
        logger.info("No active courses for %s", weekday_abbr)
        sys.exit()


    time.sleep(15) # wait to give selenium standalone container more time to wake up  
    driver_cl = DriverInitialization(settings=firefox_cfg["settings"]["preferences"],
                                     arguments=firefox_cfg["settings"]["arguments"])
    driver = driver_cl.create_firefox_driver(is_headless=tasks_cfg["is_headless"],
                                             remote_url=tasks_cfg["selenium_remote_url"],
                                             is_remote=tasks_cfg["is_remote"])

    ## login
    login_locators_filled = fill_and_resolve_locators(template_class=LoginPageLocators,
                                                      base_placeholders=locator_fillings['LoginPageLocators'],
                                                      extra_fields={"PERSON_NAME": tasks_cfg["login_name"]},)

    login_pipe = Login(driver=driver,
                       login_url=tasks_cfg["login_url"],
                       login_name=tasks_cfg["login_name"],
                       password=tasks_cfg["password"],
                       locators_filled=login_locators_filled,
                       logger=logger)
    login_pipe.run_login()

    for single_course in active_courses:
        logger.info(f"Starting booking flow for course: {single_course["orig_course_name"]} for person: {single_course["person"]}")

        # filter
        filter_locators_filled = fill_and_resolve_locators(template_class=FilterPageLocators,
                                                           base_placeholders=locator_fillings['FilterPageLocators'],
                                                           extra_fields={"DAY_GER_ABB": single_course.get("weekday_ger_abb")},)

        for _ in range(tasks_cfg["n_filter_tries"]):

            try:
                filter_pipe = Filter(driver=driver,
                                    course_overview_url=tasks_cfg["course_overview_url"],
                                    filter_locators_filled=filter_locators_filled,
                                    logger=logger)
                filter_pipe.run_filter()

                if filter_pipe.ctx["applied_filter_number"] != tasks_cfg["n_correct_filter"]:
                        logger.warning("Incorrect number of filters applied: %s", filter_pipe.ctx["applied_filter_number"])
                        continue
                else:
                    logger.debug("Correct numbers of filter applied")
                    

                # booking
                booking_locators_filled = fill_and_resolve_locators(template_class=BookingLocators,
                                                                    base_placeholders=locator_fillings['BookingLocators'],
                                                                    extra_fields={"COURSE_NAME": single_course.get("orig_course_name"),
                                                                                  "PERSON_NAME": single_course.get("person")},)

                booking_pipe = Booking(driver=driver,
                                       booking_locators_filled=booking_locators_filled,
                                       logger=logger)
                booking_pipe.run_booking()
                logger.info(f"Booking of {single_course["orig_course_name"]} for person: {single_course["person"]} successful")
                break


            except Exception as err:
                logger.error("Error in filter/ booking process: ", err)

    logger.info("Closing process...")
    sys.exit()

if __name__ == "__main__":
    main()