from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Path to the ChromeDriver executable
chromedriver_path = r'path_to_your_ChromeDriver.exe'  # Change this to the actual path

# Your login credentials
email = "xxxxx@xxxx.com"  # Replace with your actual email
password = "XXXXXXXXXXX"  # Replace with your actual password

# Initialize the WebDriver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage
driver.get('https://www.notarygadget.com/UserLogin')  # replace with your actual URL

# Allow some time for the page to load
time.sleep(5)

# Instantiate the WebDriverWait object
wait = WebDriverWait(driver, 10)

try:
    # Debug information
    print("Trying to find the email field...")
    
    # Locate the email field
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'txtLoginID')))
    
    print("Email field found. Trying to find the password field...")
    
    # Locate the password field
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'txtPassword')))
    
    print("Password field found. Trying to find the login button...")
    
    # Locate the login button using the div class
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ButtonDarkGray')))
    
    print("Login button found. Trying to log in...")

    # Enter login credentials and submit the form
    email_field.send_keys(email)
    password_field.send_keys(password)
    login_button.click()

    # Allow some time for the login process
    time.sleep(10)

    # Print the current URL after login
    current_url = driver.current_url
    print(f"Current URL after login: {current_url}")

    # Verify we are on the correct page
    if "Signings" in current_url:
        print("Navigated to the Signings page.")
    else:
        print("Failed to navigate to the Signings page.")
        driver.quit()
        exit()

    # Allow some time for the page to load
    time.sleep(5)

    # Iterate over the table rows
    rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'trSigning')]")
    print(f"Found {len(rows)} rows to process.")

    for index, row in enumerate(rows):
        print(f"Processing row {index + 1}...")
        try:
            # Re-find the row element to avoid stale element reference
            rows = driver.find_elements(By.XPATH, "//tr[contains(@id, 'trSigning')]")
            row = rows[index]
            
            # Click on the notarial fees icon (second icon)
            fees_icon = row.find_element(By.XPATH, ".//img[@alt='Notarial fees not entered']")
            fees_icon.click()
            print("Found and clicked the notarial fees icon.")
            time.sleep(2)  # Wait for the new window to open

            # Switch to the frame if it opens in a frame
            try:
                driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
                print("Switched to the frame.")
            except:
                print("No frame found.")
            
            # Generate a random value between 3 and 8
            random_value = random.randint(2, 8) # Here just input 2 numbers the app will generate a random # between those # 
            print(f"Generated random value: {random_value}")

            # Locate the input field for notarial acts
            fees_input = driver.find_element(By.ID, 'txtNotarialActs1')  # Corrected the ID
            fees_input.send_keys(str(random_value))  # Send the random value
            print("Entered the random value into the input field.")

            # Locate and click the save button (div with class 'ButtonDarkGray')
            save_button = driver.find_element(By.CLASS_NAME, 'ButtonDarkGray')
            save_button.click()
            print("Clicked the save button.")
            time.sleep(2)  # Wait for the save action to complete

            # Switch back to the main content if you switched earlier
            driver.switch_to.default_content()
            print("Switched back to the main content.")

            # Wait a little before processing the next row
            time.sleep(2)
        
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")
            continue  # Continue with the next row

except Exception as e:
    print(f"Error during login or navigation: {e}")

# Close the driver
driver.quit()