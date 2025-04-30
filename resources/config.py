import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URLs for different environments
BASE_URLS = {
    'dev': 'https://dev.example.com',
    'staging': 'https://staging.example.com',
    'prod': 'https://www.example.com'
}

# Current test environment
ENV = os.getenv('TEST_ENV', 'dev')

def get_base_url():
    """Get the base URL for the current test environment"""
    # Allow override via environment variable
    custom_url = os.getenv('BASE_URL')
    if custom_url:
        return custom_url
    
    return BASE_URLS[ENV]
