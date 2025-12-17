from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    USERNAME = (By.XPATH, "//input[@autocomplete='{USERNAME}']")
    PASSWORD = (By.XPATH, "//input[@autocomplete='{PASSWORD}']")
    CHECKBOX = (By.XPATH, "//input[@type='{CHECKBOX}']")
    SUBMIT   = (By.XPATH, "//button[@type='{SUBMIT}']")


class FilterPageLocators(object):
    FILTER       = (By.XPATH, "//button[contains(normalize-space(.), '{FILTER}')]")
    LOCATION     = (By.XPATH, "//option[contains(normalize-space(.), '{LOCATION}')]")
    DAY_TEMP     = (By.XPATH, "//span[contains(normalize-space(.), '{DAY_GER_ABB}')]/preceding-sibling::input") # Placeholder for the german abbrivated day
    ANWENDEN     = (By.XPATH, "//button[contains(normalize-space(.), '{APPLY_FILTER}')]")
    FILTERNUMBER = (By.XPATH, "//button[contains(normalize-space(.), '{FILTER}')]/following-sibling::div")


class CourseLocators(object):
    COURSE_DAY     = (By.XPATH, "//a[contains(normalize-space(.), '{COURSE_NAME}')]")
    CANCELLED      = (By.XPATH, "//div[contains(normalize-space(.), '{CANCELLED}')]")
    BOOKABLE       = (By.XPATH, "//span[contains(normalize-space(.), '{BOOKABLE}')]/following-sibling::kgr-select-control")
    BOOK_PERSON    = (By.XPATH, "//kgr-form-field[@label='{BOOK_PERSON}']/descendant::option[contains(normalize-space(.), '{PERSON_NAME}')]")
    INVOICE_PERSON = (By.XPATH, "//kgr-form-field[@label='{INVOICE_PERSON}']/descendant::option[contains(normalize-space(.), '{PERSON_NAME}')]")
    AGREEGTC       = (By.XPATH, "//kgr-form-field[@label='{AGREEGTC}']/descendant::input[@type='checkbox']")
    BOOK           = (By.XPATH, "//button[contains(normalize-space(.), '{BOOK}')]")
