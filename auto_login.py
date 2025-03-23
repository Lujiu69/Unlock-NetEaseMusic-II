# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A61CCF94F02323E01855A5782DA3852C224A07D3382B6481932F41D653653FF771CB54FFFFA852F4DF4560A5FCD5277A07815F846F32644005133184976CC0EF82C94EE60B5AC1BC2A5DF13856B373E70E492FBBC646B08CCC5B64919DDC140FD46E32336BFEB94379D78022B0CCE16CC11362E012D7994F1C147ADB984A275D35CF7BB60EBE0AD94D6F20F2BA10FFD7C31ED437A05E92C2F7C526A01526D68E64E6C33C022AF1C8641729A9EB5DEB716161A876DE5EABF3705AC95D8F51CCA9D4BFA7078C55F4D2F66F09103E67CAFE32263DB8354FCD8221F519A8483E42223530BD05C0DB0DC9048B42206424654EDABE7469DA85F896CE7705D9389C5E965EA2D10404F0F76EE66FDE1E7E3FE994E8C97BBEC435DCDA6BDA01A2D8EC7EC651E313E1ACD3C0F38E759345D7013250313C89E33B516F67ABEE0D007EBDC1CCE010A9AFB8BFE81DEFCD3C8EB316D10B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
