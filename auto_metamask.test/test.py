import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auto_metamask import *

if __name__ == '__main__':

    metamask_path = downloadMetamask(
        'https://github.com/MetaMask/metamask-extension/releases/download/v10.34.0/metamask-chrome-10.34.0.zip')
    driver = setupWebdriver(metamask_path, '/Applications/Chromium.app/Contents/MacOS/Chromium')
    # Test account, please do not use for production environment
    setupMetamask(
        'whip squirrel shine cabin access spell arrow review spread code fire marine', 'testtest')
    # Please use a special network name to avoid conflicts with built-in networks, such as 'MY_MATIC'
    addNetwork('MY_MATIC', 'https://rpc-mumbai.maticvigil.com', '80001', 'MATIC')
    changeNetwork('MY_MATIC')
    # Test account, please do not use for production environment
    importPK("bb334564f93fc3a40a3b6a89e0560101bb86e5b75c773381f1e6d2f37fc5c5ba")

    driver.switch_to.new_window()
    driver.get('https://metamask.github.io/test-dapp/')

    # Wait 20s for the page to load, and click the 'Connect' button
    wait = WebDriverWait(driver, 20, 1)
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='connectButton']"))).click()
    # MetaMask will pop up a window, complete the connection
    connectWallet()

    # Click the 'Request Permissions' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='requestPermissions']"))).click()
    # MetaMask will pop up a window
    connectWallet()

    # Click the 'Personal Sign' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='personalSign']"))).click()
    # MetaMask will pop up a window
    confirmWallet()

    # Click the 'Send Transaction' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='sendButton']"))).click()
    # MetaMask will pop up a window
    confirmWallet()
    waitPendingWallet()

    # Click the 'Create Token' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='createToken']"))).click()
    # MetaMask will pop up a window
    confirmWallet()
    waitPendingWallet()

    # Click the 'Approve Tokens' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='approveTokens']"))).click()
    # MetaMask will pop up a window
    approveTokens()
    waitPendingWallet()

    time.sleep(60)
    driver.quit()
