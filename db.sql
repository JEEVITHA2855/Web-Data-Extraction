-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS scraping_db;
USE scraping_db;

-- Step 2: Create Products Table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price FLOAT NOT NULL,
    rating FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Step 3: Create Indexes for Performance
CREATE INDEX idx_price ON products(price);
CREATE INDEX idx_rating ON products(rating);
CREATE INDEX idx_name ON products(name);

-- =====================================================
-- DATA QUALITY CHECKS
-- =====================================================

-- Check for NULL values
SELECT 'NULL Check' as check_type, COUNT(*) as issues 
FROM products 
WHERE name IS NULL OR price IS NULL;

-- Check for duplicates
SELECT 'Duplicate Check' as check_type, name, COUNT(*) as count 
FROM products 
GROUP BY name 
HAVING COUNT(*) > 1;

-- Check for invalid prices
SELECT 'Invalid Price Check' as check_type, COUNT(*) as issues 
FROM products 
WHERE price <= 0;

-- Check for invalid ratings
SELECT 'Invalid Rating Check' as check_type, COUNT(*) as issues 
FROM products 
WHERE rating < 0 OR rating > 5;

-- =====================================================
-- DATA ANALYSIS QUERIES
-- =====================================================

-- Analysis 1: Basic Statistics
SELECT 
    COUNT(*) as total_products,
    MIN(price) as min_price,
    MAX(price) as max_price,
    AVG(price) as avg_price,
    AVG(rating) as avg_rating
FROM products;

-- Analysis 2: Average Price
SELECT AVG(price) as average_price 
FROM products;

-- Analysis 3: High-Value Products (>50,000)
SELECT name, price, rating 
FROM products 
WHERE price > 50000 
ORDER BY price DESC;

-- Analysis 4: Top Rated Products
SELECT name, rating, price 
FROM products 
WHERE rating >= 4.5 
ORDER BY rating DESC, price ASC
LIMIT 10;

-- Analysis 5: Price Range Distribution
SELECT 
    CASE 
        WHEN price < 30000 THEN 'Budget (<30k)'
        WHEN price BETWEEN 30000 AND 80000 THEN 'Mid-Range (30k-80k)'
        WHEN price BETWEEN 80000 AND 150000 THEN 'Premium (80k-150k)'
        ELSE 'Luxury (>150k)'
    END as price_category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    AVG(rating) as avg_rating
FROM products
GROUP BY price_category
ORDER BY avg_price;

-- Analysis 6: Rating Distribution
SELECT 
    CASE 
        WHEN rating >= 4.5 THEN 'Excellent (4.5+)'
        WHEN rating >= 4.0 THEN 'Good (4.0-4.5)'
        WHEN rating >= 3.5 THEN 'Average (3.5-4.0)'
        ELSE 'Below Average (<3.5)'
    END as rating_category,
    COUNT(*) as count,
    AVG(price) as avg_price
FROM products
GROUP BY rating_category
ORDER BY avg_price DESC;

-- Analysis 7: Price per Rating Point (Value Analysis)
SELECT 
    name,
    price,
    rating,
    ROUND(price / rating, 2) as price_per_rating_point
FROM products
WHERE rating > 0
ORDER BY price_per_rating_point ASC
LIMIT 10;

-- Analysis 8: Products Added Recently (Last 7 days)
SELECT 
    DATE(created_at) as date,
    COUNT(*) as products_added
FROM products
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Analysis 9: Find Best Value Products (High Rating, Reasonable Price)
SELECT 
    name,
    price,
    rating,
    ROUND((rating / price) * 100000, 2) as value_score
FROM products
WHERE rating >= 4.0
ORDER BY value_score DESC
LIMIT 10;

-- Analysis 10: Products by Price Quartiles
SELECT 
    CASE 
        WHEN price <= (SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) FROM products) 
            THEN 'Q1 (Bottom 25%)'
        WHEN price <= (SELECT PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) FROM products) 
            THEN 'Q2 (25-50%)'
        WHEN price <= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) FROM products) 
            THEN 'Q3 (50-75%)'
        ELSE 'Q4 (Top 25%)'
    END as quartile,
    COUNT(*) as count
FROM products
GROUP BY quartile;

-- =====================================================
-- OPTIMIZATION QUERIES
-- =====================================================

-- Show index usage
SHOW INDEX FROM products;

-- Explain query execution plan
EXPLAIN SELECT * FROM products WHERE price > 50000;

-- =====================================================
-- DATA MAINTENANCE
-- =====================================================

-- Remove duplicates (keep first occurrence)
DELETE p1 FROM products p1
INNER JOIN products p2 
WHERE p1.id > p2.id AND p1.name = p2.name;

-- Clean invalid data
DELETE FROM products WHERE price <= 0 OR rating < 0 OR rating > 5;

-- Update missing ratings to 0
UPDATE products SET rating = 0 WHERE rating IS NULL;

-- =====================================================
-- BACKUP AND EXPORT
-- =====================================================

-- Export data to CSV (run from command line)
-- mysqldump -u root -p scraping_db products > products_backup.sql

-- Select all data for export
SELECT * FROM products ORDER BY created_at DESC;

-- =====================================================
-- DROP TABLES (Use with caution!)
-- =====================================================

-- DROP TABLE IF EXISTS products;
-- DROP DATABASE IF EXISTS scraping_db;
