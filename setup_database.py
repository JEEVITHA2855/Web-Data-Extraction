"""
Database Setup Script
Creates the database and tables for the web scraping project
"""

import mysql.connector
from config import DB_CONFIG

def setup_database():
    """
    Creates database and tables
    """
    print("🔧 Setting up database...")
    
    # Connect without specifying database
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database
        print(f"📦 Creating database '{DB_CONFIG['database']}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print("✅ Database created successfully")
        
        # Use the database
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create table
        print("📋 Creating products table...")
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
        print("✅ Table created successfully")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Database setup complete! You can now run: python scraper.py")
        
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. MySQL server is running")
        print("   2. Username and password in config.py are correct")

if __name__ == "__main__":
    setup_database()
