# Test Case:
# _____________________________________________________
# 1. Go to https://opensource-demo.orangehrmlive.com/
# 2. Enter Username - Admin
# 3. Enter Password - admin123
# 4. Click on Login
# 5. Capture the actual title
# 6. Capture the expected title
# 7. close Browser


from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)

driver = webdriver.Firefox(executable_path=".\..\WebDrivers\geckodriver")
# driver = webdriver.Firefox(options=options ,executable_path=".\..\WebDrivers\geckodriver")
driver.get("https://opensource-demo.orangehrmlive.com/")
driver.implicitly_wait(10)

# Pass the xpath and it will wait for the element to be visible
def fluentWait(xpath):
    try:
        # wait for typed text animation completed
        wait = WebDriverWait(driver, timeout=10)
        typing_completed = wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath),
                                                                       xpath + " is not present in the view"))
        if typing_completed:
            element = driver.find_element_by_id("typed")
            print(f"Full text typed: {element.text}")

    except TimeoutException:
        print("Timed out waiting for typing animation!")


try:
    fluentWait("//*[@name='username']")
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
finally:
    print("Success")
    driver.close()


