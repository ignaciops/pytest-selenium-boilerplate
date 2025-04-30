import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from config.test_config import DEFAULT_TIMEOUT

class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    # Basic element interactions
    def find_element(self, locator):
        """Find an element with explicit wait
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        by, value = locator
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.take_screenshot(f"element_not_found_{value}")
            raise Exception(f"Element not found with {by}={value}")
    
    def find_elements(self, locator):
        """Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        by, value = locator
        try:
            self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return self.driver.find_elements(by, value)
        except TimeoutException:
            return []
    
    def click(self, locator):
        """Click element with explicit wait for clickability
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        by, value = locator
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
        except Exception as e:
            self.take_screenshot(f"click_failed_{value}")
            raise Exception(f"Failed to click element with {by}={value}: {str(e)}")
    
    def type_text(self, locator, text, clear=True):
        """Type text into input field with option to clear first
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            text: Text to type into the element
            clear: Whether to clear the field before typing (default: True)
        """
        element = self.find_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get element text with explicit wait
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible within timeout
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            timeout: Custom timeout in seconds (default: None, uses class timeout)
        """
        by, value = locator
        wait_time = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=None):
        """Check if element is present in DOM within timeout
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            timeout: Custom timeout in seconds (default: None, uses class timeout)
        """
        by, value = locator
        wait_time = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    # Advanced interactions
    def select_dropdown_by_text(self, locator, text):
        """Select dropdown option by visible text
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            text: Visible text of the option to select
        """
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, option_value):
        """Select dropdown option by value attribute
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            option_value: Value attribute of the option to select
        """
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(option_value)
    
    def select_dropdown_by_index(self, locator, index):
        """Select dropdown option by index
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            index: Index of the option to select (0-based)
        """
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_index(index)
    
    def get_dropdown_selected_text(self, locator):
        """Get selected option text from dropdown
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        element = self.find_element(locator)
        select = Select(element)
        return select.first_selected_option.text
    
    def hover(self, locator):
        """Hover over an element
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
    
    def double_click(self, locator):
        """Double click on an element
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        element = self.find_element(locator)
        ActionChains(self.driver).double_click(element).perform()
    
    def right_click(self, locator):
        """Right click on an element
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        element = self.find_element(locator)
        ActionChains(self.driver).context_click(element).perform()
    
    def drag_and_drop(self, source_locator, target_locator):
        """Drag and drop from source element to target element
        
        Args:
            source_locator: Tuple of (by, value) for the source element
            target_locator: Tuple of (by, value) for the target element
        """
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()
    
    def scroll_to_element(self, locator):
        """Scroll to element using JavaScript
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Small pause to allow the page to settle after scrolling
        time.sleep(0.5)
    
    def scroll_to_top(self):
        """Scroll to the top of the page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait methods
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear from the DOM
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
            timeout: Custom timeout in seconds (default: None, uses class timeout)
        """
        by, value = locator
        wait_time = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until_not(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to complete loading
        
        Args:
            timeout: Custom timeout in seconds (default: None, uses class timeout)
        """
        wait_time = timeout if timeout is not None else self.timeout
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    # Alert handling
    def accept_alert(self):
        """Accept an alert"""
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()
    
    def dismiss_alert(self):
        """Dismiss an alert"""
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()
    
    def get_alert_text(self):
        """Get text from an alert"""
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert.text
    
    # Frame handling
    def switch_to_frame(self, locator):
        """Switch to iframe by locator
        
        Args:
            locator: Tuple of (by, value) where by is a By enum value and value is the locator string
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
    
    # JavaScript execution
    def execute_js(self, script, *args):
        """Execute JavaScript in the browser"""
        return self.driver.execute_script(script, *args)
    
    # Utility methods
    def take_screenshot(self, name):
        """Take a screenshot with a custom name"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
        
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            
        file_name = f"{name}_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, file_name)
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path
    
    def get_page_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_load()
