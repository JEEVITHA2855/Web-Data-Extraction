# 🌐 Web Data Extraction & Analysis Project

> **Interview-Ready Project**: Automated web scraping, data cleaning, MySQL storage, and SQL analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.16.0-green.svg)](https://www.selenium.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [What This Project Demonstrates](#-what-this-project-demonstrates)
- [Technologies Used](#-technologies-used)
- [Architecture & Data Flow](#-architecture--data-flow)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [SQL Analysis Examples](#-sql-analysis-examples)
- [Interview Talking Points](#-interview-talking-points)
- [Future Enhancements](#-future-enhancements)

---

## 🎯 Project Overview

This project demonstrates **end-to-end data engineering skills** by:
1. **Extracting** product data from websites using Selenium & BeautifulSoup
2. **Cleaning** and validating scraped data
3. **Storing** structured data in MySQL database
4. **Analyzing** data using SQL queries
5. **Optimizing** database performance with indexes

**Real-world use case**: E-commerce price monitoring, competitor analysis, market research

---

## 💼 What This Project Demonstrates

| Skill | Implementation |
|-------|----------------|
| **Web Scraping** | Selenium for dynamic content, BeautifulSoup for HTML parsing |
| **Data Engineering** | ETL pipeline (Extract → Transform → Load) |
| **Data Cleaning** | Removing symbols, type conversion, deduplication, validation |
| **Database Design** | Normalized schema, proper indexing, constraints |
| **SQL Proficiency** | Complex queries, aggregations, window functions |
| **Code Quality** | Modular OOP design, error handling, documentation |
| **Version Control** | Git & GitHub repository management |

---

## 🛠️ Technologies Used

```
Python 3.8+          → Core programming language
Selenium 4.16        → Browser automation for dynamic websites
BeautifulSoup4       → HTML parsing and data extraction
MySQL 8.0+           → Relational database for data storage
mysql-connector      → Python-MySQL integration
```

**Why Selenium?**  
*"I used Selenium because the target website loads content dynamically via JavaScript, which static request libraries like `requests` cannot handle."*

**Why BeautifulSoup?**  
*"BeautifulSoup converts raw HTML into structured Python objects, making it easy to navigate the DOM and extract specific elements."*

---

## 🏗️ Architecture & Data Flow

```
┌─────────────────┐
│   Website       │
│  (HTML/JS)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Selenium      │  ← Opens browser, renders JavaScript
│  (Web Driver)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ BeautifulSoup   │  ← Parses HTML, extracts data
│  (HTML Parser)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Cleaning   │  ← Removes symbols, validates, deduplicates
│   (Python)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MySQL Database │  ← Structured storage with indexes
│   (Relational)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQL Analysis   │  ← Business insights & reporting
│   (Queries)     │
└─────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0+
- Google Chrome browser
- ChromeDriver (matching Chrome version)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/Web-Data-Extraction.git
cd Web-Data-Extraction
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Run the schema file
source db.sql
```

### Step 5: Configure Database Connection
Edit `config.py` with your MySQL credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'scraping_db'
}
```

---

## 🚀 Usage

### Run the Complete Pipeline
```bash
python scraper.py
```

### What Happens:
1. ✅ Opens website using Selenium
2. ✅ Extracts product data (name, price, rating)
3. ✅ Cleans and validates data
4. ✅ Stores in MySQL database
5. ✅ Runs automated SQL analysis
6. ✅ Displays insights and statistics

### Expected Output:
```
============================================================
🚀 WEB DATA EXTRACTION & ANALYSIS PROJECT
============================================================
🌐 Opening website with Selenium...
⏳ Waiting for page to load...
✅ Browser closed
🔍 Parsing HTML content...
📦 Extracted 10 items
🧹 Cleaning data...
✅ Cleaned 10 items
✅ Removed duplicates. Final count: 10
💾 Connecting to MySQL database...
✅ Successfully inserted 10 records
📊 Total records in database: 10
🔌 Database connection closed

📊 Running data analysis...

💰 Average Price: ₹92,656.30

🏆 High-Value Products (>₹50,000):
   - Canon EOS R6: ₹2,15,995.00
   - LG OLED TV 55": ₹1,34,990.00
   ...
```

---

## 📁 Project Structure

```
Web-Data-Extraction/
│
├── scraper.py              # Main scraping script (ETL pipeline)
├── config.py               # Database & settings configuration
├── db.sql                  # Database schema & analysis queries
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
└── .git/                  # Version control
```

---

## ⭐ Key Features

### 1. **Robust Data Cleaning**
```python
# Remove currency symbols and commas
price = price.replace('₹', '').replace(',', '').strip()

# Convert to proper types
price = float(price)
rating = float(rating) if rating else 0.0

# Validate data
if name and price > 0:
    cleaned_data.append(...)
```

### 2. **SQL Injection Prevention**
```python
# Parameterized queries
cursor.executemany(
    "INSERT INTO products (name, price) VALUES (%s, %s)",
    data_tuples
)
```

### 3. **Performance Optimization**
```sql
-- Indexes for faster queries
CREATE INDEX idx_price ON products(price);
CREATE INDEX idx_rating ON products(rating);
```

### 4. **Data Quality Checks**
```sql
-- Check for duplicates
SELECT name, COUNT(*) 
FROM products 
GROUP BY name 
HAVING COUNT(*) > 1;

-- Validate price range
SELECT COUNT(*) 
FROM products 
WHERE price <= 0;
```

---

## 📊 SQL Analysis Examples

### Average Price
```sql
SELECT AVG(price) FROM products;
```

### High-Value Products
```sql
SELECT name, price 
FROM products 
WHERE price > 50000 
ORDER BY price DESC;
```

### Price Distribution
```sql
SELECT 
    CASE 
        WHEN price < 30000 THEN 'Budget'
        WHEN price BETWEEN 30000 AND 80000 THEN 'Mid-Range'
        ELSE 'Premium'
    END as category,
    COUNT(*) as count
FROM products
GROUP BY category;
```

### Best Value Products (Rating/Price)
```sql
SELECT 
    name,
    price,
    rating,
    ROUND((rating / price) * 100000, 2) as value_score
FROM products
ORDER BY value_score DESC
LIMIT 10;
```

---

## 🎤 Interview Talking Points

### **Q: Why did you choose Selenium over requests?**
> *"I used Selenium because the target website relies on JavaScript to render product listings dynamically. Static HTTP libraries like `requests` can't execute JavaScript, so Selenium was necessary to load the full DOM before scraping."*

### **Q: How did you ensure data quality?**
> *"I implemented a multi-step validation process:*
> 1. *Removed currency symbols and formatted numbers*
> 2. *Checked for NULL or empty values*
> 3. *Validated price and rating ranges*
> 4. *Removed duplicates using Python sets*
> 5. *Ran SQL queries to verify data integrity"*

### **Q: Why MySQL instead of NoSQL?**
> *"Since product data has a fixed schema (name, price, rating), a relational database was ideal. MySQL provides ACID compliance, supports complex joins, and has excellent indexing for analytical queries."*

### **Q: How did you optimize database performance?**
> *"I created indexes on frequently queried columns (`price`, `rating`) to speed up WHERE and ORDER BY operations. I also used EXPLAIN to analyze query execution plans."*

### **Q: What would you improve in production?**
> *"I would add:*
> - *Rotating user agents to avoid blocking*
> - *Retry logic with exponential backoff*
> - *Async scraping for faster data collection*
> - *Scheduled runs using cron/Airflow*
> - *Data versioning to track price changes over time"*

---

## 🔮 Future Enhancements

- [ ] Add data visualization (Matplotlib/Plotly)
- [ ] Implement incremental scraping (only new products)
- [ ] Add price change tracking (time-series analysis)
- [ ] Deploy as scheduled job (Airflow/Cron)
- [ ] Create REST API for data access (Flask/FastAPI)
- [ ] Add email alerts for price drops
- [ ] Implement multi-threading for faster scraping
- [ ] Add unit tests (pytest)

---

## 📄 License

This project is created for educational and portfolio purposes.

---

## 👤 Author

**Your Name**  
📧 your.email@example.com  
💼 [LinkedIn](https://linkedin.com/in/yourprofile)  
🐙 [GitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **Selenium Documentation** → https://www.selenium.dev/documentation/
- **BeautifulSoup Docs** → https://www.crummy.com/software/BeautifulSoup/
- **MySQL Reference** → https://dev.mysql.com/doc/

---

**⭐ If this project helped you, please star the repository!**

---

*Last Updated: January 2026*
