import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Configure Chrome to ignore SSL certificate errors
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')

# Disable logging of SSL certificate errors
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

# Create a Chrome WebDriver with custom options
driver = webdriver.Chrome(options=chrome_options)

url = 'https://shopee.co.id/-Tasya-Farasya-Approved-SKINTIFIC-5X-Ceramide-Skin-Barrier-Moisturize-Gel-30g-Moisturizer-Cream-Pemutih-Wajah-Day-Cream-Night-Cream-Pelembab-Wajah-i.457706720.11242593437?sp_atk=cecb80f3-af3a-4373-89e1-a70f1d2f9f5a&xptdk=cecb80f3-af3a-4373-89e1-a70f1d2f9f5a'
path = 'C:/Users/NISRINA/chromedriver-win64/chromedriver.exe'

# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')

# chrome_options.add_argument('disable-notifications')
# chrome_options.add_argument('--disable-infobars')

# driver = webdriver.Chrome(options=chrome_options)
# Create instance of ChromeOptions Class
# handling_ssl = webdriver.ChromeOptions()

# # Using the accept insecure cert method with True as parameter to accept the untrusted certificate
# handling_ssl.accept_insecure_certs = True

# # Creating instance of Chrome driver by passing reference of ChromeOptions object
# driver = webdriver.Chrome(options=handling_ssl)
driver.get(url)

# Close the WebDriver
driver.quit()

# html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
# soup = BeautifulSoup(html, "html.parser")
soup = BeautifulSoup(driver.page_source, "html.parser")

review = soup.find_all('div', class_='Rk6V+3')
print(len(review))
print(review)