import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://www.tokopedia.com/youmakeups/review'
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
driver.get(url)

data = []

for i in range(1, 11):
    # Click 'Selengkapnya' button and wait for the review to expand
    try:
        selengkapnya_buttons = driver.find_elements(By.CSS_SELECTOR, "button.css-89c2tx")
        
        for selengkapnya_button in selengkapnya_buttons:
            selengkapnya_button.click()
            time.sleep(2)  # Adjust this sleep time based on the page loading time

        # Now scrape the data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})

        for container in containers:
            review = container.find('span', attrs={'data-testid': 'lblItemUlasan'})

            if review:
                data.append({review.text})
            else:
                data.append({'No review found'})

        # Move this outside the inner loop to avoid clicking the button multiple times
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[aria-label='Laman berikutnya']").click()
        time.sleep(3)
    except Exception as e:
        print(f"Error in iteration {i}: {e}")

df = pd.DataFrame(data)
print(df)

driver.close()

# Now, you can save the DataFrame to a CSV file
df.to_csv('scraping_you.csv', index=False)
