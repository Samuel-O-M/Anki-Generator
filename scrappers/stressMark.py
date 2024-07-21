from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def setup_driver():

    driver = webdriver.Chrome()
    driver.get("https://russiangram.com")

    time.sleep(0.5)

    russian_visible = driver.find_element(By.ID, "russian-visible")
    if not russian_visible.is_selected():
        russian_visible.click()
    
    stress_style = driver.find_element(By.ID, "stress-style-accent")
    stress_style.click()

    return driver

def stress_mark(input, driver):

    textarea = driver.find_element(By.ID, "MainContent_UserSentenceTextbox")
    textarea.clear()
    textarea.send_keys(input)
    
    textarea.send_keys(Keys.CONTROL, Keys.RETURN)
        
    russian_visible = driver.find_element(By.ID, "russian-visible")
    if not russian_visible.is_selected():
        russian_visible.click()
    
    stress_style = driver.find_element(By.ID, "stress-style-accent")
    stress_style.click()
    
    updated_textarea = driver.find_element(By.ID, "MainContent_UserSentenceTextbox")
    result_text = updated_textarea.get_attribute("value")

    return result_text

def close_driver(driver):

    driver.quit()

if __name__ == "__main__":

    # Speed test
    
    driver = setup_driver()
    
    print(stress_mark("человек", driver))
    print(stress_mark("сказать", driver))
    print(stress_mark("человек", driver))
    print(stress_mark("сказать", driver))
    print(stress_mark("человек", driver))
    print(stress_mark("сказать", driver))
    print(stress_mark("человек", driver))
    print(stress_mark("сказать", driver))
    
    close_driver(driver)
