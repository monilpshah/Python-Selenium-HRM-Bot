from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service


class Driver:
    driver = None
    driver = webdriver.Firefox(executable_path=".\..\WebDrivers\geckodriver")

    def __init__(self):
        self.driver = self.initialize_driver()
        pass

    @staticmethod
    def initialize_driver():
        if Driver.driver is None:
            Driver.driver = webdriver.Firefox(executable_path=".\..\WebDrivers\geckodriver")
        return Driver.driver
