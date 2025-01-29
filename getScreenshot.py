import time
import getConfig, getVideoScript
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

screenW, screenH = getConfig.get_screen_config()
dir = getConfig.get_screenshot_directory()

def getPostScreenshots(id, script):
    driver, wait = __setup_driver(script.url)
    script.titleSCFile = __take_screenshot(driver, wait, f"post-title-t3_{id}")
    script.textSCFile = __take_screenshot(driver, wait, f"t3_{id}-post-rtjson-content")
    print(script.url)
    for commentFrame in script.frames:
        print(f"t1_{commentFrame.commentId}-comment-rtjson-content")
        commentFrame.screenShotFile = __take_screenshot(driver, wait, f"t1_{commentFrame.commentId}-comment-rtjson-content")
    driver.quit()

def __take_screenshot(driver, wait, handle):
    method = By.ID
    search = wait.until(EC.presence_of_element_located((method, handle)))
    driver.execute_script("window.focus();")
    fileName = f"{dir}/{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def __setup_driver(url):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenW, height=screenH)
    driver.get(url)

    time.sleep(10)

    try:
        # Repeatedly check for the close button (max 5 seconds)
        for _ in range(10):  
            try:
                close_button = driver.find_element(By.XPATH, '//*[@id="close"]')
                if close_button.is_displayed():
                    close_button.click()
                    print("Closed login popup.")
                    break
            except:
                time.sleep(0.5)  # Wait and retry
    except Exception as e:
        print("No login popup found or could not close it.", e)

    return driver, wait