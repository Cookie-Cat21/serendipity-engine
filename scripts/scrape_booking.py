from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# --- The confirmed URL you found ---
url = "https://www.booking.com/hotel/lk/shangri-la-colombo.html"

# --- Setup Brave Browser (Visible Mode) ---
options = Options()
options.binary_location = "C:/Users/Ovindu/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

print("Initializing WebDriver for Booking.com...")
driver = webdriver.Chrome(options=options)

try:
    print(f"Navigating to: {url}")
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # --- Step 1: Handle Cookie Banner (if it appears) ---
    try:
        print("Looking for cookie banner...")
        accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_button.click()
        print("Cookie banner accepted.")
    except Exception:
        print("Cookie banner not found or already accepted. Continuing...")

    # --- Step 2: Wait for a STABLE element (the hotel title) ---
    print("Waiting for the main page content to load...")
    # This class name is for the 'Shangri-La Colombo' H2 title
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "d2fee87262")))
    print("Main page content loaded.")

    # --- Step 3: Add a HARD PAUSE for dynamic content (reviews) ---
    print("Pausing for 5 seconds to let reviews load...")
    time.sleep(5)

    # --- Step 4: Parse and Save ---
    print("Now parsing the page source...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Use the data-testid we found from your screenshot
    review_spans = soup.find_all('span', attrs={'data-testid': 'review-text'})
    print(f"\nFound {len(review_spans)} reviews on the page.")

    if review_spans:
        reviews_list = []
        for span in review_spans:
            # Check for empty spans and ignore them
            if span.text.strip():
                reviews_list.append(span.text.strip())

        df = pd.DataFrame({'review_text': reviews_list})
        output_path = os.path.join("data", "booking_reviews.csv")
        df.to_csv(output_path, index=False)
        print(f"\nSuccessfully extracted {len(reviews_list)} reviews to '{output_path}'")
        print("Data collection complete!")
    else:
        print("\nCould not find any review text. The page structure may have changed.")

finally:
    driver.quit()
    print("Browser closed.")