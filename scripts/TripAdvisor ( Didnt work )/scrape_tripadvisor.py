from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time

# --- Options for Brave Browser ---
options = uc.ChromeOptions()
options.binary_location = "C:/Users/Ovindu/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"

# The URL we want to scrape
url = "https://www.tripadvisor.com/Attraction_Review-g297896-d317135-Reviews-Galle_Fort-Galle_Galle_District_Southern_Province.html"

# --- Main Script with an Intelligent Wait ---
print("Initializing undetected-chromedriver...")
driver = uc.Chrome(options=options)
print("WebDriver is ready.")

try:
    print(f"Navigating to: {url}")
    driver.get(url)

    # --- THIS IS THE CRITICAL CHANGE ---
    # We will now wait up to 30 seconds for the reviews to appear before saving.
    # We are waiting for the element from your screenshot to be visible.
    print("Waiting for review content to load...")
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "location-review-review-list-parts-ExpandableReview__reviewText--gOm_F")))
    print("Review content has loaded!")

    # A small extra wait just to be safe
    time.sleep(2)

    print("Saving the final page source to tripadvisor_final.html")
    with open("tripadvisor_final.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("\nSuccess! Check for the 'tripadvisor_final.html' file.")

finally:
    print("Done. Closing the browser.")
    driver.quit()