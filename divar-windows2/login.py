from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv



chrome_options = Options()

user_data_folder = r"C:\path\to\custom\profile"
chrome_options.add_argument(f"--user-data-dir={user_data_folder}")

print("login kon...")
time.sleep(2)
driver = webdriver.Chrome(options=chrome_options)


driver.get("http://www.divar.ir")




try:
    while True:
        pass  # Keeps the script running
except KeyboardInterrupt:
    print("\nExiting script. Browser will remain open.")
    
