"""
Test data module - contains sample test data for demonstration purposes.
In a real project, you might want to:
1. Connect to a test database
2. Load data from external files (CSV, JSON, etc.)
3. Generate random data with libraries like Faker
"""

# User credentials for different roles
USER_CREDENTIALS = {
    'admin': {
        'username': 'admin@example.com',
        'password': 'admin123',
        'role': 'Administrator'
    },
    'manager': {
        'username': 'manager@example.com',
        'password': 'manager123',
        'role': 'Manager'
    },
    'user': {
        'username': 'user@example.com',
        'password': 'user123',
        'role': 'Standard User'
    }
}

# Sample form data
REGISTRATION_DATA = {
    'valid_user': {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'P@ssw0rd123',
        'confirm_password': 'P@ssw0rd123',
        'phone': '1234567890',
        'country': 'United States',
        'agree_terms': True
    },
    'missing_required_fields': {
        'first_name': '',
        'last_name': 'Doe',
        'email': '',
        'password': 'P@ssw0rd123',
        'confirm_password': 'P@ssw0rd123',
        'phone': '1234567890',
        'country': 'United States',
        'agree_terms': True
    },
    'invalid_email': {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'not-an-email',
        'password': 'P@ssw0rd123',
        'confirm_password': 'P@ssw0rd123',
        'phone': '1234567890',
        'country': 'United States',
        'agree_terms': True
    }
}

# Sample product data
PRODUCTS = [
    {
        'id': 1,
        'name': 'Laptop',
        'price': 999.99,
        'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
        'category': 'Electronics',
        'in_stock': True
    },
    {
        'id': 2,
        'name': 'Smartphone',
        'price': 699.99,
        'description': 'Latest smartphone with 128GB storage and dual camera',
        'category': 'Electronics',
        'in_stock': True
    },
    {
        'id': 3,
        'name': 'Headphones',
        'price': 199.99,
        'description': 'Noise-cancelling wireless headphones',
        'category': 'Accessories',
        'in_stock': False
    }
]

# Search test data
SEARCH_QUERIES = {
    'valid_with_results': ['laptop', 'phone', 'electronics'],
    'valid_no_results': ['xylophone', 'zzzzzz', '12345xyz'],
    'special_characters': ['laptop$', '***', '><script>']
}

# Helper functions to get test data
def get_user_credentials(user_type='user'):
    """Get credentials for a specific user type"""
    return USER_CREDENTIALS.get(user_type, USER_CREDENTIALS['user'])

def get_registration_data(scenario='valid_user'):
    """Get registration form data for a specific scenario"""
    return REGISTRATION_DATA.get(scenario, REGISTRATION_DATA['valid_user'])

def get_product_by_id(product_id):
    """Get a product by ID"""
    for product in PRODUCTS:
        if product['id'] == product_id:
            return product
    return None
