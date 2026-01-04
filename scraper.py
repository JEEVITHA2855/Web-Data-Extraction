"""
Web Data Extraction & Analysis Project
Extracts product data from a website, cleans it, and stores in MySQL

Author: Interview-Ready Project
Date: January 2026
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
import time
import re
from config import DB_CONFIG

class WebScraper:
    """
    Main scraper class that handles data extraction, cleaning, and storage
    """
    
    def __init__(self, url, max_pages=1):
        self.url = url
        self.max_pages = max_pages
        self.raw_data = []
        self.cleaned_data = []
        
    def scrape_data(self):
        """
        Uses Selenium to open website and extract HTML content
        Selenium is necessary for JavaScript-rendered pages
        Supports multi-page scraping for comprehensive data collection
        """
        print("🌐 Opening website with Selenium...")
        
        # Initialize Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            for page_num in range(1, self.max_pages + 1):
                # Modify URL for pagination (works for books.toscrape.com)
                if 'page-' in self.url:
                    current_url = self.url.replace('page-1', f'page-{page_num}')
                else:
                    current_url = self.url
                
                print(f"📄 Scraping page {page_num}/{self.max_pages}...")
                
                # Load the page
                driver.get(current_url)
                print("⏳ Waiting for page to load...")
                time.sleep(3)  # Wait for dynamic content
                
                # Get page source
                html = driver.page_source
                
                # Parse with BeautifulSoup
                self.parse_html(html)
                
                print(f"✅ Page {page_num} completed. Total items so far: {len(self.raw_data)}")
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
        finally:
            driver.quit()
            print("✅ Browser closed")
    
    def parse_html(self, html):
        """
        Parses HTML using BeautifulSoup to extract structured data
        Real scraping from books.toscrape.com
        """
        print("🔍 Parsing HTML content...")
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract book items from books.toscrape.com
        items = soup.find_all("article", class_="product_pod")
        
        if not items:
            print("❌ No items found. Website structure may have changed.")
            return
        
        print(f"🎯 Found {len(items)} products on page")
        
        for item in items:
            try:
                # Extract book title
                title_tag = item.find("h3").find("a")
                name = title_tag.get('title', 'Unknown')
                
                # Extract price
                price_tag = item.find("p", class_="price_color")
                price = price_tag.text.strip() if price_tag else 'N/A'
                
                # Extract rating (star-rating class)
                rating_tag = item.find("p", class_="star-rating")
                rating_class = rating_tag.get('class')[1] if rating_tag else 'Zero'
                
                # Convert rating class to number
                rating_map = {
                    'One': '1.0', 'Two': '2.0', 'Three': '3.0', 
                    'Four': '4.0', 'Five': '5.0', 'Zero': '0.0'
                }
                rating = rating_map.get(rating_class, '0.0')
                
                if name and price:
                    self.raw_data.append({
                        'name': name,
                        'price': price,
                        'rating': rating
                    })
            except Exception as e:
                print(f"⚠️  Skipping item due to error: {e}")
        
        print(f"📦 Extracted {len(self.raw_data)} items")
    

    
    def clean_data(self):
        """
        Cleans raw scraped data:
        - Removes currency symbols (£, ₹, $)
        - Removes commas from numbers
        - Converts to proper data types
        - Handles missing values
        - Validates data integrity
        """
        print("🧹 Cleaning data...")
        
        for item in self.raw_data:
            try:
                # Clean name
                name = item['name'].strip()
                
                # Clean price - remove currency symbols (£, ₹, $) and commas
                price_str = item['price'].replace('£', '').replace('₹', '').replace('$', '').replace(',', '').strip()
                price = float(price_str) if price_str else 0.0
                
                # Clean rating - convert to float
                rating_str = item['rating'].replace('N/A', '0')
                rating = float(rating_str) if rating_str else 0.0
                
                # Validate data
                if name and price > 0:
                    self.cleaned_data.append({
                        'name': name,
                        'price': price,
                        'rating': rating
                    })
                else:
                    print(f"⚠️  Skipping invalid item: {name}")
                    
            except Exception as e:
                print(f"⚠️  Error cleaning item: {e}")
        
        print(f"✅ Cleaned {len(self.cleaned_data)} items")
        
        # Remove duplicates based on name
        seen = set()
        unique_data = []
        for item in self.cleaned_data:
            if item['name'] not in seen:
                seen.add(item['name'])
                unique_data.append(item)
        
        self.cleaned_data = unique_data
        print(f"✅ Removed duplicates. Final count: {len(self.cleaned_data)}")
    
    def store_in_database(self):
        """
        Stores cleaned data in MySQL database
        Uses parameterized queries to prevent SQL injection
        """
        print("💾 Connecting to MySQL database...")
        
        conn = None
        cursor = None
        
        try:
            # Connect to MySQL
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    price FLOAT NOT NULL,
                    rating FLOAT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_price (price),
                    INDEX idx_rating (rating)
                )
            """)
            
            # Insert data using parameterized query
            insert_query = """
                INSERT INTO products (name, price, rating) 
                VALUES (%s, %s, %s)
            """
            
            data_tuples = [
                (item['name'], item['price'], item['rating']) 
                for item in self.cleaned_data
            ]
            
            cursor.executemany(insert_query, data_tuples)
            conn.commit()
            
            print(f"✅ Successfully inserted {cursor.rowcount} records")
            
            # Verify insertion
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            print(f"📊 Total records in database: {count}")
            
        except mysql.connector.Error as e:
            print(f"❌ Database error: {e}")
            print("\n💡 Troubleshooting:")
            print("   1. Make sure MySQL is running")
            print("   2. Check username/password in config.py")
            print("   3. Create database: CREATE DATABASE scraping_db;")
            return False
        finally:
            if conn and conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
                print("🔌 Database connection closed")
        
        return True
    
    def run_analysis(self):
        """
        Performs SQL analysis on stored data
        """
        print("\n📊 Running data analysis...")
        
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Analysis 1: Average price
            cursor.execute("SELECT AVG(price) FROM products")
            avg_price = cursor.fetchone()[0]
            print(f"\n💰 Average Price: £{avg_price:,.2f}")
            
            # Analysis 2: High-value products
            cursor.execute("SELECT name, price FROM products WHERE price > 50 ORDER BY price DESC LIMIT 10")
            high_value = cursor.fetchall()
            print(f"\n🏆 High-Value Products (>£50):")
            for name, price in high_value:
                print(f"   - {name}: £{price:,.2f}")
            
            # Analysis 3: Top rated products
            cursor.execute("SELECT name, rating FROM products WHERE rating >= 4.5 ORDER BY rating DESC LIMIT 5")
            top_rated = cursor.fetchall()
            print(f"\n⭐ Top Rated Products (≥4.5):")
            for name, rating in top_rated:
                print(f"   - {name}: {rating}/5.0")
            
            # Analysis 4: Price distribution
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN price < 20 THEN 'Budget (<£20)'
                        WHEN price BETWEEN 20 AND 40 THEN 'Mid-Range (£20-40)'
                        WHEN price BETWEEN 40 AND 60 THEN 'Premium (£40-60)'
                        ELSE 'Luxury (>£60)'
                    END as price_range,
                    COUNT(*) as count
                FROM products
                GROUP BY price_range
            """)
            distribution = cursor.fetchall()
            print(f"\n📈 Price Distribution:")
            for range_name, count in distribution:
                print(f"   - {range_name}: {count} products")
            
        except mysql.connector.Error as e:
            print(f"❌ Analysis error: {e}")
        finally:
            if conn and conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()


def main():
    """
    Main execution function
    """
    print("=" * 60)
    print("🚀 WEB DATA EXTRACTION & ANALYSIS PROJECT")
    print("=" * 60)
    
    # Target URL - books.toscrape.com (legal practice scraping site)
    url = "http://books.toscrape.com/catalogue/page-1.html"
    print(f"🎯 Target: {url}")
    
    # Initialize scraper
    scraper = WebScraper(url)
    
    # Step 1: Scrape data
    scraper.scrape_data()
    
    # Step 2: Clean data
    if scraper.raw_data:
        scraper.clean_data()
    else:
        print("❌ No data to clean")
        return
    
    # Step 3: Store in database
    if scraper.cleaned_data:
        success = scraper.store_in_database()
        if not success:
            print("\n⚠️  Database storage failed. Skipping analysis.")
            print("📊 You can still view the cleaned data above.")
            return
    else:
        print("❌ No cleaned data to store")
        return
    
    # Step 4: Run analysis
    scraper.run_analysis()
    
    print("\n" + "=" * 60)
    print("✅ PROJECT EXECUTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
