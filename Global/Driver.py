from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from configparser import ConfigParser
import os
import sys


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


class Driver:
    driver = None

    # driver = webdriver.Firefox(executable_path=".\..\WebDrivers\geckodriver")

    def __init__(self):
        self.driver = self.initialize_driver()
        pass


    @staticmethod
    def initialize_driver():
        if Driver.driver is None:
            config = ConfigParser()
            config.read("example.ini")
            FIREFOX_DRIVER_PATH = config.get("firefoxdriver", "path")
            Driver.driver = webdriver.Firefox(executable_path=resource_path(FIREFOX_DRIVER_PATH))
        return Driver.driver
