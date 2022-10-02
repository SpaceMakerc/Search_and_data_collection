from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get("https://account.mail.ru/login/")
driver.implicitly_wait(30)
action = ActionChains(driver)
base = MongoClient("localhost:27017")
db = base['db_mail']
mail_ru = db.mail_ru

element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME, 'username')))
element.send_keys("study.ai_172")
button_log = driver.find_element(By.XPATH, "//button[@class='base-0-2-87 primary-0-2-101 auto-0-2-113']")
button_log.click()
#sleep(2.0)
password = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME, 'password')))
password.send_keys('NextPassword172#')
button_pas = driver.find_element(By.XPATH, "//button[@class='base-0-2-87 primary-0-2-101 auto-0-2-113']")
button_pas.click()

list_links = []
checker = None

while True:
    messages = driver.find_elements(By.XPATH, "//span[@class='ll-crpt']/ancestor::a")
    if messages[-1] == checker:
        break
    for message in messages:
        if message:
            link = message.get_attribute("href")
            if link not in list_links:
                list_links.append(link)
    checker = messages[-1]
    action.move_to_element(checker)
    action.perform()

for i in list_links:
    driver.get(i)
    data = {
        'by_who' : driver.find_element(By.XPATH, "//div[@class='letter__author']/span").text,
        'date' : driver.find_element(By.XPATH, "//div[@class='letter__date']").text,
        'theme' : driver.find_element(By.TAG_NAME, 'h2').text,
        'link' : i
    }
    try:
        mail_ru.insert_one(data)
    except DuplicateKeyError:
        print(f'письмо {i} уже есть в базе')

print()