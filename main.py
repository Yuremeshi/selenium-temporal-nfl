from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List

def func_element(driver: WebDriver, by: By, locator: str, wait: int = 10) -> WebElement:
    """Find single element after waiting wait seconds"""
    return WebDriverWait(driver, wait).until(
        EC.presence_of_element_located((by, locator))
    )

def func_elements(driver: WebDriver, by: By, locator: str, wait: int = 10) -> List[WebElement]:
    """Find all elements after waiting wait seconds"""
    return WebDriverWait(driver, wait).until(
        EC.presence_of_all_elements_located((by, locator))
    )

driver = webdriver.Firefox()
driver.get('https://nfl-stats-chi.vercel.app/')
# years_element = func_element(driver, By.ID, 'headlessui-listbox-button-:R1lt9uja')
# years_element.click()
# year_iter = len(years_element)
# for i in range(year_iter - 1):
#     year_select = years_element[i + 1]
#     year_select.click()
#     teams_element = func_elements(driver, By.ID, 'headlessui-combobox-input-:Rdl9uja:')
#     teams_iter = len(teams_element)
#     for j in range(teams_iter):
#         team_select = teams_element[j]
#         team_select.click()
#         button_element = func_element(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[3]/button')
#         button_element.click()
#         player_elements = func_elements(driver, By.CLASS_NAME, 'border-2.border-gray-400.p-3.cursor-pointer.mb-2.rounded-md')
#         player_iter = len(player_elements)
#         for k in range(player_iter):
#             player_select = player_elements[k]
#             player_select.click()
#             player_stats = func_elements(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]')
#             stats_iter = len(player_stats)
#             for l in range(stats_iter):
#                 player_stat = player_stats[l]
#                 print(player_stat.text)
#                 close = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/button')
#                 close.click()


year_element = driver.find_element(By.ID, 'headlessui-listbox-button-:R1lt9uja:')
year_element.click()
year_select = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/form/div[3]/div/div/div/div[9]/span')
year_select.click()
team_element = driver.find_element(By.ID, 'headlessui-combobox-input-:Rdl9uja:')
team_element.click()
team_select = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/form/div[2]/div/div/div/div[22]/div')
team_select.click()
button_element = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/form/div[3]/button')
button_element.click()
player_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'border-2.border-gray-400.p-3.cursor-pointer.mb-2.rounded-md'))
)
for player_element in player_elements:
    player_element.click()
    player_stats = func_elements(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]')
    iterations = len(player_stats)
    for i in range(iterations):
        player_stat = player_stats[i]
        print(player_stat.text)
        close = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/button')
        close.click()


driver.quit()