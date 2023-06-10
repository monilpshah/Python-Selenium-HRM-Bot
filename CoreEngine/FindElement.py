from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from Global.Driver import Driver


class FindElement:
    def __init__(self, driver):
        self.driver = driver

    def sendKeys(self, value):
        self.driver.find_element(By.NAME, "username").send_keys(value)
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
