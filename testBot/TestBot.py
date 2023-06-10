from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import traceback
import logging
from Global.Driver import Driver

# Google Sheet API
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


class TestBot:

    def __init__(self):
        self.driver = Driver.initialize_driver()
        pass

    def closeDriver(self):
        self.driver.close()

    def launch(self, url):
        try:
            self.driver.get(url)
            self.driver.set_page_load_timeout(30)
            self.driver.maximize_window()
            # self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("Unable to launch the browser driver", e)

    def fluentWait(self, xpath, elementName, timeout):
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                 ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            logging.info(elementName + " is visible in the screen")
        except Exception as e:
            raise Exception("Unable to wait for the " + elementName, e)

    def login(self, username, password):
        try:
            oUsername = "//*[@name='username']"
            oPassword = "//*[@name='password']"
            oLoginBtn = "//button[@type='submit']"
            self.fluentWait(oUsername, "Username", 10)
            self.driver.find_element(By.XPATH, oUsername).send_keys(username)
            self.fluentWait(oPassword, "Password", 10)
            self.driver.find_element(By.XPATH, oPassword).send_keys(password)
            self.fluentWait(oLoginBtn, "Login Button", 10)
            self.driver.find_element(By.XPATH, oLoginBtn).click()
        except Exception as e:
            raise Exception("Unable to login into the System ", e)

    def navigate(self, menuName):
        try:
            oNavigator = "//*[contains(@class,'navbar')]//span[text()='{menuName}']".format(menuName=menuName)
            oActiveMenu = "//*[contains(@class,'navbar')]//a[contains(@class,'active')]//span[text()='{menu}']".format(
                menu=menuName)
            oSearchbar = "//div[contains(@class,'main-menu')]//*[@placeholder='Search']"
            self.fluentWait(oSearchbar, "Searchbar", 10)
            self.driver.find_element(By.XPATH, oSearchbar).send_keys(menuName)
            self.fluentWait(oNavigator, menuName, 10)
            self.driver.find_element(By.XPATH, oNavigator).click()
            try:
                self.fluentWait(oActiveMenu, "selected " + menuName, 10)
                logging.info(menuName + " menu is selected successfully")
            except TimeoutException as e:
                logging.error(menuName + " menu can't be selected. Something went Wrong!!!")
        except Exception as e:
            raise Exception("Unable to navigate to " + menuName + " page", e)

    def readExcel(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'key.json'
        credentials = None
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '199TtxUfqbgwrPfzfzvsC3zxwsn_TUJjW3Ahlh2LOH7Y'
        SAMPLE_RANGE_NAME = 'Sheet1!A2:J1000'

        try:
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])
            # print(values)
            if not values:
                logging.warning('No data found.')

            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                # print('%s, %s' % (row[0], row[7]))
                pass
            return values
        except HttpError as err:
            raise Exception("Unable to read the excel", e)

    def updateFlag(self, rowNumber, addFlag, botComment):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'key.json'
        credentials = None
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        SAMPLE_SPREADSHEET_ID = '199TtxUfqbgwrPfzfzvsC3zxwsn_TUJjW3Ahlh2LOH7Y'
        SAMPLE_RANGE_NAME = 'Sheet1!A2:J1000'
        try:
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            data = result.get('values', [])
            # print(data)
            newData = []
            for row in data:
                if len(row) < 10:
                    row.append("")
                newData.append(row)
            newData[rowNumber][8] = addFlag
            newData[rowNumber][9] = botComment
            request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                             range=SAMPLE_RANGE_NAME,
                                                             valueInputOption="USER_ENTERED",
                                                             body={"values": newData}).execute()
            # logging.info(request)

        except HttpError as err:
            raise Exception("Unable to read the excel", e)

    def addCandidate(self, data):
        try:
            oAddBtn = "//div[contains(@class,'header')]/button/i[contains(@class,'plus')]"
            oFirstName = "//input[@name='firstName']"
            oMiddleName = "//input[@name='middleName']"
            oLastName = "//input[@name='lastName']"
            oVacancy = "//*[text()='Vacancy']//following::div[contains(@class,'select')][1]"
            oVacancyName = "//*[text()='Vacancy']//following::*[text()='{postName}']"
            oEmail = "//*[text()='Email']//following::input[1]"
            oContactNumber = "//*[text()='Contact Number']//following::input[1]"
            oResume = "//*[text()='Resume']//following::input[1]"
            oKeywords = "//*[text()='Keywords']//following::input[1]"
            oDateofApplication = "//*[text()='Date of Application']//following::input[1]"
            oNotes = "//*[text()='Notes']//following::textarea"
            oConsentCheckbox = "//*[text()='Consent to keep data']//following::*[contains(@class,'checkbox')]"
            oSave = "//button[@type='submit']"
            oSuccess = "//div[contains(@class,'toast-content--success')]"
            oApplicationStage = "//*[text()='Application Stage']"
            for index, row in enumerate(data):
                if row[8].lower() == "No".lower():
                    fullname = row[0].split(" ")
                    if len(fullname) == 3:
                        oFname = fullname[0]
                        oMname = fullname[1]
                        oLname = fullname[2]
                    else:
                        raise Exception("Name is invalid Please enter the full name of the candidate " + row[0])
                    self.navigate("Recruitment")
                    self.fluentWait(oAddBtn, "Add Button", 10)
                    self.driver.find_element(By.XPATH, oAddBtn).click()
                    self.fluentWait(oFirstName, "First Name", 10)
                    self.driver.find_element(By.XPATH, oFirstName).send_keys(oFname)
                    self.fluentWait(oMiddleName, "Middle Name", 10)
                    self.driver.find_element(By.XPATH, oMiddleName).send_keys(oMname)
                    self.fluentWait(oLastName, "Last Name", 10)
                    self.driver.find_element(By.XPATH, oLastName).send_keys(oLname)
                    self.fluentWait(oVacancy, "Vacancy", 10)
                    self.driver.find_element(By.XPATH, oVacancy).click()
                    self.driver.find_element(By.XPATH, oVacancyName.format(postName=row[1])).click()
                    self.fluentWait(oEmail, "Email", 10)
                    self.driver.find_element(By.XPATH, oEmail).send_keys(row[2])
                    self.fluentWait(oContactNumber, "Contact Number", 10)
                    self.driver.find_element(By.XPATH, oContactNumber).send_keys(row[4])
                    # self.fluentWait(oResume, "Resume", 10)
                    # self.driver.find_element(By.XPATH, oResume).send_keys("/Users/monilshah/PycharmProjects/automationBots/testBot/geckodriver.log")
                    self.fluentWait(oKeywords, "Keywords", 10)
                    self.driver.find_element(By.XPATH, oKeywords).send_keys(row[5])
                    self.fluentWait(oDateofApplication, "Date of Application", 10)
                    self.driver.find_element(By.XPATH, oDateofApplication).send_keys(
                        Keys.COMMAND + "A" + Keys.BACKSPACE)
                    self.driver.find_element(By.XPATH, oDateofApplication).send_keys(row[6])
                    self.fluentWait(oNotes, "Notes", 10)
                    self.driver.find_element(By.XPATH, oNotes).send_keys(row[7])
                    self.fluentWait(oConsentCheckbox, "Consent Checkbox", 10)
                    self.driver.find_element(By.XPATH, oConsentCheckbox).click()
                    self.fluentWait(oSave, "Save", 10)
                    self.driver.find_element(By.XPATH, oSave).click()
                    self.fluentWait(oSuccess, "Success", 10)
                    self.updateFlag(index, "Yes", "Success")
                    logging.warning(row[0] + " candidate is added successfully in to the System.")
                    self.fluentWait(oApplicationStage, "Application Stage", 15)
                else:
                    logging.error(row[0] + " is already added in to the System.")

        except Exception as e:
            self.updateFlag(index, "Yes", e)
            raise Exception("Unable to add the candidate.", e)


try:
    test = TestBot()
    test.launch("https://opensource-demo.orangehrmlive.com")
    test.login(username="Admin", password="admin123")
    test.addCandidate(test.readExcel())
except Exception as e:
    raise Exception("Something went wrong!!!! ", e)
