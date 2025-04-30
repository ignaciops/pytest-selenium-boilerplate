import os
import logging
import platform
import json
from datetime import datetime
import pytest
import allure
import selenium
from allure_commons.types import AttachmentType

from config.test_config import get_driver

def pytest_configure(config):
    """
    Configure the test environment before test collection begins.
    This hook is called once at the beginning of a test run.
    """
    # Create necessary directories
    directories = ['screenshots', 'logs', 'downloads', 'allure-results']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Configure logging
    log_file = f"logs/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Register custom marks
    config.addinivalue_line("markers", "smoke: mark test as part of smoke test suite")
    config.addinivalue_line("markers", "regression: mark test as part of regression test suite") 
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "ui: mark test as UI test")

    # Collect environment info
    config._metadata = {
        'Python Version': platform.python_version(),
        'Platform': platform.platform(),
        'Pytest Version': pytest.__version__,
        'Selenium Version': selenium.__version__,
    }
    
    # Configure Allure if it's being used
    if hasattr(config, 'getoption') and config.getoption('--alluredir'):
        try:
            allure_dir = config.getoption('--alluredir')
            with open(f"{allure_dir}/environment.properties", "w") as f:
                for key, value in config._metadata.items():
                    f.write(f"{key}={value}\n")
            
            # Add additional environment info in JSON format for Allure
            env_data = {
                **config._metadata,
                'Browser': os.getenv('BROWSER', 'chrome'),
                'Headless': os.getenv('HEADLESS', 'False'),
                'Environment': os.getenv('TEST_ENV', 'dev')
            }
            with open(f"{allure_dir}/environment.json", "w") as f:
                json.dump(env_data, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to create Allure environment file: {e}")

# Add command line options for browser selection and headless mode
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests (chrome, firefox, edge, safari)")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--remote", action="store_true", default=False, help="Use remote WebDriver")

# Fixture for standard function-scoped driver
@pytest.fixture(scope='function')
def driver(request):
    """
    Fixture to initialize and provide a WebDriver instance for tests.
    Browser type can be specified via command line option: --browser=[chrome|firefox|edge|safari]
    Headless mode can be enabled with --headless
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    remote = request.config.getoption("--remote")
    
    logging.info(f"Initializing {browser} driver (headless={headless}, remote={remote})")
    
    driver = get_driver(browser=browser, headless=headless, remote=remote)
    
    # Add browser info to Allure report
    if hasattr(request, "_allure"):
        allure.attach(
            f"Browser: {browser}\nHeadless: {headless}\nRemote: {remote}",
            name="Browser Configuration",
            attachment_type=AttachmentType.TEXT
        )
    
    # Setup complete
    yield driver
    
    # Teardown - quit driver
    driver.quit()

# Fixture for session-scoped driver when needed
@pytest.fixture(scope='session')
def session_driver(request):
    """
    Fixture to initialize and provide a session-wide WebDriver instance.
    Use this when you need to maintain browser state between tests.
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    remote = request.config.getoption("--remote")
    
    logging.info(f"Initializing session-wide {browser} driver")
    
    driver = get_driver(browser=browser, headless=headless, remote=remote)
    
    # Setup complete
    yield driver
    
    # Teardown - quit driver
    driver.quit()

# Implementation to take screenshots on test failure.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Always attach test logs to Allure report if available
    if hasattr(item, "_allure"):
        log_messages = []
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                try:
                    with open(handler.baseFilename, 'r') as f:
                        logs = f.read()
                        # Filter to get only logs relevant to this test (simplified approach)
                        log_messages.append(logs)
                except Exception as e:
                    print(f"Failed to read logs: {e}")
        
        if log_messages:
            allure.attach(
                "\n".join(log_messages),
                name="Test Logs",
                attachment_type=AttachmentType.TEXT
            )
    
    if report.when == "call" and report.failed:
        # Try to get the driver from any of the common fixture names
        for driver_name in ['driver', 'session_driver', 'authenticated_driver', 'browser']:
            try:
                if driver_name in item.funcargs:
                    driver = item.funcargs[driver_name]
                    screenshot_path = take_screenshot(driver, item.name)
                    
                    # Attach screenshot to Allure report if available
                    if hasattr(item, "_allure"):
                        with open(screenshot_path, "rb") as f:
                            allure.attach(
                                f.read(),
                                name="Failure Screenshot",
                                attachment_type=AttachmentType.PNG
                            )
                    
                    # Attach page source to Allure report if available
                    if hasattr(item, "_allure"):
                        allure.attach(
                            driver.page_source,
                            name="Page HTML",
                            attachment_type=AttachmentType.HTML
                        )
                    
                    break  # Found a driver, no need to check others
            except Exception as e:
                print(f"Failed to capture screenshot with {driver_name}: {e}")

def take_screenshot(driver, name):
    # Sanitize the test name for use in a filename
    sanitized_name = name.replace('/', '_').replace(':', '_').replace(' ', '_')
    
    # Create timestamp for unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create screenshot path using os.path.join for cross-platform compatibility
    screenshot_path = os.path.join('screenshots', f"{sanitized_name}_{timestamp}.png")
    
    # Take and save the screenshot
    driver.save_screenshot(screenshot_path)
    print(f"\nScreenshot saved to {screenshot_path}")
    
    return screenshot_path
