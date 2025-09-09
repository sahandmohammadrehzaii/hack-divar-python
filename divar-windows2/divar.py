from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv

def append_to_csv_old(a, b, filename="data.csv"):
    # Open the CSV file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Append the values of a and b as a new row
        writer.writerow([a, b])


def append_to_csv(a, b, filename="data.csv"):
    # Open the CSV file in append mode with utf-8 encoding
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Append the values of a and b as a new row
        writer.writerow([a, b])
    


animation_script_toblue = """
        let element = arguments[0];

        // Store the original font size and color
        let originalFontSize = window.getComputedStyle(element).fontSize;
        let originalColor = window.getComputedStyle(element).color;

        // Apply the transition properties for font size and color change
        element.style.transition = 'font-size 0.5s ease-in-out, color 0.5s ease-in-out';  // Adjust timing here

        // Increase font size by 3rem and change color to white
        setTimeout(() => {
            element.style.fontSize = 'calc(' + originalFontSize + ' + 1rem)';  // Increase font size by 3rem
            element.style.color = 'white';  // Change text color to white
        }, 500);  // Start the animation after 500ms

        // Reset after animation
        setTimeout(() => {
            element.style.fontSize = originalFontSize;  // Reset font size
            element.style.color = originalColor;  // Reset color
        }, 1700);  // 
    """
    
animation_script = """
        let element = arguments[0];

        // Store the original background color
        let originalBackground = window.getComputedStyle(element).backgroundColor;

        // Get element's bounding rectangle to calculate position
        let rect = element.getBoundingClientRect();

        // Add styles for smooth transitions
        element.style.transition = 'transform 0.33s ease-in-out, background-color 0.33s ease-in-out';  // 1.5x faster

        // Zoom in and change background color to semi-transparent red
        setTimeout(() => {
            element.style.transform = 'scale(1.2)';  // Zoom in once
            element.style.backgroundColor = 'rgba(255, 0, 0, 0.8)';  // Semi-transparent red
        }, 500);  // Start animation after a short delay

        // Move the position of the element (slightly lower than middle)
        setTimeout(() => {
            element.style.transition = 'transform 0.33s ease-in-out, background-color 0.33s ease-in-out';  // Keep same speed
            element.style.transform = 'scale(1.2)';  // Maintain zoom while moving
            element.style.backgroundColor = 'rgba(255, 0, 0, 0.8)';  // Maintain background color change
        }, 500);  // Start the movement after the zoom begins

        // Reset after animation
        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.backgroundColor = originalBackground;
        }, 1000);  // 
    """

def Find_Elements_By_XPATH(d,x):
    
    WebDriverWait(d, 35).until(
        EC.presence_of_all_elements_located((By.XPATH, x))
    )
    print(x)
    return d.find_elements(By.XPATH, x)

def Find_Element_By_XPATH(d,x):
    WebDriverWait(d, 30).until(
        EC.presence_of_element_located((By.XPATH, x))
    )
    return d.find_element(By.XPATH, x)    

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2)) 
        

chrome_options = Options()

user_data_folder = r"C:\path\to\custom\profile"
chrome_options.add_argument(f"--user-data-dir={user_data_folder}")

print("Start...")
time.sleep(2)
driver = webdriver.Chrome(options=chrome_options)


driver.get("http://www.divar.ir")



divar_search = Find_Element_By_XPATH(driver,'//*[@id="app"]/header/nav/div/div[2]/div/div/div[1]/form/input')
driver.execute_script(animation_script, divar_search)


human_typing(divar_search, "خیارشور")

time.sleep(1)
divar_search.send_keys(Keys.RETURN)
#time.sleep(10000)

def extract_phone_number(driver):
    print("look for phone")

    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
    )
    links = driver.find_elements(By.TAG_NAME, 'a')
    
    
    phone_number = "0"
    
    # Extract and store phone numbers from `href="tel:<phone>"` links
    for link in links:
        href_value = link.get_attribute("href")
        if href_value and href_value.startswith("tel:"):
            phone_number = href_value.replace("tel:", "").strip()
            driver.execute_script(animation_script_toblue, link)
    
    return phone_number

def getads():

    ads = []

    WebDriverWait(driver, 35).until(
        #EC.presence_of_element_located((By.XPATH, '//*[@id="post-list-container-id"]/div[1]/div/div/div/div[1]/div/div[2]' ))
        EC.presence_of_element_located((By.CLASS_NAME, "kt-post-card__info"))
    )
    
    cols = Find_Elements_By_XPATH(driver,'//*[@id="post-list-container-id"]/div[1]/div/div/div/div[*]')
    print("cols:")
    print(len(cols))      
    for col in cols:

        rows = Find_Elements_By_XPATH(col, './div/div[*]')        
        for ad in rows:

            if 'href="/v/' in ad.get_attribute("outerHTML"):
                ads.append(ad)
                
    return ads


passed = []


    
while True:

   for ad in getads():
       adId = Find_Element_By_XPATH(ad, './article/a').get_attribute('href').split('/')[-1]
       
       if adId not in passed:
           passed.append(adId)
           driver.execute_script(animation_script, ad)
           time.sleep(5)
           ad.click()
           
           WebDriverWait(driver, 30).until(
           EC.presence_of_all_elements_located((By.TAG_NAME, 'h1'))
           )
           
           h1 = driver.find_element(By.TAG_NAME, "h1")
           title = h1.text
           
           time.sleep(1)
           
           btn = Find_Element_By_XPATH(driver, '//*[@id="app"]/div[1]/div/main/article/div/div[1]/section[1]/div[2]/button')   
           driver.execute_script(animation_script, btn)
           time.sleep(1)
           btn.click()
           time.sleep(1)
           phone = extract_phone_number(driver)
           if phone != "0":
               print(phone+" -> "+title)
               append_to_csv(title,phone,"phones.csv")
           time.sleep(4)
           driver.back()
           time.sleep(1)
           break


try:
    while True:
        pass  # Keeps the script running
except KeyboardInterrupt:
    print("\nExiting script. Browser will remain open.")
    
