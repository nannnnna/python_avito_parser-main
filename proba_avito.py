# import requests
import datetime
import time

# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Настройка опций для Chrome WebDriver
options = Options()
options.add_argument("window-size=1200x600")
options.add_argument("user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")



cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
url = 'https://www.avito.ru/'
driver_path = "chromedriver.exe"
service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url)
    time.sleep(5)  # Подождите некоторое время для полной загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".visual-rubricator-gridItem-VHHHg"))
    )

    category_elements = driver.find_elements(By.CSS_SELECTOR, ".visual-rubricator-gridItem-VHHHg")
    
    categories = {}
    for element in category_elements:
        category_name = element.find_element(By.CSS_SELECTOR, "p").text
        category_link = element.get_attribute("href")
        categories[category_name] = category_link

    # Сохранение категорий и ссылок в файл
    with open('categories.txt', 'w', encoding='utf-8') as file:
        for name, link in categories.items():
            file.write(f"{name}: {link}\n")
    
except TimeoutException:
    print("Страница не загрузилась в течение заданного времени")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    driver.quit()

