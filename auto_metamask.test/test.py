import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auto_metamask import *

if __name__ == '__main__':

    metamask_path = downloadMetamask(
        'https://github.com/MetaMask/metamask-extension/releases/download/v10.11.2/metamask-chrome-10.11.2.zip')
    driver = setupWebdriver(metamask_path)
    # Test account, please do not use for production environment
    setupMetamask(
        'whip squirrel shine cabin access spell arrow review spread code fire marine', 'testtest')
    addNetwork('BSC', 'https://bsc-dataseed1.binance.org', '56', 'BNB')
    changeNetwork('BSC')
    # Test account, please do not use for production environment
    importPK("bb334564f93fc3a40a3b6a89e0560101bb86e5b75c773381f1e6d2f37fc5c5ba")

    driver.switch_to.new_window()
    driver.get('https://metamask.github.io/test-dapp/')

    wait = WebDriverWait(driver, 20, 1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Connect"]'))).click()
    connectWallet()

    time.sleep(60)
    driver.quit()
