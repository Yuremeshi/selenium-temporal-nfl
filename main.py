from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import csv

FIRST_N_PLAYERS = 20

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

headers_list = ['first_name', 'last_name', 'ht/wt', 'age', 'college', 'exp']
player_stats_list = [headers_list]
counter = 0

years_element = func_element(driver, By.ID, 'headlessui-listbox-button-:R1lt9uja:')
years_element.click()
years_elements = func_elements(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[3]/div/div/div/div/span')
year_iter = len(years_elements)
for i in range(1, year_iter):
    if counter == FIRST_N_PLAYERS:
        break
    year_select = years_elements[i]
    year_select.click()
    teams_element = func_element(driver, By.ID, 'headlessui-combobox-input-:Rdl9uja:')
    teams_element.click()
    teams_elements = func_elements(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[2]/div/div/div/div/div')
    teams_iter = len(teams_elements)
    for j in range(teams_iter):
        if counter == FIRST_N_PLAYERS:
            break
        team_select = teams_elements[j]
        team_select.click()
        button_element = func_element(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[3]/button')
        button_element.click()
        player_elements = func_elements(driver, By.CLASS_NAME, 'border-2.border-gray-400.p-3.cursor-pointer.mb-2.rounded-md')
        player_iter = len(player_elements)
        
        for k in range(player_iter):
            if counter == FIRST_N_PLAYERS:
                break
            player_select = player_elements[k]
            player_select.click()
            player_first = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/h1[1]')
            player_last = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/h1[2]')
            player_body = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/p[2]')
            player_age = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/p[2]')
            player_college = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[3]/p[2]')
            player_exp = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[4]/p[2]')
            player_stats_list.append([
                player_first.text,
                player_last.text,
                player_body.text,
                player_age.text,
                player_college.text,
                player_exp.text
            ])
            counter += 1
            print(player_stats_list)
            close = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/button')
            close.click()

filename="output.csv"

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in player_stats_list:
        writer.writerow(row)

driver.quit()


# year_element = driver.find_element(By.ID, 'headlessui-listbox-button-:R1lt9uja:')
# year_element.click()
# year_select = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/form/div[3]/div/div/div/div[9]/span')
# year_select.click()
# team_element = driver.find_element(By.ID, 'headlessui-combobox-input-:Rdl9uja:')
# team_element.click()
# team_select = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/form/div[2]/div/div/div/div[22]/div')
# team_select.click()
# button_element = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/form/div[3]/button')
# button_element.click()
# player_elements = WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, 'border-2.border-gray-400.p-3.cursor-pointer.mb-2.rounded-md'))
# )
# for player_element in player_elements:
#     player_element.click()
#     player_stats = func_elements(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]')
#     iterations = len(player_stats)
#     for i in range(iterations):
#         player_stat = player_stats[i]
#         print(player_stat.text)
#         close = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/button')
#         close.click()