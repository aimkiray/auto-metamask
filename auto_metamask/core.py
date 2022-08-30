import os
import sys
import requests
import shutil
import logging
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

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
    options.add_argument("--window-size=1280,720")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Chrome is controlled by automated test software
    # options.binary_location = "/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_extension(metamask_path)
    s = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

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
    wait_fast = WebDriverWait(driver, 1, 1)

    global wait_slow
    wait_slow = WebDriverWait(driver, 40, 1)

    wait.until(EC.number_of_windows_to_be(2))

    global metamask_handle
    metamask_handle = driver.window_handles[0]

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
                (By.CSS_SELECTOR, '#popover-content > div > div > section > header > div > button'))).click()
            # wait_fast.until(EC.element_to_be_clickable(
            #     (By.XPATH, '//button[text()="Got it"]'))).click()
        except Exception:
            logging.warning("No popover")

        # Wait for transaction to appear in the list
        # if "Transaction" in func.__name__:
        #     time.sleep(5)
        #     try:
        #         wait.until(EC.element_to_be_clickable(
        #             (By.XPATH, '//button[text()="Activity"]'))).click()
        #         wait.until(EC.visibility_of_element_located(
        #             (By.CSS_SELECTOR, 'div.transaction-list__pending-transactions')))
        #     except Exception:
        #         logging.warning("No transaction")
        #         return

        func(*args, **kwargs)

        driver.switch_to.window(current_handle)
    return switch


@switchPage
def setupMetamask(recovery_phrase, password):
    """Autocomplete metamask welcome page

    :param recovery_phrase: Recovery phrase
    :type recovery_phrase: String
    :param password: Wallet password (minimum 8 characters)
    :type password: String
    """

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Get Started"]'))).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Import wallet"]'))).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="No Thanks"]'))).click()

    inputs = wait.until(
        EC.visibility_of_all_elements_located((By.XPATH, '//input')))

    inputs[0].send_keys(recovery_phrase)
    inputs[1].click()
    inputs[2].send_keys(password)
    inputs[3].send_keys(password)
    inputs[4].click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Import"]'))).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="All Done"]'))).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button'))).click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[text()="Assets"]')))
    except Exception:
        logging.error("Setup failed")
        sys.exit(1)

    logging.info('Setup success')


@switchPage
def addNetwork(network_name, rpc_url, chain_id, currency_symbol):
    """Add new network

    :param network_name: Network name
    :type network_name: String
    :param rpc_url: RPC URL
    :type rpc_url: String
    :param chain_id: Chain ID
    :type chain_id: String
    :param currency_symbol: Currency symbol
    :type currency_symbol: String
    """

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.app-header__network-component-wrapper > div'))).click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.menu-droppo-container.network-droppo > div > button'))).click()

    inputs = wait.until(
        EC.visibility_of_all_elements_located((By.XPATH, '//input')))

    inputs[0].send_keys(network_name)
    inputs[1].send_keys(rpc_url)
    inputs[2].send_keys(chain_id)
    inputs[3].send_keys(currency_symbol)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Save"]'))).click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//h6[text()="“' + network_name + '” was successfully added!"]')))
    except Exception:
        logging.error("Add network failed")
        sys.exit(1)

    logging.info('Add network success')


@switchPage
def changeNetwork(network_name):
    """Change network

    :param network_name: Network name
    :type network_name: String
    """

    logging.info('Changing network')

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.app-header__network-component-wrapper > div'))).click()

    network_dropdown_element = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'div.network-dropdown-list')))

    network_dropdown_list = network_dropdown_element.find_elements(
        by=By.TAG_NAME, value='li')

    for network_dropdown in network_dropdown_list:
        text = network_dropdown.text
        if (text == network_name):
            network_dropdown.click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[text()="Assets"]')))
    except Exception:
        logging.error("Change network failed")
        sys.exit(1)

    logging.info('Change network success')


@switchPage
def importPK(priv_key):
    """Import private key

    :param priv_key: private key
    :type priv_key: String
    """

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.account-menu__icon > div'))).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//div[text()="Import Account"]'))).click()

    input = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '#private-key-box')))

    input.send_keys(priv_key)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Import"]'))).click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[text()="Assets"]')))
    except Exception:
        logging.error("Import PK failed")
        sys.exit(1)

    logging.info('Import PK success')


@switchPage
def connectWallet():
    """Connect wallet
    """

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Next"]'))).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Connect"]'))).click()

    # try:
    #     driver.refresh()
    #     wait.until(EC.element_to_be_clickable(
    #         (By.XPATH, '//button[text()="Sign"]'))).click()
    # except Exception:
    #     logging.warning("No signature required")

    try:
        wait_slow.until_not(EC.element_to_be_clickable(
            (By.XPATH, '//button[text()="Connect"]')))
    except Exception:
        logging.error("Connect wallet failed")
        sys.exit(1)

    logging.info('Connect wallet successfully')


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
        sys.exit(1)

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
        sys.exit(1)

    logging.info('Confirm transaction successfully')
