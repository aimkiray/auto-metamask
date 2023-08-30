## Overview
Web3 applications often require the operation of wallets, such as MetaMask, for their functionality. This tool has been designed to automate the handling of the MetaMask component, making it easier for developers to test their applications.

## Installation
auto-metamask can be installed using pip:

```shell
$ pip install auto-metamask
```

Please make sure that you have installed [Chromium](https://www.chromium.org/getting-involved/download-chromium) or [Chrome](https://www.google.com/chrome/) browser. If no directory is specified, the system default Chrome will be used. It is recommended not to use the latest version of Chrome, as there is no matching Chrome driver.

The Metamask extension is compatible with version 10.34.0 from July 10, 2023. Please try to use this version. If you wish to use an older version, please use version 0.1.3 of this extension.

## Usage Examples

```python
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
```

## API Reference

#### downloadMetamask

```python
def downloadMetamask(url)
```

Download the metamask extension

**Arguments**:

- `url` (`String`): Metamask extension download address (.zip)

**Returns**:

`String`: Extension file path

<a id="auto_metamask.core.setupWebdriver"></a>

#### setupWebdriver

```python
def setupWebdriver(metamask_path, chrome_path=None)
```

Initialize chrome browser and install metamask extension

**Arguments**:

- `metamask_path` (`String`): Extension file path

**Returns**:

`WebDriver`: Selenium Chrome WebDriver

<a id="auto_metamask.core.setupMetamask"></a>

#### setupMetamask

```python
@switchPage
def setupMetamask(recovery_phrase, password)
```

Setup metamask wallet

**Arguments**:

- `recovery_phrase` (`String`): Recovery phrase (12 words)
- `password` (`String`): Wallet password (minimum 8 characters)

<a id="auto_metamask.core.addNetwork"></a>

#### addNetwork

```python
@switchPage
def addNetwork(network_name, rpc_url, chain_id, currency_symbol)
```

Add a custom network

**Arguments**:

- `network_name` (`String`): Network name
- `rpc_url` (`String`): RPC URL
- `chain_id` (`String`): Chain ID
- `currency_symbol` (`String`): Currency symbol

<a id="auto_metamask.core.changeNetwork"></a>

#### changeNetwork

```python
@switchPage
def changeNetwork(network_name)
```

Switch to a network

**Arguments**:

- `network_name` (`String`): Network name

<a id="auto_metamask.core.importPK"></a>

#### importPK

```python
@switchPage
def importPK(priv_key)
```

Import private key

**Arguments**:

- `priv_key` (`String`): Private key

<a id="auto_metamask.core.connectWallet"></a>

#### connectWallet

```python
@switchPage
def connectWallet()
```

Connect wallet

<a id="auto_metamask.core.approveWallet"></a>

#### approveWallet

```python
@switchPage
def approveWallet()
```

Approve wallet

<a id="auto_metamask.core.approveTokens"></a>

#### approveTokens

```python
@switchPage
def approveTokens()
```

Approve tokens

<a id="auto_metamask.core.confirmWallet"></a>

#### confirmWallet

```python
@switchPage
def confirmWallet()
```

Confirm wallet

Use for Transaction, Sign, Deploy Contract, Create Token, Add Token, Sign In, etc.

<a id="auto_metamask.core.waitPendingWallet"></a>

#### waitPendingWallet

```python
@switchPage
def waitPendingWallet()
```

Wait pending

## Credits

* [metamask-extension](https://github.com/MetaMask/metamask-extension)
* [selenium](https://github.com/SeleniumHQ/selenium)
* [selenium-stealth](https://github.com/diprajpatra/selenium-stealth)