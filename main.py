# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
# import time
# import os
# from dotenv import load_dotenv
# import undetected_chromedriver as uc
# from datetime import datetime

# load_dotenv()

# chrome_options=uc.ChromeOptions()
# prefs = {
#     "download.prompt_for_download": False,
#     "directory_upgrade": True, 
#     "safebrowsing.enabled": True,
# }

# chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# ## Initialize driver

# driver=uc.Chrome(options=chrome_options)
# driver.maximize_window()
# wait=WebDriverWait(driver, 60)
# shortWait=WebDriverWait(driver, 15)

# try:
#     web_url = "https://www.sec.gov/edgar/search/#"
#     driver.get(web_url)
#     print("Opening Website...")

#     wait.until(EC.element_to_be_clickable((By.ID, 'show-full-search-form'))).click()
#     print("Clicked on 'more search options'")

#     # Keyword box
#     wait.until(EC.element_to_be_clickable((By.ID, 'keywords'))).send_keys(os.getenv('FIRST_KW'))
#     time.sleep(2)
    
#     # ticker box
#     wait.until(EC.element_to_be_clickable((By.ID, 'entity-full-form'))).send_keys(os.getenv('COMPANY_1'))
#     time.sleep(2)
    
#     # Browse filling types
#     wait.until(EC.element_to_be_clickable((By.ID, 'show-filing-types'))).click()
#     print("Clicked on Browse filling types")
#     time.sleep(2)
    
#     # fcbd-1-K     fcbd-10-Q     fcb6
#     # 1-K filter
#     # Select the 1-K checkbox by label
#     checkbox_label1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='1-K']")))
#     driver.execute_script("arguments[0].click();", checkbox_label1)
#     print("1-K checkbox selected")
#     time.sleep(2)
    
#     # Select the 10-Q checkbox by label
#     checkbox_label2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='10-Q']")))
#     driver.execute_script("arguments[0].click();", checkbox_label2)
#     print("10-Q checkbox selected")
#     time.sleep(2)
    
#     # Filter 
#     wait.until(EC.element_to_be_clickable((By.ID, 'custom_forms_set'))).click()
#     print("Clicked on filter")
#     time.sleep(5)
    
#     # Submit
#     wait.until(EC.element_to_be_clickable((By.ID, 'search'))).click()
#     print("Submitted")
#     time.sleep(2)
    
#     driver.execute_script("window.scrollBy(0, 500);")
#     time.sleep(1)
    
    
    
#     # flow after table appears
#     # Wait for the filings table to load
#     print("Waiting for filings table to appear...")               
#     table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hits"]/table')))
#     rows = table.find_elements(By.XPATH, ".//tbody/tr")
#     print(f"Found {len(rows)} rows in the filings table.")

#     latest_date = None
#     latest_row = None

#     # Loop through each row to find the latest 'Filed' date
#     for row in rows:
#         try:
#             filed_date_text = row.find_element(By.XPATH, ".//td[contains(@class,'filed')]").text.strip()
#             filed_date = datetime.strptime(filed_date_text, "%Y-%m-%d")

#             if latest_date is None or filed_date > latest_date:
#                 latest_date = filed_date
#                 latest_row = row
#         except Exception as e:
#             continue
    
#     print(f"1.latest date --> {latest_date}")
#     print(f"2.latest row --> {latest_row}")
    
#     if latest_row:
#         try:
#             # Get the link element inside "Form & File" column
#             link_element = latest_row.find_element(By.XPATH, ".//td[contains(@class,'filetype')]/a")
#             report_url = link_element.get_attribute("href")

#             print(f"Latest filing date: {latest_date.strftime('%Y-%m-%d')}")
#             print(f"Opening link: {report_url}")

#             # Scroll and click
#             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_element)
#             time.sleep(1)
#             link_element.click()
#         except Exception as e:
#             print(f" Failed to click the latest report link: {e}")
#     else:
#         print(" No valid filing rows found.")

        

#     print("Paused for Enter")
#     input("Enter to continue...")
    
# finally:
#     driver.quit()
#     print("Driver Closed.")

## 2. Approach No 2
print("Hello 1")

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import os
import re
from dotenv import load_dotenv
import undetected_chromedriver as uc
from datetime import datetime
from bs4 import BeautifulSoup


print("Hello 2")

load_dotenv()

FIRST_KW = os.getenv('FIRST_KW')
COMPANY_1 = os.getenv('COMPANY_1') # Alcoa Corp (AA)
COMPANY_2 = os.getenv('COMPANY_2') # TSLA
COMPANY_3 = os.getenv('COMPANY_3') # NVDA

# keyword = os.getenv('FIRST_KW')
# print(f"keyword:- {keyword}")
COMPANY = COMPANY_1

chrome_options=uc.ChromeOptions()
prefs = {
    "download.prompt_for_download": False,
    "directory_upgrade": True, 
    "safebrowsing.enabled": True,
}

chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
print("Hello 3")
## Initialize driver

driver=uc.Chrome(options=chrome_options)
driver.maximize_window()
wait=WebDriverWait(driver, 60)
shortWait=WebDriverWait(driver, 15)

def scroll(value):
    driver.execute_script(f"window.scrollBy(0, {value});")

print("Hello 4 - Browser Initialized")

try:
    web_url = "https://www.sec.gov/edgar/search/#"
    driver.get(web_url)
    print("Opening Website...")

    wait.until(EC.element_to_be_clickable((By.ID, 'show-full-search-form'))).click()
    print("Clicked on 'more search options'")

    # Keyword box
    wait.until(EC.element_to_be_clickable((By.ID, 'keywords'))).send_keys(FIRST_KW)
    time.sleep(1)
    
    # ticker box
    wait.until(EC.element_to_be_clickable((By.ID, 'entity-full-form'))).send_keys(COMPANY)
    time.sleep(1)
    
    # Browse filling types
    wait.until(EC.element_to_be_clickable((By.ID, 'show-filing-types'))).click()
    print("Clicked on Browse filling types")
    time.sleep(1)
    
    # fcbd-1-K     fcbd-10-Q     fcb6
    # 1-K filter
    # Select the 1-K checkbox by label
    for label_text in ["1-K", "10-Q"]:
        checkbox_label = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space()='{label_text}']")))
        driver.execute_script("arguments[0].click();", checkbox_label)
        print(f"{label_text} checkbox selected")
        time.sleep(1)
    
    # Filter 
    wait.until(EC.element_to_be_clickable((By.ID, 'custom_forms_set'))).click()
    print("Clicked on filter")
    time.sleep(5)
    
    # Submit
    wait.until(EC.element_to_be_clickable((By.ID, 'search'))).click()
    print("Submitted")
    time.sleep(1)
    
    scroll(value=500)
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

            form_type = latest_row.find_element(By.XPATH, ".//td[contains(@class,'filetype')]").text.strip()  # NEW ↓
            print(f"Latest filing date: {latest_date.strftime('%Y-%m-%d')}")
            print(f"Opening link: {report_url}")

            # Scroll and click
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_element)
            time.sleep(1)
            link_element.click()
        except Exception as e:
            print(f" Failed to click the latest report link: {e}")
    else:
        print(" No filing rows found.")
        driver.quit()
        exit()

    
    ## Logic After clicking on the link

    time.sleep(5)
    
    open_doc_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="open-file"]')))
    open_doc_button.click()
    print("Clicked on Open Document")
    
    time.sleep(3)
    
    tabs = driver.window_handles
    
    if len(tabs) > 1:
        driver.switch_to.window(tabs[-1])
        print("Switched to the new tab.")
    else:
        print("New tab not found.")
    
    time.sleep(5)
    
    # driver.execute_script("window.scrollBy(0, 500);")
    # time.sleep(2)
    
    ## Text Extraction from the document
    print("Current tab title: ", driver.title)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")
    
    # Get the full text content (without tags)
    full_text = soup.get_text(separator="\n", strip=True)
    
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    clean_text = "\n".join(lines)
    
    # Define the keyword you want to search for
    keyword = "cyber"

    # Split text into rough "paragraphs" (based on double line breaks or periods)
    paragraphs = re.split(r'\n{2,}|\.\s', clean_text)

    # Search for keyword in each paragraph
    matched_paragraphs = [p for p in paragraphs if keyword.lower() in p.lower()]
    
    output_text = ""  # NEW ↓

    if matched_paragraphs:
        print(f"\n Found {len(matched_paragraphs)} paragraph with keyword '{keyword}':\n")
        output_text += f"\nFound {len(matched_paragraphs)} paragraph with keyword '{keyword}':\n"
        for idx, para in enumerate(matched_paragraphs, 1):
            print(f"{idx}. {para}\n")
            output_text += f"\n{idx}. {para}\n"
    else:
        print(f"No paragraphs found containing '{keyword}'")
        output_text += f"No paragraphs found containing '{keyword}'"
    
    # # Method 2: Line-based context search 
    # lines = clean_text.split("\n")
    # for i, line in enumerate(lines):
    #     if keyword.lower() in line.lower():
    #         start = max(0, i - 2)
    #         end = min(len(lines), i + 3)
    #         context = "\n".join(lines[start:end])
    #         print(f"\nFound around line {i+1}:\n{context}\n")
    
    
    # ---- Save Results ----
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{COMPANY}_{form_type}_{timestamp}.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Company: {COMPANY}\n")
        f.write(f"Form Type: {form_type}\n")
        f.write(f"Filing Date: {latest_date.strftime('%Y-%m-%d')}\n")
        f.write(f"Report URL: {report_url}\n")
        f.write(f"Keyword: {keyword}\n")
        f.write("=" * 80 + "\n\n")
        f.write(output_text)

    print(f"\nOutput saved to: {output_file}")

    input("Press Enter to close browser...")
    
finally:
    driver.quit()
    print("Driver Closed.")