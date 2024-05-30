import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
# from selenium.webdriver import DesiredCapabilities
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service 
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

url = 'https://www.tokopedia.com/somethinc/review'
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
driver.get(url)

# desired_capabilities = DesiredCapabilities().CHROME.copy()
# desired_capabilities['acceptInsecureCerts'] = True

# driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities = desired_capabilities)
# driver.implicitly_wait(10)

# driver.get(url)
# print(driver.find_element(By.CLASS_NAME, 'shopee-product-rating').text)
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
# driver.get(url)
data=[]
username=[]
for i in range(0,5):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    containers = soup.findAll('article', attrs = {'class':'css-ccpe8t'})
    for container in containers:
        review = container.find('span', attrs={'data-testid': 'lblItemUlasan'})
        username2 = container.find('span', attrs={'class': 'name'})
        print(username2.text)
        
        if review:
            print(review.text)
            data.append({'Review': review.text})
            username.append({'Username' : username2.text})
        else:
            data.append({'Review': 'No review found'})  # Handle the case where 'review' is not found
            username.append({'Username' : username2.text})
        
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button[aria-label='Laman berikutnya']").click()
    time.sleep(3)

df = pd.DataFrame(data, username, columns=['Review', 'Username'])
print(df)

driver.close()

# Now, you can save the DataFrame to a CSV file
df.to_csv('scraping_somethinc.csv', index=False)

# time.sleep(3)
# soup = BeautifulSoup(driver.page_source, "html.parser")
# # print(soup)

# containers = soup.findAll('article', attrs = {'class':'css-ccpe8t'})
# print(len(containers))
# print(containers)