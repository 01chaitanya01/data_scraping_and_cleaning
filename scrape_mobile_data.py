from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

url = "https://www.flipkart.com/search?q=mobiles"

driver.get(url)

mobiles = []

try:
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_75nlfW']"))
        )
        products = driver.find_elements(By.XPATH, "//div[@class='_75nlfW']")

        for product in products:
            try:
                name = product.find_element(By.XPATH, ".//div[@class='KzDlHZ']").text
                price = product.find_element(By.XPATH, ".//div[@class='hl05eU']").text
                description = product.find_element(By.XPATH, ".//div[@class='_6NESgJ']").text

                mobiles.append({
                    'name': name,
                    'price': price,
                    'sizeInCm': description,
                    'sizeInInch': description 
                })
            except Exception as e:
                print(f"Error fetching data for product: {e}")
                continue

        try:
            nextBtn = driver.find_element(By.PARTIAL_LINK_TEXT, "NEXT")
            nextBtn.click()
            time.sleep(5) 
        except Exception as e:
            print(f"Error going to next page: {e}")
            break

finally:
    df = pd.DataFrame(mobiles)
    df.to_csv("scrapped_mobile_data.csv", index=False)

    driver.quit()