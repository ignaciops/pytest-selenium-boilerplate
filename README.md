# pytest-selenium-boilerplate

A basic test automation boilerplate built with:

## Core Technologies
- **pytest**: Test runner and framework
- **Selenium WebDriver**: Browser automation
- **Allure**: Rich test reporting
- **Page Object Model**: Design pattern for maintainable tests

## Features
- Centralized configuration management
- Screenshot capture on test failure
- Parameterized testing support
- Cross-browser testing capabilities (Chrome, Firefox, Edge, Safari)
- Remote WebDriver support for grid/cloud testing
- Page Object Model implementation
- Detailed Allure reports with screenshots, logs, and HTML
- Session-scoped driver capability

## Setup

### Installation
```bash
# Clone the repository
git clone https://github.com/ignaciops/pytest-selenium-boilerplate.git
cd pytest-selenium-boilerplate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

A `.env.example` file is included in the repository with all available configuration options. 

To configure the framework:

1. Copy the example file to create your own `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to customize settings:
   ```
   # Browser configuration
   BROWSER=chrome           # chrome, firefox, edge, safari
   HEADLESS=False
   USE_REMOTE=False
   REMOTE_URL=http://localhost:4444/wd/hub

   # WebDriver Management
   USE_WEBDRIVER_MANAGER=False  # Set to True to use webdriver-manager, False to use drivers from PATH

   # Environment
   TEST_ENV=dev             # dev, staging, prod
   BASE_URL=https://custom-url.com  # Override environment URL

   # Timeouts
   DEFAULT_TIMEOUT=10
   PAGE_LOAD_TIMEOUT=30
   IMPLICIT_WAIT=5
   ```


## WebDriver Management

This framework provides two methods to manage browser drivers:

### Option 1: Manual WebDriver Installation (Default)
By default, the framework expects browser drivers to be installed manually and available in your system PATH.

1. Download the appropriate drivers:
   - Chrome: [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Firefox: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - Edge: [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

2. Add the driver location to your system PATH

### Option 2: Automatic WebDriver Management
The framework can automatically download and manage drivers using webdriver-manager.

To enable this feature, set in your .env file:
```
USE_WEBDRIVER_MANAGER=True
```

**Note:** While more convenient, automatic management may occasionally fail on some systems, particularly Windows. If you encounter issues, try option 1. To facilitate using both options, webdriver-manager is included in the requirements.txt file.

## Project Structure
```
pytest-selenium-boilerplate/
├── config/
│   └── test_config.py       # WebDriver configuration
├── pages/
│   └── basePage.py          # Base Page Object class
├── resources/
│   ├── config.py            # Environment configuration
│   └── test_data.py         # Test data and helper functions
├── tests/
│   ├── conftest.py          # pytest configuration
│   └── test_example.py      # Example test cases
├── screenshots/             # Screenshot storage
├── logs/                    # Test run logs
├── allure-results/          # Allure report data
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Usage

### Running Tests with the Test Runner

The project includes a convenient test runner script that simplifies test execution and always enables Allure reporting:

```bash
# Run all tests with Allure reporting
python run_tests.py

# Run only smoke tests
python run_tests.py --smoke

# Run regression tests with Firefox
python run_tests.py --regression --browser firefox

# Run UI tests in headless mode
python run_tests.py --ui --headless

# Run tests with 4 parallel processes
python run_tests.py --parallel 4

# Run specific test files
python run_tests.py tests/test_login.py
```

Make the script executable on Unix-based systems:
```bash
chmod +x run_tests.py
./run_tests.py --smoke
```

### Running Tests Directly with pytest

You can also run tests directly with pytest:

```bash
# Run with default settings (Chrome browser)
pytest

# Run with specific browser
pytest --browser firefox

# Run in headless mode
pytest --headless

# Run with Allure reporting
pytest --alluredir=allure-results

# Run in parallel (4 workers)
pytest -n 4

# Run with remote driver (Selenium Grid/Cloud)
pytest --remote

# Run tests by marker
pytest -m smoke
```

### Generating Allure Reports
```bash
# Generate and open Allure report
allure serve allure-results
```

### Test Categories

Tests can be categorized using pytest markers:

```python
@pytest.mark.smoke       # Smoke tests - critical path tests for basic functionality
@pytest.mark.regression  # Regression tests - more comprehensive tests
@pytest.mark.ui          # UI tests - tests that interact with the UI
@pytest.mark.api         # API tests - tests that interact with APIs
```

These markers can be combined to create more specific categories, and tests can have multiple markers.

## Page Object Model

This boilerplate implements an enhanced Page Object Model pattern:

- **BasePage**: Provides common methods for all page objects
  - Element interaction (click, type, find)
  - Waits and synchronization
  - Screenshots and error handling
  - Advanced interactions (dropdowns, alerts, iframes)
  - JavaScript execution

Example page class:
```python
from selenium.webdriver.common.by import By
from pages.basePage import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def navigate_to(self, base_url):
        self.driver.get(f"{base_url}/login")
        self.wait_for_page_load()
        
    def login(self, username, password):
        self.type_text(*self.USERNAME_FIELD, username)
        self.type_text(*self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)
        
    def get_error_message(self):
        if self.is_element_visible(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return None
```

## Best Practices

- Keep page objects focused on UI interactions only
- Store test data separately from tests in `resources/test_data.py`
- Use environment-specific configuration in `resources/config.py`
- Leverage parameterized tests for data-driven testing
- Add meaningful Allure annotations (`@allure.feature`, `@allure.story`, etc.)
- Use `with allure.step()` for better test reporting
- Use explicit waits rather than implicit waits where possible

## Screenshot Strategy

This framework employs a dual screenshot strategy:

1. **BasePage Screenshots**: Captured immediately when an element interaction fails during test execution. This provides details about the exact state when a specific action fails.

2. **Test Failure Screenshots**: Automatically captured via pytest hooks when a test fails, including integration with Allure reports. This shows the final state of the application after test failure.

Together, these strategies provide comprehensive visual evidence for debugging test failures at different levels.
