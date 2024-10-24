import os
from playwright.sync_api import sync_playwright

def send_photos_via_whatsapp(contact_name, folder_name, file_names):
    with sync_playwright() as p:
        # Connect to the existing Chrome instance using the debugging port
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # Get the list of pages (tabs) in the browser
        pages = browser.contexts[0].pages
        page = pages[0]  # Use the first tab or choose based on your scenario

        # Navigate to WhatsApp Web (or use an existing WhatsApp Web tab)
        page.goto("https://web.whatsapp.com")

        # Search for the contact
        search_box = page.locator('div[contenteditable="true"]')
        search_box.click()
        search_box.fill(contact_name)

        # Wait for the search results to load and click on the contact
        page.locator(f"span[title='{contact_name}']").click()

        # Send each file
        for file_name in file_names:
            file_path = os.path.join(folder_name, file_name)

            if os.path.isfile(file_path):
                # Click on the attach button (paperclip icon)
                attach_btn = page.locator('span[data-icon="plus"]')
                attach_btn.click()

                # Upload the file
                file_input = page.locator("li").filter(has_text="Photos & videos").locator('input[type="file"]')
                file_input.set_input_files(file_path)

                # Wait for the file to be ready and send it
                page.locator('span[data-icon="send"]').click()

                print(f"Sent {file_name} to {contact_name}")

        # You can close the browser if needed, or leave it open
        browser.close()

# Example usage:
folder = '/Users/tirthyakamaldasgupta/Downloads/Official documents'  # Replace with your folder path
files = ['1706976767431.jpeg']  # Replace with your file names
recipient = 'TIRTHYA KAMAL DASGUPTA'  # Replace with the WhatsApp contact's name

send_photos_via_whatsapp(recipient, folder, files)
