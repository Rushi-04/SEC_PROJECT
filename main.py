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
    
    
    
    # flow after table appears
    # Wait for the filings table to load
    print("Waiting for filings table to appear...")               
    table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hits"]/table')))
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    print(f"Found {len(rows)} rows in the filings table.")

    latest_date = None
    latest_row = None

    # Loop through each row to find the latest 'Filed' date
    for row in rows:
        try:
            filed_date_text = row.find_element(By.XPATH, ".//td[contains(@class,'filed')]").text.strip()
            filed_date = datetime.strptime(filed_date_text, "%Y-%m-%d")

            if latest_date is None or filed_date > latest_date:
                latest_date = filed_date
                latest_row = row
        except Exception as e:
            continue
    
    print(f"1.latest date --> {latest_date}")
    print(f"2.latest row --> {latest_row}")
    
    if latest_row:
        try:
            # Get the link element inside "Form & File" column
            link_element = latest_row.find_element(By.XPATH, ".//td[contains(@class,'filetype')]/a")
            report_url = link_element.get_attribute("href")

            print(f"Latest filing date: {latest_date.strftime('%Y-%m-%d')}")
            print(f"Opening link: {report_url}")

            # Scroll and click
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_element)
            time.sleep(1)
            link_element.click()
        except Exception as e:
            print(f" Failed to click the latest report link: {e}")
    else:
        print(" No valid filing rows found.")

        

    print("Paused for Enter")
    input("Enter to continue...")
    
finally:
    driver.quit()
    print("Driver Closed.")