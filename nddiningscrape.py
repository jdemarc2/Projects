from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Launch a web browser
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# Load the webpage
url = "https://netnutrition.cbord.com/nn-prod/ND"
driver.get(url)

# Find the link element for South Dining Hall
link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="cbo_nn_unitNameLink" and contains(text(), "North Dining Hall")]')))
print(link.get_attribute("outerHTML"))  # Print the HTML of the link element
link.click()

# Wait for the page to fully load after clicking the South Dining Hall link
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//tr[@class="cbo_nn_unitsAlternateRow"]')))

# Define the expected date format in the HTML
expected_date_format = '%A, %B %d, %Y'

# Get the current date
current_date = time.strftime(expected_date_format)

# Click on the Dinner menu link for the current date
dinner_menu_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//td[contains(text(), "{current_date}")]/ancestor::tr//a[contains(@class, "cbo_nn_menuLink") and contains(text(), "Dinner")]')))
dinner_menu_link.click()

# Wait for the menu items to load
time.sleep(5)

# Find all the items between "Homestyle" and "Soup"
items = driver.find_elements(By.XPATH, '//tr[.//td[contains(.,"Homestyle")]]/following-sibling::tr[.//td[contains(.,"Soup")]][1]/preceding-sibling::tr[not(.//td[contains(.,"Soup")])]')
item_list = []

# Define a list to store item dictionaries
for item in items:
    item_dict = {}
    item_text = item.text.split("\n")
    if len(item_text) >= 2:  # Check if item_text has at least two elements
        item_dict['Item Name'] = item_text[0]
        
        # Click on the food item to view its nutritional information
        item.click()
        
        # Wait for the nutritional information to load
        time.sleep(2)

        calories = driver.find_element(By.XPATH, '//td[@class="cbo_nn_LabelDetail" and contains(., "Calories")]').text
        item_dict['Calories'] = calories

        # Extract the calorie information for the food item
        calories_fat = driver.find_element(By.XPATH, '//td[contains(text(),"Calories")]').text
        item_dict['Calories From Fat'] = calories_fat

        # Append the item dictionary to the list
        item_list.append(item_dict)

# Serialize the list of dictionaries to JSON format
json_data = json.dumps(item_list, indent=4)

# Write the JSON data to a file
with open("output.json", "w") as file:
    file.write(json_data)

# Close the browser
driver.quit()