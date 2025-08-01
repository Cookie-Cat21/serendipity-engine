from bs4 import BeautifulSoup
import pandas as pd
import os

# --- Configuration ---
html_file_to_read = "tripadvisor_uc.html"
output_csv_file = "reviews.csv"
data_folder = "data"

print(f"Reading the saved file: {html_file_to_read}")

try:
    with open(html_file_to_read, "r", encoding="utf-8") as f:
        html_content = f.read()
except FileNotFoundError:
    print(f"Error: The file '{html_file_to_read}' was not found.")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

print("\n--- Finding all review containers ---")

# 1. Find all the main 'div' containers for each review.
review_containers = soup.find_all('div', class_='mxEhR D y G- Za f e u LEMGe')

# --- Data Extraction and Storage ---
if review_containers:
    print(f"Found {len(review_containers)} review containers. Now extracting all text from them...")
    reviews_list = []
    
    # 2. Loop through each container.
    for container in review_containers:
        # 3. THE KEY CHANGE: Get ALL text from inside the container.
        # This is simpler and more reliable.
        review_text = container.text.strip()
        
        if review_text:
            reviews_list.append(review_text)

    print(f"\nSuccessfully extracted {len(reviews_list)} text blocks.")

    # Create and save the data to a CSV file
    df = pd.DataFrame({'review_text': reviews_list})
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    output_path = os.path.join(data_folder, output_csv_file)
    df.to_csv(output_path, index=False)
    
    print(f"Data saved successfully to '{output_path}'")

else:
    print("Could not find any review containers.")