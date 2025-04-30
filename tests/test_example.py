import pytest
import allure
from selenium.webdriver.common.by import By
from pages.basePage import BasePage
from resources.config import get_base_url
from resources.test_data import get_user_credentials

@allure.feature("Authentication")
@allure.story("Login")
class TestLoginExample:
    
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        # Arrange
        base_page = BasePage(driver)
        credentials = get_user_credentials('user')
        login_url = f"{get_base_url()}/login"
        
        # Create locators
        username_field = (By.ID, "username")
        password_field = (By.ID, "password")
        login_button = (By.CSS_SELECTOR, "button[type='submit']")
        dashboard_element = (By.ID, "dashboard-welcome")
        
        # Actions
        with allure.step("Navigate to login page"):
            driver.get(login_url)
            base_page.wait_for_page_load()
        
        with allure.step(f"Enter username: {credentials['username']}"):
            base_page.type_text(username_field, credentials['username'])
            
        with allure.step("Enter password"):
            base_page.type_text(password_field, credentials['password'])
            
        with allure.step("Click login button"):
            base_page.click(login_button)
            
        # Assert
        with allure.step("Verify user is logged in"):
            assert base_page.is_element_visible(dashboard_element), \
                "Dashboard welcome message is not visible after login"
            
            welcome_text = base_page.get_text(dashboard_element)
            assert credentials['username'] in welcome_text, \
                f"Welcome message does not contain username. Got: {welcome_text}"
    
    @pytest.mark.regression
    @pytest.mark.ui
    @allure.title("Failed login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username,password,error_message", [
        ("invalid@example.com", "password123", "Invalid username or password"),
        ("", "password123", "Username is required"),
        ("user@example.com", "", "Password is required")
    ])
    def test_failed_login(self, driver, username, password, error_message):
        # Arrange
        base_page = BasePage(driver)
        login_url = f"{get_base_url()}/login"
        
        # Create locators
        username_field = (By.ID, "username")
        password_field = (By.ID, "password")
        login_button = (By.CSS_SELECTOR, "button[type='submit']")
        error_element = (By.CLASS_NAME, "error-message")
        
        # Act
        with allure.step("Navigate to login page"):
            driver.get(login_url)
            base_page.wait_for_page_load()
        
        with allure.step(f"Enter username: {username}"):
            if username:
                base_page.type_text(username_field, username)
            
        with allure.step("Enter password"):
            if password:
                base_page.type_text(password_field, password)
            
        with allure.step("Click login button"):
            base_page.click(login_button)
            
        # Assert
        with allure.step(f"Verify error message: '{error_message}'"):
            assert base_page.is_element_visible(error_element), \
                "Error message is not visible after failed login"
            
            actual_error = base_page.get_text(error_element)
            assert error_message in actual_error, \
                f"Expected error message '{error_message}' not found in '{actual_error}'"
