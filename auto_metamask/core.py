import os
import requests
import shutil
import logging
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

file_path = os.getcwd()
log_format = "%(asctime)s %(levelname)s %(message)s"
date_format = "%m-%d-%Y %H:%M:%S"
logging.basicConfig(filename=file_path+"/auto-metamask.log", level=logging.INFO,
                    format=log_format, datefmt=date_format)


def downloadMetamask(url):
    """Download the metamask extension

    :param url: Metamask extension download address (.zip)
    :type url: String
    :return: Extension file path
    :rtype: String
    """
    logging.info("Downloading metamask...")
    local_filename = file_path + '/' + url.split('/')[-1]

    if os.path.exists(local_filename):
        logging.info("Metamask " + local_filename + " found in cache")
        return local_filename

    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


def setupWebdriver(metamask_path):
    """Initialize chrome browser and install metamask extension

    :param metamask_path: Extension file path
    :type metamask_path: String
    :return: Selenium Chrome WebDriver
    :rtype: WebDriver
    """

    options = Options()
    # options.add_argument('--start-maximized')
    options.add_argument("--window-size=1440,900")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Chrome is controlled by automated test software
    # options.binary_location = "/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_extension(metamask_path)
    s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    global driver
    driver = webdriver.Chrome(service=s, options=options)

    # Selenium Stealth settings
    stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
            )

    global wait
    wait = WebDriverWait(driver, 20, 1)

    global wait_fast
    wait_fast = WebDriverWait(driver, 5, 1)

    global wait_slow
    wait_slow = WebDriverWait(driver, 40, 1)

    wait.until(EC.number_of_windows_to_be(2))

    global metamask_handle
    metamask_handle = driver.window_handles[1]

    driver.switch_to.window(metamask_handle)
    wait.until(EC.url_contains('home'))

    global metamask_url
    metamask_url = driver.current_url.split('#')[0]

    return driver


def switchPage(func):
    @wraps(func)
    def switch(*args, **kwargs):
        current_handle = driver.current_window_handle
        driver.switch_to.window(metamask_handle)

        driver.get(metamask_url)

        try:
            wait_fast.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='popover-close']"))).click()
        except Exception:
            logging.warning("No popover")

        func(*args, **kwargs)

        try:
            wait_fast.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='popover-close']"))).click()
        except Exception:
            logging.warning("No popover")

        driver.switch_to.window(current_handle)
    return switch


@switchPage
def setupMetamask(recovery_phrase, password):
    """Setup metamask wallet

    :param recovery_phrase: Recovery phrase (12 words)
    :type recovery_phrase: String
    :param password: Wallet password (minimum 8 characters)
    :type password: String
    """

    wait_slow.until(EC.invisibility_of_element_located(
        (By.CSS_SELECTOR, "div[class='loading-overlay__container']")))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[data-testid='onboarding-terms-checkbox']"))).click()
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='onboarding-import-wallet']"))).click()
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='metametrics-no-thanks']"))).click()

    # Split the recovery phrase into individual words
    words = recovery_phrase.split(' ')
    word_count = len(words)

    # Check if the length of the words is valid
    if word_count not in [12, 15, 18, 21, 24]:
        logging.error(
            "Invalid recovery phrase. The phrase should be 12, 15, 18, 21, or 24 words long.")
    else:
        # Select the dropdown
        # //*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select
        # //*[contains(@class, 'dropdown__select')]
        # //div[@class='import-srp__container']//select[@class='dropdown__select']
        select = Select(wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='import-srp__container']//select[@class='dropdown__select']"))))

        # Select option by value (number of words)
        select.select_by_value(str(word_count))
        # For each input field
        for i in range(word_count):
            # Get the corresponding word
            word = words[i]

            # Input the word into the field
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f"input[data-testid='import-srp__srp-word-{i}']"))).send_keys(word)

    # Click the confirm button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='import-srp-confirm']"))).click()

    # find the password input and type the password
    new_password = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='create-password-new']")))
    new_password.send_keys(password)

    # find the confirm password input and type the password
    confirm_password = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='create-password-confirm']")))
    confirm_password.send_keys(password)

    # find the terms checkbox and click
    terms_checkbox = driver.find_element(
        By.CSS_SELECTOR, "input[data-testid='create-password-terms']")
    terms_checkbox.click()

    # find the submit button and click
    submit_button = driver.find_element(
        By.CSS_SELECTOR, "button[data-testid='create-password-import']")
    submit_button.click()

    # find the all done button and click
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='onboarding-complete-done']"))).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='pin-extension-next']"))).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='pin-extension-done']"))).click()

    try:
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='popover-close']"))).click()
    except Exception:
        logging.warning("No welcome popover")
        return

    try:
        # This button is only available when the popup is closed
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Setup failed")
        return

    logging.info('Setup success')


@switchPage
def addNetwork(network_name, rpc_url, chain_id, currency_symbol):
    """Add a custom network

    :param network_name: Network name
    :type network_name: String
    :param rpc_url: RPC URL
    :type rpc_url: String
    :param chain_id: Chain ID
    :type chain_id: String
    :param currency_symbol: Currency symbol
    :type currency_symbol: String
    """

    # Switch to the settings page
    driver.get(metamask_url + '#settings/networks/add-network')

    # network-display
    # wait.until(EC.element_to_be_clickable(
    #     (By.CSS_SELECTOR, "button[data-testid='network-display']"))).click()

    # //div[contains(@class, 'multichain-network-list-menu-content-wrapper')]//button[contains(@class, 'mm-button-secondary')]
    # wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, "//div[contains(@class, 'multichain-network-list-menu-content-wrapper')]//button[contains(@class, 'mm-button-secondary')]"))).click()

    inputs = wait.until(
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='networks-tab__add-network-form-body']//input")))

    inputs[0].send_keys(network_name)
    inputs[1].send_keys(rpc_url)
    inputs[2].send_keys(chain_id)
    inputs[3].send_keys(currency_symbol)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'networks-tab__add-network-form-footer')]//button[contains(@class, 'btn-primary')]"))).click()

    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'home__new-network-added__switch-to-button')]"))).click()
    except Exception:
        logging.error("Add network failed")
        return

    logging.info('Add network success')


@switchPage
def changeNetwork(network_name):
    """Change network

    :param network_name: Network name
    :type network_name: String
    """

    logging.info('Change network')

    # display the network list
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='network-display']"))).click()

    # click the network name
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[text()='{}']".format(network_name)))).click()

    try:
        # check if the network is changed
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//p[text()='{}']".format(network_name))))
    except Exception:
        logging.error("Change network failed")
        return

    logging.info('Change network success')


@switchPage
def importPK(priv_key):
    """Import private key

    :param priv_key: Private key
    :type priv_key: String
    """

    # Click the account menu
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='account-menu-icon']"))).click()
    # Click the import account button
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//section[contains(@class, 'multichain-account-menu-popover')]//button[contains(@class, 'mm-button-base--size-sm')])[2]"))).click()

    key_input = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '#private-key-box')))

    key_input.send_keys(priv_key)

    # Click the import button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='import-account-confirm-button']"))).click()

    try:
        # This button is only available when the popup is closed
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Import PK failed")
        return

    logging.info('Import PK success')


@switchPage
def connectWallet():
    """Connect wallet
    """

    # Next
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='page-container-footer-next']"))).click()

    # Confirm
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-testid='page-container-footer-next']"))).click()

    try:
        # This button is only available when the popup is closed
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Connect wallet failed")
        return

    logging.info('Connect wallet successfully')


@switchPage
def approveWallet():
    """Approve wallet
    """

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'btn-primary')]"))).click()
    
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'btn-primary')]"))).click()

    try:
        # This button is only available when the popup is closed
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='eth-overview-send']")))
    except Exception:
        logging.error("Import PK failed")
        return

    logging.info('Approve successfully')


@switchPage
def signWallet():
    """Sign wallet
    """

    try:
        wait_fast.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[text()="Sign"]')))
    except Exception:
        logging.warning('Sign refresh')
        driver.refresh()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Sign"]'))).click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[text()="Assets"]')))
    except Exception:
        logging.error("Connect wallet failed")
        return

    logging.info('Sign successfully')


@switchPage
def confirmTransaction():
    """Confirm transaction
    """

    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[text()="Activity"]'))).click()
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.transaction-list__pending-transactions')))
    except Exception:
        logging.error("No transaction")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Confirm"]'))).click()

    try:
        wait_slow.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.transaction-status--pending')))
        wait_slow.until_not(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.transaction-status--pending')))
    except Exception:
        logging.error("Confirm transaction failed")
        return

    logging.info('Confirm transaction successfully')
