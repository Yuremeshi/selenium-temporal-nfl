import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import csv
from temporalio import activity
from dotenv import load_dotenv
import psycopg2
import os

FIRST_N_PLAYERS = 100

def func_element(driver: WebDriver, by: By, locator: str, wait: int = 10) -> WebElement:
    return WebDriverWait(driver, wait).until(EC.presence_of_element_located((by, locator)))

def func_elements(driver: WebDriver, by: By, locator: str, wait: int = 10) -> List[WebElement]:
    return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((by, locator)))

@activity.defn
async def selenium_scraper() -> None:
    driver = webdriver.Firefox()
    driver.get('https://nfl-stats-chi.vercel.app/')
    
    headers_list = ['first_name', 'last_name', 'pos_num', 'ht_wt', 'age', 'college', 'experience']
    player_stats_list = [headers_list]
    counter = 0

    years_element = func_element(driver, By.ID, 'headlessui-listbox-button-:R1lt9uja:')
    years_element.click()
    years_elements = func_elements(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[3]/div/div/div/div/span')
    year_iter = len(years_elements)
    for i in range(1, year_iter):
        if counter == FIRST_N_PLAYERS:
            break
        if i > 1:
            years_element.click()
            years_elements = func_elements(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[3]/div/div/div/div/span')
            time.sleep(1)
        year_select = years_elements[i]
        year_select.click()
        teams_element = func_element(driver, By.ID, 'headlessui-combobox-input-:Rdl9uja:')
        teams_element.click()
        teams_elements = func_elements(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[2]/div/div/div/div/div')
        teams_iter = len(teams_elements)
        for j in range(teams_iter):
            if counter == FIRST_N_PLAYERS:
                break
            if j > 0:
                teams_element.click()
                teams_elements = func_elements(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[2]/div/div/div/div/div')
                time.sleep(1)
            team_select = teams_elements[j]
            team_select.click()
            button_element = func_element(driver, By.XPATH, '/html/body/main/div/div[2]/form/div[3]/button')
            button_element.click()
            player_elements = func_elements(driver, By.CLASS_NAME, 'border-2.border-gray-400.p-3.cursor-pointer.mb-2.rounded-md')
            player_iter = len(player_elements)
            time.sleep(1)            
            for k in range(player_iter):
                if counter == FIRST_N_PLAYERS:
                    break
                player_select = player_elements[k]
                player_select.click()
                player_first = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/h1[1]')
                player_last = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/h1[2]')
                player_number = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/p')
                player_body = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/p[2]')
                player_age = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/p[2]')
                player_college = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[3]/p[2]')
                player_exp = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[4]/p[2]')
                player_stats_list.append([
                    player_first.text,
                    player_last.text,
                    player_number.text,
                    player_body.text,
                    player_age.text,
                    player_college.text,
                    player_exp.text
                ])
                counter += 1
                close = func_element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/button')
                close.click()

    filename = "output.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in player_stats_list:
            writer.writerow(row)
    
    driver.quit()

@activity.defn
async def postgres() -> None:
    load_dotenv()
    
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS player_stats (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    pos_num TEXT,
    ht_wt TEXT,
    age TEXT,
    college TEXT,
    experience TEXT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    csv_path = f"./output.csv"
    reader = csv.DictReader(open(csv_path))
    for row in reader:
        insert_query = """
        INSERT INTO player_stats (first_name, last_name, pos_num, ht_wt, age, college, experience)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['first_name'],
            row['last_name'],
            row['pos_num'],
            row['ht_wt'],
            row['age'],
            row['college'],
            row['experience']
        )
        cursor.execute(insert_query, values)
        conn.commit()

    cursor.close()
    conn.close()