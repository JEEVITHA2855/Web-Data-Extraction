"""
Configuration file for database connection and project settings
"""

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2855',  # Change this to your MySQL password
    'database': 'scraping_db'
}

# Scraper Settings
SCRAPER_SETTINGS = {
    'wait_time': 5,  # Seconds to wait for page load
    'headless': True,  # Run browser in background
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Data Quality Thresholds
DATA_QUALITY = {
    'min_price': 0,
    'max_price': 10000000,
    'min_rating': 0,
    'max_rating': 5.0
}
