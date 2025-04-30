import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Browser configuration
DEFAULT_BROWSER = os.getenv("BROWSER", "chrome")

# Timeout settings
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))

# Screenshot settings
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

# Remote WebDriver settings
USE_REMOTE = os.getenv("USE_REMOTE", "False").lower() == "true"
REMOTE_URL = os.getenv("REMOTE_URL", "http://localhost:4444/wd/hub")

# WebDriver management
USE_WEBDRIVER_MANAGER = os.getenv("USE_WEBDRIVER_MANAGER", "False").lower() == "true"

def get_driver(browser=DEFAULT_BROWSER, headless=False, remote=USE_REMOTE):
    """
    Initialize and return a WebDriver instance based on the specified browser.
    
    Args:
        browser (str): Browser to use ('chrome', 'firefox', 'edge', 'safari')
        headless (bool): Whether to run in headless mode
        remote (bool): Whether to use a remote WebDriver
        
    Returns:
        WebDriver: Configured WebDriver instance
    """
    browser = browser.lower()
    
    # Set browser capabilities and options
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        if remote:
            driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
        else:
            try:
                if USE_WEBDRIVER_MANAGER:
                    # Use webdriver-manager
                    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                else:
                    # Use driver from PATH
                    driver = webdriver.Chrome(options=options)
            except Exception as e:
                # Fallback logic if the preferred method fails
                print(f"Failed to initialize Chrome driver using {'webdriver-manager' if USE_WEBDRIVER_MANAGER else 'PATH'}: {e}")
                print(f"Trying alternative method...")
                if USE_WEBDRIVER_MANAGER:
                    # Try using driver from PATH as fallback
                    driver = webdriver.Chrome(options=options)
                else:
                    # Try using webdriver-manager as fallback
                    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        
        if remote:
            driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
        else:
            try:
                if USE_WEBDRIVER_MANAGER:
                    # Use webdriver-manager
                    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
                else:
                    # Use driver from PATH
                    driver = webdriver.Firefox(options=options)
            except Exception as e:
                # Fallback logic
                print(f"Failed to initialize Firefox driver using {'webdriver-manager' if USE_WEBDRIVER_MANAGER else 'PATH'}: {e}")
                print(f"Trying alternative method...")
                if USE_WEBDRIVER_MANAGER:
                    driver = webdriver.Firefox(options=options)
                else:
                    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    
    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        
        if remote:
            driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
        else:
            try:
                if USE_WEBDRIVER_MANAGER:
                    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
                else:
                    driver = webdriver.Edge(options=options)
            except Exception as e:
                print(f"Failed to initialize Edge driver using {'webdriver-manager' if USE_WEBDRIVER_MANAGER else 'PATH'}: {e}")
                print(f"Trying alternative method...")
                if USE_WEBDRIVER_MANAGER:
                    driver = webdriver.Edge(options=options)
                else:
                    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    
    elif browser == "safari":
        options = SafariOptions()
        # Safari doesn't support headless mode
        if remote:
            driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
        else:
            # Safari doesn't need webdriver-manager
            driver = webdriver.Safari(options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    return driver
