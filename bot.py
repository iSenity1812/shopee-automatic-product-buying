# This bot is just a demo version made by Hasami Nagisa - old name: Asaki
# Contact:
# Discord: isepipi8239
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import json
import os
from colored import Fore, Back, Style
import time
import datetime
from logWriter import delete_all_log_files, logger


# LOG CONTROLLER
# directory_path = '.\logs'
# logger.info("Dit me may")
# delete_all_log_files(directory_path)
"""
Userdata -- accounts.json
    [+] Check if file exist & create file
    [+] Input
    [+] Save
    [+] No reset when run programme
    [+] Import
    [+] Remove account
        [+] Choose account 
        [+] Remove username & password

[+] Find all options (button to choose a type of product)
    [+] Convert it to a function that can control with input
        [++] Find all button --> eg: button[4] --> 4 input options
""" 
##################################################################

"""TODO: make a function to check a current website
        If expected url = func(get_cur_ul) -> verify page found -> set time for verify
        else skip

""" 

########################################################################
class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password
        }

def XPATH_Present(XPATH):       # Function: Search for the xpath element in the current website in secs : if the function not found the element -> refresh page
    try:
        XPATH_present = EC.presence_of_element_located((By.XPATH, XPATH))
        WebDriverWait(driver, 4).until(XPATH_present)
        return 1
    except TimeoutException:
        print("Timed out")
        
        return 0

def elementPresent(className):
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, className))
        WebDriverWait(driver, 4).until(element_present)
        return 1
    except TimeoutException:
        print("Timed out waiting for page to load / Can not find element... Reloading...")

        return 0


# Reset some variable when the program restart during executing

# def initialize_variables():
#     product_url = ""
#     year = 0
#     month = 0
#     day = 0
#     hour = 0
#     minute = 0
#     second = 0

#     return 






def save_accounts(accounts):
    """Saves the list of accounts to a JSON file.

    Args:
        accounts: A list of Account objects.
    """

    with open("accounts.json", "w") as f:
        json.dump([account.to_dict() for account in accounts], f, indent=4)

def create_accounts_file():
    with open("accounts.json", "w") as f:
        json.dump([], f, indent=4)

def is_accounts_file_writable():
    """Checks if the accounts.json file is writable.

    Returns:
        True if the accounts.json file is writable, False otherwise.
    """

    try:
        with open("accounts.json", "r") as f:
            json.load(f)
    except FileNotFoundError:
        return True
    except json.decoder.JSONDecodeError:
        return True
    except PermissionError:
        return False
    return True

def get_accounts():
    """Get accounts from JSON file.

    Returns:
        A list of Account objects.
    """

    try:
        with open("accounts.json", "r") as f:
            account_data = json.load(f)
    except FileNotFoundError:   
        account_data = []

    accounts = []
    for account_data in account_data:
        accounts.append(Account(account_data["username"], account_data["password"]))
    return accounts

def add_account(username, password):
    """Adds a new account to the JSON file.

    Args:
        username: The username of the new account.
        password: The password of the new account.
    """
    account_json_file = "accounts.json"

    if not is_accounts_file_writable():
        print("File is not writable")
        return
    
    accounts = get_accounts()

    if check_username_exists(username, account_json_file):
        print("Username already exists.")
        return

    accounts.append(Account(username, password))
    save_accounts(accounts)

def check_username_exists(username, account_json_file):
    """Checks if the username exists in the specified JSON file.

    Args:
        username: The username to check.
        account_json_file: The path to the JSON file containing the user data.

    Returns:
        True if the username exists, False otherwise.
    """

    account_json_file = "accounts.json"
    with open(account_json_file, "r") as f:
        account_data = json.load(f)
    
    for account in account_data:
        if account["username"] == username:
            return True
    return False

def prevent_duplicate_username(username, account_json_file):
    """Prevents the user from adding a duplicate username to the JSON file.

    Args:
        username: The username to check.
        account_json_file: The path to the JSON file containing the user data.
    """

    while check_username_exists(username, account_json_file):
        print("Username already exists. Please enter a different username.")
        username = input("Enter a different username: ")


def import_account(username):
    """Imports an account from the JSON file.

    Args:
        username: The username of the account to import.

    Returns:
        An Account object, or None if the account is not found.
    """

    accounts = get_accounts()
    for account in accounts:
        if account.username == username:
            return account
    return None

def delete_account(username):
    """Deletes an account from the JSON file.

    Args:
        username: The username of the account to delete.
    """

    accounts = get_accounts()
    accounts = [account for account in accounts if account.username != username]
    save_accounts(accounts)

def edit_account(username, new_username, new_password):
    """Edits an account in the JSON file.

    Args:
        username: The username of the account to edit.
        new_username: The new username for the account.
        new_password: The new password for the account.
    """

    accounts = get_accounts()
    for account in accounts:
        if account.username == username:
            account.username = new_username
            account.password = new_password
            break
    save_accounts(accounts)


def get_username_from_json_acount(account_json_file, account_index):
    with open (account_json_file, "r") as f:
        account_data = json.load(f)
    
    if int(account_index) >= len(account_data) or int(account_index) < 0:
        raise IndexError("Account index out of range")
    username = account_data[int(account_index)]["username"]

    return  username


def login_with_json_account(website_url, account_json_file, account_index):

    with open(account_json_file, "r") as f:
        account_data = json.load(f)
    
    username = account_data[int(account_index)]["username"]
    password = account_data[int(account_index)]["password"]


    driver.get(website_url)
    driver.maximize_window()

    # Located username_field & password_field

    username_field_address = '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div[2]/form/div[1]/div[1]/input'
    password_field_address = '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div[2]/form/div[2]/div[1]/input'

    username_field = driver.find_element(by=By.XPATH, value=username_field_address)
    password_field = driver.find_element(by=By.XPATH, value=password_field_address)

    #Enter username & password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # driver.implicitly_wait(2)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "wyhvVD._1EApiB.hq6WM5.L-VL8Q.cepDQ1._7w24N1"))).click()
    login_button = driver.find_element(by=By.CLASS_NAME, value='wyhvVD._1EApiB.hq6WM5.L-VL8Q.cepDQ1._7w24N1')
    login_button.click()

    # Wait for the login to complete

    #Check if the login was successful
    if driver.find_element(by=By.XPATH, value=username_field_address).text == account_data[int(account_index)]["username"]:
        return True
    else:
        return False
        

def view_all_suernames_in_json_file(account_json_file):
    with open(account_json_file, "r") as f:
        account_data = json.load(f)
    
    usernames = []
    for account in account_data:
        usernames.append(account["username"])
    
    return usernames


def get_information_about_product():
    """
    Get infomation about product
        - Title, Price, Rate, Store/Valid quantity, Price
        - clasify
            - Location of Types / Options
    """
    global xpath_choice
    print("---------------------------------")
    productTitle = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[1]/span')
    productEvaluate = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[2]/button[2]/div[1]')
    productSold = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[2]/div/div[1]')
    productStore = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/div/div/section[2]/div/div[2]')
    productPrice = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[3]/div/div/section/div/div/div')

    #//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/div/div/section[1]/div/button[1]
    # //*[@id="main"]/div/div[2]/div[1]/div[1]/div/div[2]/section[1]/section[2]/div/div[4]/div/div/div/section[1]/div/button[1]
    container_element = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/div/div/section[1]/div')
    button_elements = container_element.find_elements(by=By.TAG_NAME, value='button')
    
    """Count a button in //*[@id="main"]/div/div[2]/div[1]/div[1]/div/div[2]/section[1]/section[2]/div/div[4]/div/div/div/section[1]/div/"""
    xpath = '//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/div/div/section[1]/div'
    xpath_list = [f"{xpath}/button[{i}]" for i in range(1, len(button_elements) + 1)]

    """Print a list of buttons"""
    # print(xpath_list)
    print(f"{Fore.cyan}[+] Buttons founded:{Style.reset} {len(xpath_list)}")

    for i in range(len(xpath_list)):
        status = driver.find_element(by=By.XPATH, value=xpath_list[i]).get_attribute('aria-disabled')
    
        if status == 'true':
            print(f"{Fore.blue}[{i+1}] Classify: {Style.reset} {button_elements[i].text} | {Fore.blue}[+] Status: {Style.reset} {Fore.red}Not Available{Style.reset}")
        else:
            print(f"{Fore.blue}[{i+1}] Clasify: {Style.reset} {button_elements[i].text} | {Fore.blue}[+] Status: {Style.reset} {Fore.green}Available{Style.reset}")

    # Get status of product (Available / Not available)
    # print xpath_list attribute 
        # If aria-disabled = true > Not Available | else > Available

    # for xpath in xpath_list:    
    #     print(f"{Fore.yellow}[+]{Style.reset} {xpath}")
    
    # print(f"{Fore.cyan}[+] Select a button: {Style.reset}")
    # for i in range(len(xpath_list)):
    #     print(f"{Fore.red}[{i+1}]: {Style.reset} {xpath_list[i]}")

    
    # Get classify choice 
    while True:
        try:
            choice = int(input(f"{Fore.blue}[?] Classify Choice: {Style.reset}"))
            if choice in range(1, len(xpath_list) + 1):
                break
            else: print(f"{Fore.red}[!] Please enter a number between 1 and {len(xpath_list)}!{Style.reset}")
        except ValueError:
            print(f"{Fore.red}[!] Please enter a number!{Style.reset}")

    print("---------------------------------------------------")

    xpath_choice = xpath_list[choice - 1]
    print(f"{Fore.green}[+] Location: {Style.reset}", xpath_choice)

    # Classify
    productClassify = driver.find_element(by=By.XPATH, value=xpath_choice)
    global classifyText
    classifyText = productClassify.text

    print(""""""
    f"{Fore.green}[+] Product Title:{Style.reset} {productTitle.text}\n"
    f"{Fore.green}[+] Product Evaluate:{Style.reset} {productEvaluate.text}\n"
    f"{Fore.green}[+] Product Sold:{Style.reset} {productSold.text}\n"
    f"{Fore.green}[+] Product Store:{Style.reset} {productStore.text}\n"
    f"{Fore.green}[+] Product Price:{Style.reset} {productPrice.text}\n"
    f"{Fore.green}[+] Product Classify:{Style.reset} {productClassify.text}\n"
    """""")

    print("---------------------------------------------------")



# Main page
""" 
Wait elements to appear > find > click (Option) > click 'Buy' button
    If product was sold out > refresh page
"""
"""
    Plan in future
        - If refresh page > n attempt (n = const) > return get_infomation_about_product > change other classify
"""



def stage1_Mainpage():
    global attempt
    # Wait elements to appear
    while True:
        if not XPATH_Present(xpath_choice):
            print(f"{Fore.red}[-]{Style.reset} Element not found")
            driver.refresh()
        else: break

    # Condition if product was sold out
    
    """
    If aria-disabled = false > existed | else > not existed
        - Not existed > refresh | attemp-- > attempt = 0 > get_infomation_about_product
    """
    i = 0
    while True:
        stage1_ariaDisabled = driver.find_element(by=By.XPATH, value=xpath_choice).get_attribute('aria-disabled')
        if stage1_ariaDisabled == "false":
            print(f"{Fore.green}[+] Product is available{Style.reset}")
            break
        elif stage1_ariaDisabled == "true":
            print(f"{Fore.red}[-] Product was sold out!{Style.reset}")
            for i in range(0, attempt):
                i += 1

                driver.refresh()
                print(f"{Fore.blue}[+]{Style.reset} Attempt: {Fore.green}{i}{Style.reset}")

                # Re-check
                while True:
                    if not XPATH_Present(xpath_choice):
                        driver.refresh()
                        print(f"{Fore.red}[!] Element not found{Style.reset}")
                    else: break
                
                stage1_ariaDisabled_reCheck = driver.find_element(by=By.XPATH, value=xpath_choice).get_attribute('aria-disabled')
                if stage1_ariaDisabled_reCheck == "false":
                    print(f"{Fore.green}[+] Product is available{Style.reset}")
                    break
                elif stage1_ariaDisabled == "true":
                    print(f"{Fore.red}[-] Product was sold out!{Style.reset}")
                    continue
            
            # NOTE: UPDATE LATER
            if i == attempt:
                print(f"{Fore.red}[!] Out of range! The program will shutdown{Style.reset}")
                exit()
                
    # Get button-selected status
    stage1_selectedButton = 'hUWqqt n-ioz2 _69cHHm'
    stage1_notSelectedButton = 'hUWqqt _69cHHm'

    while True:
        stage1_getButtonStatus = driver.find_element(by=By.XPATH, value=xpath_choice).get_attribute('class')
        
        if stage1_getButtonStatus == stage1_selectedButton:
            print(f"{Fore.green}[+] Button is selected{Style.reset}")
            break
        elif stage1_getButtonStatus == stage1_notSelectedButton:
            print(f"{Fore.red}[-] Button is not selected{Style.reset}")
            driver.find_element(by=By.XPATH, value=xpath_choice).click()
            print("Rechecking....")



            # Find element > click (Options > Add to cart)
    var_stage1_buyClass = 'btn.btn-solid-primary.btn--l.iFo-rx'
    # driver.find_element(by=By.XPATH, value=xpath_choice).click()  #Opption
    driver.find_element(by=By.CLASS_NAME, value=var_stage1_buyClass).click()    # Add to cart


"""Change quantity > Click to other element (update quantity & price) > Buy"""
def stage2_Carting():

    # Get Buy now XPATH
    var_stage2_buyButton_location = 'TTXpRG'

    # Wait elements to appear

    while True:
        if not elementPresent(var_stage2_buyButton_location): 
            driver.refresh()
            print(f"{Fore.red}[-] Element not found.{Style.reset}")
        else: break


    # Check checkbox-status     alternative value: aria-checked: true/false
    var_stage2_checkBox_location = '//*[@id="main"]/div/div[2]/div/div/div[3]/main/section[1]/section/div[1]/div/div[1]/label/input'
    var_stage2_checkBox_status = driver.find_element(by=By.XPATH, value=var_stage2_checkBox_location).get_attribute('aria-checked')
    if var_stage2_checkBox_status == 'true': # checkbox = on
        print(f"{Fore.green}[+] Box has been checked!{Style.reset}")
    elif var_stage2_checkBox_status == 'false':
        var_stage2_checkBox_status.click()

    # Change quantity
        # alternative elements: aria-valuenow; value
    var_stage2_quantity_box = '//*[@id="main"]/div/div[2]/div/div/div[3]/main/section[1]/section/div[1]/div/div[5]/div/input'
    # Get value from quantity box
    find_ariaValuenow = driver.find_element(by=By.XPATH, value=var_stage2_quantity_box).get_attribute("aria-valuenow")
    print_ariaValuenow = f"{Fore.yellow}[#] Update value: {find_ariaValuenow}{Style.reset}"
    print(print_ariaValuenow)

    # Check quantity
    if find_ariaValuenow == str(quantity):
        print(f"{Fore.green}[+] Value is matched the input{Style.reset}")
    else: 
        print(f"{Fore.red}[-] Value does not match the input{Style.reset}")
        driver_stage2_quantity_box = driver.find_element(by=By.XPATH, value=var_stage2_quantity_box)
        driver_stage2_quantity_box.click()
        driver_stage2_quantity_box.send_keys(Keys.CONTROL, "a")
        driver_stage2_quantity_box.send_keys(Keys.BACKSPACE)
        driver_stage2_quantity_box.send_keys(quantity)
        print(f"{Fore.green}[*] Updated quantity to {Fore.blue}{quantity} {Style.reset}")
        driver.find_element(by=By.CLASS_NAME, value="lKFOxX").click()   # Click other element to update quantity
    
    time.sleep(0.5)
    driver.find_element(by=By.CLASS_NAME, value = var_stage2_buyButton_location).click()
    print(f"{Fore.green}[>>>] Navigating to checkout page...{Style.reset}")


def stage3_Checkout():
    finishOrder = 'stardust-button.stardust-button--primary.stardust-button--large.apLZEG'
    while True:
        if not elementPresent("gQuJxM"):
            driver.refresh()
            print(f"{Fore.red}[-] Element not found{Style.reset}")
        else: break
    driver.execute_script("window.scrollTo(0, 1000)")
    if test == 0:
        driver.find_element(by=By.CLASS_NAME, value=finishOrder).click()
        print(f"{Fore.green}[+] Order successfully.{Style.reset}")
    if test == 1:
        if driver.find_element(by=By.CLASS_NAME, value=finishOrder):
            print(f"{Fore.green}[+] Order successfully. [TEST = ON]{Style.reset}")
        else: print(f"{Fore.red}ERROR{Style.reset}")
        


# Login from json --> change website url to product's url --> Countdown
def wait_for_element_present(locators):
    try:
        WebDriverWait(driver, 4).until(lambda driver: any(EC.presence_of_element_located(locator) for locator in locators))
        return 1
    except TimeoutException:
        print("Timeout!")
        return 0

    # Using
    # locator = {
    #   (By.XPAYH, "//div[@id='my-element']")
    # }

def countdown(stop):
    while True:
        difference = stop - datetime.datetime.now()
        count_hours, rem = divmod(difference.seconds, 3600)
        count_minutes, count_seconds = divmod(rem, 60)
        if difference.days == 0 and count_hours == 0 and count_minutes == 0 and count_seconds == 0:
            print(f"{Fore.blue}[+] Times up! START BUYING...{Style.reset}")
            break

        timeFormatter = '{:02d}:{:02d}:{:02d}:{:02d}'.format(difference.days, count_hours, count_minutes, count_seconds)
        print(timeFormatter, end='\r')
        time.sleep(0.00001)



def get_run_code_time(code_block):

    start_time = time.time()
    code_block()
    end_time = time.time()

    run_time = end_time - start_time

    return run_time


def my_code_block():
    stage1_Mainpage()
    stage2_Carting()
    stage3_Checkout()


def quitAndRestart():
            # Exit webpage & Run bot again (end_choice variable)
    print(""""""
    f"{Fore.blue}[+]{Style.reset} Wanna exit or reboot again \n"
    f"{Fore.blue}[1]{Style.reset} Exit \n"
    f"{Fore.blue}[2]{Style.reset} Reboot \n"
    """""")
    while True:
        end_choice = input(f"{Fore.yellow}[?]{Style.reset} Enter your choice: ")
        if end_choice == "1":

            driver.quit()
            exit()
        elif end_choice == "2":
            print("Still in dev :) ")
            exit()
        else: 
            print(f"{Fore.red}[-] Invalid input. Please try again. {Style.reset}")


def main():

    global quantity, attempt, test

    if not os.path.exists("accounts.json"):
        create_accounts_file()

    # Menu
    while True:
        print("---------------------------------")
        print(f"{Fore.green}Menu: {Style.reset}")
        print(f"{Fore.cyan} [1]{Style.reset} Add account" )
        print(f"{Fore.cyan} [2]{Style.reset} Import account")
        print(f"{Fore.cyan} [3]{Style.reset} Delete account")
        print(f"{Fore.cyan} [4]{Style.reset} Edit account")
        print(f"{Fore.cyan} [5]{Style.reset} View all account")
        print(f"{Fore.cyan} [6]{Style.reset} Buy product (Include logging & purchasing method)")
        print(f"{Fore.cyan} [7]{Style.reset} Exit")
        print("----------------------------------")

        choice = input(f"{Fore.yellow}[?] Enter your choice: {Style.reset}")

        if choice == "1":
            username = input(f"{Fore.cyan}[?]{Style.reset} Enter the username: ")
            password = input(f"{Fore.cyan}[?]{Style.reset} Enter the password: ")
            print(f"{Fore.green}[+] Account added successfully!{Style.reset}")

            add_account(username, password)
        elif choice == "2":
            username = input(f"{Fore.cyan}[?] Enter the username of the account to import: {Style.reset}")

            account = import_account(username)
            if account is not None:
                print(f"{Fore.green}[+] Account found: {Style.reset}")
                print("Username:", account.username)
                print("Password:", account.password)
            else:
                print(f"{Fore.red}[-] Account not found. {Style.reset}")
                
        elif choice == "3":
            username = input(f"{Fore.yellow}Enter the username of the account to delete: {Style.reset}")
            delete_account(username)

        elif choice == "4":
            username = input(f"{Fore.green}[+] Enter the username of the account to edit: {Style.reset}")
            new_username = input(f"{Fore.cyan}[?]{Style.reset} Enter the new username: ")
            new_password = input(f"{Fore.cyan}[?]{Style.reset} Enter the new password: ")
            edit_account(username, new_username, new_password)

        elif choice == "5":
            usernames = view_all_suernames_in_json_file(account_json_file)
            # print("Usernames: ", usernames)
            print(f"Username: {usernames}")

        elif choice == "6":
            
            # Test case
            while True:
                try:
                    test = int(input(f"{Fore.yellow}[+] Test function OFF-0 / ON-1 (Test will not order): {Style.reset}"))
                    if test == 0:
                        print(f"{Fore.blue}[!] Test{Style.reset} = {Fore.red}OFF{Style.reset}")
                        break
                    elif test == 1:
                        print(f"{Fore.blue}[!] Test {Style.reset}= {Fore.green}ON{Style.reset}")
                        break
                    else: print(f"{Fore.red}[-] Invalid input. Please enter 0 or 1{Style.reset}")
                except ValueError:
                    print(f"{Fore.red}[-] Invalid input. Please enter 0 or 1. {Style.reset}")

            # Input username index & print list of username
            while True:
                try:
                    account_index = int(input(f"{Fore.yellow}[?] Enter account index (0 -> n-1; n: number of accounts): {Style.reset}"))
                    if len(view_all_suernames_in_json_file(account_json_file)) == 1 and account_index == 0:
                        break
                    elif len(view_all_suernames_in_json_file(account_json_file)) > 1:
                        if 0 <= account_index < len(view_all_suernames_in_json_file(account_json_file)):
                            break
                        else:
                            print(f"{Fore.red}[-] Invalid input{Style.reset}")
                    else: 
                        print(f"{Fore.red}[!] Invalid input{Style.reset}")
                except ValueError:
                    print(f"{Fore.red}[-] Invalid! Input must be int{Style.reset}")

            # Get quantity
            while True:
                try:
                    quantity = int(input(f"{Fore.yellow}[?] Enter quantity (max = 3): {Style.reset}"))
                    if 0 < quantity <= 3:
                        break 
                    else:
                        print(f"{Fore.red}[-] Quantity must be between 1 and 3. {Style.reset}")
                except ValueError:
                    print(f"{Fore.red}[-]Invalid input. Quantity must be between 1 and 3. {Style.reset}")
            
            # Get refresh attempts
            while True:
                try:
                    attempt = int(input(f"{Fore.yellow}[?] Enter refresh attempts (Max = 200; Recommended: 100-150): {Style.reset}"))
                    if 0 <=  attempt < 200:
                        break
                    else:
                        print(f"{Fore.red}[-] Refresh attempts must be between 1 and 200. {Style.reset}")
                except ValueError:
                        print(f"{Fore.red}[-]Invalid input. Refresh attempts must be between 1 and 200. {Style.reset}")



            # Set a timer
            while True:
                year = input(f"{Fore.green}[?]{Style.reset} Enter the year: ")
                month = input(f"{Fore.green}[?]{Style.reset} Enter the month: ")
                day = input(f"{Fore.green}[?]{Style.reset} Enter the day: ")
                hour = input(f"{Fore.green}[?]{Style.reset} Enter the hour: ")
                minute = input(f"{Fore.green}[?]{Style.reset} Enter the minute: ")
                second = input(f"{Fore.green}[?]{Style.reset} Enter the second: ")
                try:
                    year = int(year)
                    month = int(month)
                    day = int(day)
                    hour = int(hour)
                    minute = int(minute)
                    second = int(second)    

                    if 2023 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 24 and 0 <= minute <= 60 and 0 <= second <= 60:
                        break
                    else: 
                        print(f"{Fore.red}[-] Invalid input. {Style.reset}" )
                except ValueError:
                    print(f"{Fore.red}[-] Invalid input. {Style.reset}" )
                
            print('Buying process will start at: {:02d}-{:02d}-{:02d}|{:02d}:{:02d}:{:02d}'.format(year, month, day, hour, minute, second))
            end_time = datetime.datetime(year, month, day, hour, minute, second)


            try:
                username = get_username_from_json_acount(account_json_file, account_index) 
            except IndexError: print("Account is out of range")
            else:
                print(f"{Fore.green}[+]{Style.reset} Username: ", username)
            
            login_status = login_with_json_account(website_url, account_json_file, account_index) 
            if login_status:
                print(f"{Fore.red}[-] Login failed {Style.reset}")
            else:
                print(f"{Fore.green}[+] Login successful {Style.reset}")
            # FINISHED LOGIN

            # Change url ->  product's url
                
            # ADD GET CURRENT SITE HERE
            """Clm quen mat cai url page verify cmnr :VV xai do method nay"""
            # Check url
            time.sleep(5)
            curURL = driver.current_url


            expected_url = ["https://shopee.vn/", product_url, "https://shopee.vn/?is_from_login=true"]

            time_limit = 100
            if curURL != expected_url[0] and curURL != expected_url[1] and curURL != expected_url[2]:
                print(f"{Fore.red}[-] Found verification site! Please do your verification. You have {time_limit} secs to do that{Style.reset}")
                # Loop check verify every 10s
                max_count = time_limit / 10
                for i in range(max_count):
                    i -= 1
                    if i == 0: 
                        break
                    else:
                        time.sleep(time_limit)
                        print(f"Checking verification....")
                        if driver.current_url == expected_url[0] or driver.current_url == expected_url[1] or driver.current_url == expected_url[2]:
                            print(f"{Fore.green} [+] You done your verification. {Style.reset}")
                            break
                        else:
                            print(f"{Fore.red} [!!] You not done your verification. Why are you so fckin slow? {Style.reset}")
                            time.sleep(2)
                            print(f"The program is restarting... ")
                            time.sleep(1)
                            print("Kidding! The bot is shutting down")
                            driver.quit()
                            exit()
            else:
                print(f"{Fore.rgb(106,255,77)}[>>>] Navigating page...{Style.reset}")


            driver.get(product_url)
            time.sleep(5)
            get_information_about_product()
            
            countdown(end_time)

            # Stage 1 > Stage 2 > Check out

            print("-------------------------------------------")
            run_time = get_run_code_time(my_code_block)
            logger.info(f"Product URL: {product_url}")
            logger.info(f"Product classify: {classifyText} | Quantity: {quantity}")
            logger.info(f"Total running time: {run_time}")
            print(f"The run time of the code block is {Fore.cyan}{run_time}{Style.reset} seconds.")
            
            print("-------------------------------------------")

            quitAndRestart()

        elif choice == "7":
            break
        else:
            print(f"{Fore.yellow}[!] Invalid choice. {Style.reset}")




if __name__ == "__main__":

    website_url = "https://shopee.vn/buyer/login?next=https%3A%2F%2Fshopee.vn%2F"
    account_json_file = "accounts.json"

    # options = Options()
    # options.add_experimental_option("detach", True)
    # options.add_experimental_option("excludeSwitches", ["--disable-webrtc-stun-discovery"])
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    import undetected_chromedriver as uc
    driver = uc.Chrome(headless=False, use_subprocess=False)

    print(f"{Fore.rgb(166,77,255)} Thanks for using my bot. This bot is still in dev. So sometimes it can occur error. Hopefully you can enjoy it. Thanks <3{Style.reset}")
    product_url = input(f"{Fore.yellow}Shopee product's url: {Style.reset}")
    main()
