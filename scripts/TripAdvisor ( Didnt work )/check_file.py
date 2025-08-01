# This script will help us see the start of the HTML file.

html_file_to_read = "tripadvisor_uc.html"

print(f"--- Checking the first 500 characters of {html_file_to_read} ---")
try:
    with open(html_file_to_read, "r", encoding="utf-8") as f:
        # Read only the first 500 characters
        content_preview = f.read(500)
        print("\nSTART OF FILE CONTENT:\n")
        print(content_preview)
        print("\n\nEND OF FILE CONTENT PREVIEW\n")

except FileNotFoundError:
    print(f"Error: The file '{html_file_to_read}' was not found.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

print("--- End of check ---")