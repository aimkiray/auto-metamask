## Overview
Since web3 applications usually need to operate wallets (such as metamask), this tool can automate the operation of the metamask part to facilitate developers to test the application.

## Installation
auto-metamask can be installed using pip:

```shell
$ pip install auto-metamask
```

## Usage Examples

```python
import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

    time.sleep(6)
    driver.quit()
```

## API Reference

<a id="auto_metamask.core"></a>

### auto\_metamask.core

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
def setupWebdriver(metamask_path)
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

Autocomplete metamask welcome page

**Arguments**:

- `recovery_phrase` (`String`): Recovery phrase
- `password` (`String`): Wallet password (minimum 8 characters)

<a id="auto_metamask.core.addNetwork"></a>

#### addNetwork

```python
@switchPage
def addNetwork(network_name, rpc_url, chain_id, currency_symbol)
```

Add new network

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

Change network

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

- `priv_key` (`String`): private key

<a id="auto_metamask.core.connectWallet"></a>

#### connectWallet

```python
@switchPage
def connectWallet()
```

Connect wallet

<a id="auto_metamask.core.signWallet"></a>

#### signWallet

```python
@switchPage
def signWallet()
```

Sign wallet

<a id="auto_metamask.core.confirmTransaction"></a>

#### confirmTransaction

```python
@switchPage
def confirmTransaction()
```

Confirm transaction

## Credits

* [metamask-extension](https://github.com/MetaMask/metamask-extension)
* [selenium](https://github.com/SeleniumHQ/selenium)
* [selenium-stealth](https://github.com/diprajpatra/selenium-stealth)