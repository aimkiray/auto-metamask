## Overview

To streamline the testing process for developers, this tool automates the management of the MetaMask component, a wallet operation often essential for the functionality of Web3 applications.

## Installation

auto-metamask can be installed using pip:

```shell
$ pip install auto-metamask
```

Ensure you've installed either the Chromium or Chrome browser. In the absence of a specified directory, the default system Chrome will be used. It's advisable to avoid the newest version of Chrome due to the unavailability of a corresponding Chrome driver.

The Metamask extension is optimized for version 10.34.0, dated July 10, 2023. It's recommended to use this version. For those inclined to use an earlier version, please opt for version 0.1.3 of this package.

Alternatively, you can download a specific version of the Chromium browser along with the compatible Chrome driver manually. After downloading, provide its path to the setupWebdriver function.

For a comprehensive list of Chromium browser versions and their respective Chrome drivers, visit: Chromium Browser Snapshots.

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
    driver = setupWebdriver(metamask_path, '/Applications/Chromium.app/Contents/MacOS/Chromium', None, 'chromedriver_mac64/chromedriver')
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
    connect()

    # Click the 'Request Permissions' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='requestPermissions']"))).click()
    # MetaMask will pop up a window
    connect()

    # Click the 'Personal Sign' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='personalSign']"))).click()
    # MetaMask will pop up a window
    confirm()

    # Click the 'Send Transaction' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='sendButton']"))).click()
    # MetaMask will pop up a window
    confirm()
    waitPending(20)

    # Click the 'Create Token' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='createToken']"))).click()
    # MetaMask will pop up a window
    confirm()
    waitPending(20)

    # Click the 'Approve Tokens' button
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id='approveTokens']"))).click()
    # MetaMask will pop up a window
    approveTokens(6)
    waitPending(20)

    time.sleep(60)
    driver.quit()
```

## API Reference

<a id="auto_metamask.core.downloadMetamask"></a>

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
def setupWebdriver(metamask_path,
                   chrome_path=None,
                   version=None,
                   chromedriver_path=None)
```

Initialize chrome browser and install metamask extension

**Arguments**:

- `metamask_path` (`String`): Extension file path
- `chrome_path` (`String`): Chrome browser path, default is None.
- `version` (`String`): Chrome browser version, make sure it matches the chromedriver version, if not provided, the latest version will be used, default is None. if chromedriver_path is provided, this parameter will be ignored.
- `chromedriver_path` (`String`): Chromedriver file path, default is None.

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

<a id="auto_metamask.core.connect"></a>

#### connect

```python
@switchPage
def connect()
```

Connect wallet

<a id="auto_metamask.core.approve"></a>

#### approve

```python
@switchPage
def approve()
```

Approve wallet

<a id="auto_metamask.core.approveTokens"></a>

#### approveTokens

```python
@switchPage
def approveTokens(cap=None)
```

Approve tokens

**Arguments**:

- `cap` (`Number`): Spending limit, must be greater than 0, default is None.

<a id="auto_metamask.core.confirm"></a>

#### confirm

```python
@switchPage
def confirm()
```

Confirm wallet

Use for Transaction, Sign, Deploy Contract, Create Token, Add Token, Sign In, etc.

<a id="auto_metamask.core.waitPending"></a>

#### waitPending

```python
@switchPage
def waitPending(timeout=40)
```

Wait pending

**Arguments**:

- `timeout` (`Number`): Timeout (seconds)

## Credits

* [metamask-extension](https://github.com/MetaMask/metamask-extension)
* [selenium](https://github.com/SeleniumHQ/selenium)
* [selenium-stealth](https://github.com/diprajpatra/selenium-stealth)