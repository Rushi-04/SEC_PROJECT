from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import os
from dotenv import load_dotenv
import undetected_chromedriver as uc
from datetime import datetime

load_dotenv()

chrome_options=uc.ChromeOptions()
prefs = {
    "download.prompt_for_download": False,
    "directory_upgrade": True, 
    "safebrowsing.enabled": True,
}

chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

## Initialize driver

driver=uc.Chrome(options=chrome_options)
driver.maximize_window()
wait=WebDriverWait(driver, 60)
shortWait=WebDriverWait(driver, 15)

try:
    web_url = "https://www.sec.gov/edgar/search/#"
    driver.get(web_url)
    print("Opening Website...")

    wait.until(EC.element_to_be_clickable((By.ID, 'show-full-search-form'))).click()
    print("Clicked on 'more search options'")

    # Keyword box
    wait.until(EC.element_to_be_clickable((By.ID, 'keywords'))).send_keys(os.getenv('FIRST_KW'))
    time.sleep(2)
    
    # ticker box
    wait.until(EC.element_to_be_clickable((By.ID, 'entity-full-form'))).send_keys(os.getenv('COMPANY_1'))
    time.sleep(2)
    
    # Browse filling types
    wait.until(EC.element_to_be_clickable((By.ID, 'show-filing-types'))).click()
    print("Clicked on Browse filling types")
    time.sleep(2)
    
    # fcbd-1-K     fcbd-10-Q     fcb6
    # 1-K filter
    # Select the 1-K checkbox by label
    checkbox_label1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='1-K']")))
    driver.execute_script("arguments[0].click();", checkbox_label1)
    print("1-K checkbox selected")
    time.sleep(2)
    
    # Select the 10-Q checkbox by label
    checkbox_label2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='10-Q']")))
    driver.execute_script("arguments[0].click();", checkbox_label2)
    print("10-Q checkbox selected")
    time.sleep(2)
    
    # Filter 
    wait.until(EC.element_to_be_clickable((By.ID, 'custom_forms_set'))).click()
    print("Clicked on filter")
    time.sleep(5)
    
    # Submit
    wait.until(EC.element_to_be_clickable((By.ID, 'search'))).click()
    print("Submitted")
    time.sleep(2)
    
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)
    
    
    
    
    
    
    # Wait for the table to load
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='table']//tbody/tr")))

    rows = driver.find_elements(By.XPATH, "//table[@class='table']//tbody/tr")
    print(f"Total rows found: {len(rows)}")

    records = []
    for row in rows:
        filed_date_text = row.find_element(By.XPATH, "./td[@class='filed']").text.strip()
        link_element = row.find_element(By.XPATH, "./td[@class='filetype']/a")
        link_href = link_element.get_attribute("href")
        link_text = link_element.text.strip()
        
        filed_date = datetime.strptime(filed_date_text, "%Y-%m-%d")
        
        records.append({
            "date": filed_date,
            "link": link_href,
            "text": link_text,
            "element": link_element
        })

    # Find the latest date
    latest_record = max(records, key=lambda x: x["date"])
    print(f"Latest filing: {latest_record['text']} on {latest_record['date'].date()}")

    # Scroll and click
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", latest_record["element"])
    time.sleep(1)
    driver.execute_script("arguments[0].click();", latest_record["element"])
    print(f"Clicked on latest filing: {latest_record['text']}")
    
    print("Paused for Enter")
    input("Enter to continue...")
    
finally:
    driver.quit()
    print("Driver Closed.")