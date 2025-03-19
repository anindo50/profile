# import pyautogui
# import keyboard
# import time
# import os

# # Create a folder to save screenshots
# def take_ss():
#     screenshot_dir = "screenshots"
#     if not os.path.exists(screenshot_dir):
#         os.makedirs(screenshot_dir)

#     def take_screenshot():
#         timestamp = time.strftime("%Y%m%d-%H%M%S")
#         screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        
#         # Capture and save screenshot in HD quality
#         screenshot = pyautogui.screenshot()
#         screenshot.save(screenshot_path)
        
#         print(f"Screenshot saved: {screenshot_path}")

#     # Listen for Ctrl + G shortcut
#     keyboard.add_hotkey("ctrl+g", take_screenshot)

#     print("Press 'Ctrl + G' to take a screenshot...")
#     keyboard.wait("esc")  # Keep the script running until 'Esc' is pressed
# Install the necessary libraries
# pip install newsapi-python transformers requests

# Install necessary libraries
# pip install beautifulsoup4 requests transformers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options for headless browsing and User-Agent header
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run the browser in headless mode
    chrome_options.add_argument('--no-sandbox')  # Required for running in certain environments (e.g., Docker)
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage
    chrome_options.add_argument('start-maximized')  # Start browser in maximized mode
    chrome_options.add_argument('disable-infobars')  # Disable the infobar
    chrome_options.add_argument('--disable-extensions')  # Disable extensions
    chrome_options.add_argument('--disable-gpu')  # Disable GPU (needed for headless mode)

    # Set the custom User-Agent
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Create the WebDriver with the above options
    driver_path = ChromeDriverManager()
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Fetch the latest news articles by scraping
def fetch_news():
    url = 'https://www.dhakatribune.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    driver = create_driver()
    # response = requests.get(url, headers=headers)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    headlines = soup.find_all('a', class_='link_overlay')
    news_dic = {}  # Initialize the dictionary to store article details
    
    driver = create_driver()  # Open the browser only once

    for h in headlines[:7]:
        article_url = h.get('href').strip()
        article_title = h.get('title')
        if article_url.startswith("//"):
            article_url = article_url.replace("//","https://")

            if not article_url or not article_title:  # Skip if URL or title is missing
                continue

            print(f"Fetching article: {article_title} ({article_url})")

            driver.get(article_url)  # Open article page
            time.sleep(3)  # Allow the page to load

            article_soup = BeautifulSoup(driver.page_source, 'html.parser')
            container = article_soup.find("div", class_="content_detail_content_inner")

            if not container:  # If no content is found, skip this article
                print(f"Warning: No content found for {article_title}")
                continue

            news_list = []
            all_p = container.find_all("p")

            for p in all_p:
                text = p.text.strip()
                if text:
                    news_list.append(text)
                    print(text)
            
            news_dic[article_title] = news_list  # Store article text

    driver.quit()  # Close the browser after all articles are processed
    return news_dic


# Example of using the fetcher
fetch_news()



