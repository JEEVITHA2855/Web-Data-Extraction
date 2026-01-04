"""
Clear all data from products table
"""

import mysql.connector
from config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("TRUNCATE TABLE products")
    conn.commit()
    
    print("✅ Database cleared successfully!")
    print("📊 All old data removed. Ready for fresh scraping.")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ Error: {e}")
