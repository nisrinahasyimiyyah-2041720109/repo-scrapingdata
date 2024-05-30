import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://www.tokopedia.com/avoskinofficial/review'
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
driver.get(url)


try:
    # Tunggu beberapa detik agar halaman selesai dimuat
    time.sleep(5)

    # Temukan tombol dropdown
    dropdown_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='reviewSorting']")))

    # Klik tombol dropdown untuk membuka opsi
    dropdown_button.click()

    # Tunggu beberapa detik agar opsi dropdown muncul
    time.sleep(2)

    # Temukan opsi "Rating Terendah" dan klik
    rating_terendah_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'css-d2qf6r e83okfj5')]//p[text()='Rating Terendah']")))
    rating_terendah_option.click()
    time.sleep(5)
    
except Exception as e:
    print(f"Error while selecting dropdown option: {e}")


data = []
username = []
ratings = []  # Change the variable name to 'ratings' to avoid confusion
products = []
date = []
            
page_number = 1
while page_number <= 50:
    try:
        # Click 'Selengkapnya' button and wait for the review to expand
        selengkapnya_buttons = driver.find_elements(By.CSS_SELECTOR, "button.css-89c2tx")
        
        for selengkapnya_button in selengkapnya_buttons:
            selengkapnya_button.click()
            time.sleep(2)  # Adjust this sleep time based on the page loading time

        # Now scrape the data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})

        for container in containers:
            review = container.find('span', attrs={'data-testid': 'lblItemUlasan'})
            username2 = container.find('span', attrs={'class': 'name'})
            rating_element = container.find('div', attrs={'data-testid': 'icnStarRating'})
            product_element = container.find('p', attrs={'data-unify': 'Typography'})
            date_element = container.find('p', attrs={'class': 'css-1dfgmtm-unf-heading e1qvo2ff8'})

            # Convert date_element.text to the desired format
            if "Hari ini" in date_element.text:
                date_text = time.strftime("%Y-%m-%d")
            elif "1 hari lalu" in date_element.text:
                yesterday1 = datetime.now() - timedelta(days=1)
                date_text = yesterday1.strftime("%Y-%m-%d")
            elif "2 hari lalu" in date_element.text:
                yesterday2 = datetime.now() - timedelta(days=2)
                date_text = yesterday2.strftime("%Y-%m-%d")
            elif "3 hari lalu" in date_element.text:
                yesterday3 = datetime.now() - timedelta(days=3)
                date_text = yesterday3.strftime("%Y-%m-%d")
            elif "4 hari lalu" in date_element.text:
                yesterday4 = datetime.now() - timedelta(days=4)
                date_text = yesterday4.strftime("%Y-%m-%d")
            elif "5 hari lalu" in date_element.text:
                yesterday5 = datetime.now() - timedelta(days=5)
                date_text = yesterday5.strftime("%Y-%m-%d")
            elif "6 hari lalu" in date_element.text:
                yesterday6 = datetime.now() - timedelta(days=6)
                date_text = yesterday6.strftime("%Y-%m-%d")
            elif "1 minggu lalu" in date_element.text:
                minggu1 = datetime.now() - timedelta(days=7)
                date_text = minggu1.strftime("%Y-%m-%d")
            elif "3 minggu lalu" in date_element.text:
                minggu3 = datetime.now() - timedelta(days=21)
                date_text = minggu3.strftime("%Y-%m-%d")
            elif "4 minggu lalu" in date_element.text:
                minggu4 = datetime.now() - timedelta(days=28)
                date_text = minggu4.strftime("%Y-%m-%d")
            elif "1 bulan lalu" in date_element.text:
                bulan1 = datetime.now() - timedelta(days=30)
                date_text = bulan1.strftime("%Y-%m-%d")
            else:
                date_text = date_element.text  # Use the original date if no matching condition

            if review:
                data.append({'Review': review.text})
                username.append(username2.text)
                rating = rating_element['aria-label']
                ratings.append(rating)
                products.append(product_element.text)
                date.append(date_text)
            else:
                data.append({'Review': 'No review found'})
                username.append(username2.text)
                rating = rating_element['aria-label']
                ratings.append(rating)
                products.append(product_element.text)
                date.append(date_text)

        # Move this outside the inner loop to avoid clicking the button multiple times
        time.sleep(2)
        next_page_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Laman berikutnya']")
        if "disabled" in next_page_button.get_attribute("class"):
            print("No more pages available.")
            break
        next_page_button.click()
        time.sleep(3)
        page_number += 1
        print(f"Scraped data from page {page_number}")
    except Exception as e:
        print(f"Error in iteration {page_number}: {e}")

df = pd.DataFrame(data, columns=['Review'])
df['Product'] = products
df['Rating'] = ratings  # Add the 'Rating' column
df['Username'] = username
df['Date'] = date
print(df)

driver.close()

# Now, you can save the DataFrame to a CSV file
df.to_csv('scraping_avoskin-neg.csv', index=False)
