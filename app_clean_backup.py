"""
Web Data Extraction - Professional Analytics Platform
Enterprise-grade data analytics and visualization dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from config import DB_CONFIG
from scraper import WebScraper
import time
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    /* Main theme */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Metric cards */
    .stMetric {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2563eb;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1f2937;
    }
    
    /* Professional cards */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin-bottom: 1rem;
    }
    
    /* Remove default streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styling */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@st.cache_data(ttl=60)
def load_data():
    """Load data from MySQL database"""
    try:
        conn = get_connection()
        query = "SELECT * FROM products ORDER BY created_at DESC"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

def get_statistics():
    """Get analytics statistics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total products
        cursor.execute("SELECT COUNT(*) FROM products")
        stats['total'] = cursor.fetchone()[0]
        
        # Average price
        cursor.execute("SELECT AVG(price) FROM products")
        stats['avg_price'] = cursor.fetchone()[0] or 0
        
        # Highest price
        cursor.execute("SELECT MAX(price) FROM products")
        stats['max_price'] = cursor.fetchone()[0] or 0
        
        # Average rating
        cursor.execute("SELECT AVG(rating) FROM products")
        stats['avg_rating'] = cursor.fetchone()[0] or 0
        
        # Top rated count
        cursor.execute("SELECT COUNT(*) FROM products WHERE rating >= 4.5")
        stats['top_rated'] = cursor.fetchone()[0]
        
        cursor.close()
        return stats
    except Exception as e:
        st.error(f"Error getting statistics: {e}")
        return {}

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 2rem;'>Data Platform</h2>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "Data Explorer", "Scraping Tool", "Analytics", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("<h3 style='color: white; font-size: 1rem;'>Quick Overview</h3>", unsafe_allow_html=True)
    stats = get_statistics()
    if stats:
        st.metric("Total Records", f"{stats.get('total', 0):,}")
        st.metric("Average Price", f"£{stats.get('avg_price', 0):.2f}")
        st.metric("Avg Rating", f"{stats.get('avg_rating', 0):.2f}/5.0")
    
    st.markdown("---")
    st.markdown("<p style='color: #9ca3af; font-size: 0.85rem; text-align: center;'>v1.0.0 | Enterprise Edition</p>", unsafe_allow_html=True)

# Main content
if page == "Dashboard":
        stats['total'] = cursor.fetchone()[0]
        
        # Average price
        cursor.execute("SELECT AVG(price) FROM products")
        stats['avg_price'] = cursor.fetchone()[0] or 0
        
        # Highest price
        cursor.execute("SELECT MAX(price) FROM products")
        stats['max_price'] = cursor.fetchone()[0] or 0
        
        # Average rating
        cursor.execute("SELECT AVG(rating) FROM products")
        stats['avg_rating'] = cursor.fetchone()[0] or 0
        
        # Top rated count
        cursor.execute("SELECT COUNT(*) FROM products WHERE rating >= 4.5")
        stats['top_rated'] = cursor.fetchone()[0]
        
        cursor.close()
        return stats
    except Exception as e:
        st.error(f"Error getting statistics: {e}")
        return {}

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/web-scraper.png", width=100)
    st.title("🌐 Web Scraper")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "📋 Data View", "🚀 Scrape Data", "📈 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.info("💡 **Tip**: Use the scraper to collect fresh data from websites!")
    
    # Quick stats in sidebar
    st.markdown("### Quick Stats")
    stats = get_statistics()
    if stats:
        st.metric("Total Products", stats.get('total', 0))
        st.metric("Avg Price", f"£{stats.get('avg_price', 0):.2f}")

# Main conteDashboard":
    # Header
    st.markdown('<h1 class="main-header">Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time insights and performance metrics</p>', unsafe_allow_html=True)
    
    # Key Performance Indicators
    stats = get_statistics()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Records",
            value=f"{stats.get('total', 0):,}",
            delta="Active"
        )
    
    with col2:
        st.metric(
            label="Average Price",
            value=f"£{stats.get('avg_price', 0):.2f}",
            delta=f"+£{stats.get('max_price', 0) - stats.get('avg_price', 0):.2f}"
        )
    
    with col3:
        st.metric(
            label="Quality Score",
            value=f"{stats.get('avg_rating', 0):.2f}/5.0",
            delta=f"{((stats.get('avg_rating', 0)/5.0)*100):.1f}%"
        )
    
    with col4:
        percentage = (stats.get('top_rated', 0) / stats.get('total', 1)) * 100 if stats.get('total', 0) > 0 else 0
        st.metric(
            label="Premium Products",
            value=f"{stats.get('top_rated', 0):,}",
            delta=f"{percentage:.1f}%:.1f}%",
            delta="Top Products"
        )
    
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if not df.empty:
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💵 Price Distribution")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Price Distribution Analysis")
            fig_price = go.Figure()
            fig_price.add_trace(go.Histogram(
                x=df['price'],
                nbinsx=25,
                marker_color='#2563eb',
                marker_line_color='white',
                marker_line_width=1.5,
                name='Price Distribution',
                opacity=0.85
            ))
            fig_price.update_layout(
                showlegend=False,
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title='Price (£)',
                yaxis_title='Frequency',
                font=dict(family="Arial, sans-serif", size=12, color='#1a1a1a'),
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
            )
            st.plotly_chart(fig_price, use_container_width=True)
        
        with col2:
            st.markdown("### Rating Distribution")
            rating_counts = df['rating'].value_counts().sort_index()
            fig_rating = go.Figure()
            fig_rating.add_trace(go.Bar(
                x=rating_counts.index,
                y=rating_counts.values,
                marker_color='#10b981',
                marker_line_color='white',
                marker_line_width=1.5,
                text=rating_counts.values,
               markdown("### Price Segmentation")
            df['price_category'] = pd.cut(
                df['price'], 
                bins=[0, 20, 40, 60, float('inf')],
                labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
            )
            category_counts = df['price_category'].value_counts()
            
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            fig_pie = go.Figure(data=[go.Pie(
                labels=category_counts.index,
                values=category_counts.values,
                hole=0.5,
                marker=dict(colors=colors, line=dict(color='white', width=2)),
                textinfo='label+percent',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial, sans-serif", size=12, color='#1a1a1a'),
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=True,
                legend Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Top Performing Products")
        
        top_products = df.nlargest(10, 'price')[['name', 'price', 'rating', 'created_at']].copy()
        top_products['Price'] = top_products['price'].apply(lambda x: f"£{x:.2f}")
        top_products['Rating'] = top_products['rating'].apply(lambda x: f"{x:.1f}")
        top_products['Added'] = pd.to_datetime(top_products['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        display_top = top_products[['name', 'Price', 'Rating', 'Added']]
        display_top.columns = ['Product Name', 'Price', 'Rating', 'Date Added']
        Data Explorer":
    st.markdown('<h1 class="main-header">Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Search, filter, and export product data</p>', unsafe_allow_html=True
            display_top, 
            use_container_width=True, 
            hide_index=True,
            height=400
        )
        
    else:
        st.warning("No data available. Please use the Scraping Tool to collect data.
            
            fig_scatter = go.Figure()
            
            # Scatter points
            fig_scatter.add_trace(go.Scatter(
                x=df['price'],
                y=df['rating'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df['rating'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Rating"),
                    line=dict(width=1, color='white')
                ),
                text=df['name'],
                hovertemplate='<b>%{text}</b><br>Price: £%{x:.2f}<br>Rating: %{y}/5.0<extra></extra>',
                name='Products'
            ))
            
            # Trend line
            fig_scatter.add_trace(go.Scatter(
                x=df['price'],
                y=p(df['price']),
                mode='lines',
                line=dict(color='#ef4444', width=2, dash='dash'),
                name='Trend Line',
                hoverinfo='skip'
            ))
            
            fig_scatter.update_layout(
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title='Price (Search Products", "", placeholder="Enter product name...
                yaxis_title='Rating',
                font=dict(family="Arial, sans-serif", size=12, color='#1a1a1a'),
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                showlegend=False
            )
            st.plotly_chart(fig_scatter
        with col2:
            st.subheader("🏷️ Price Categories")
            df['price_category'] = pd.cut(
                df['price'], 
                bins=[0, 20, 40, 60, float('inf')],
                labels=['Budget (<£20)', 'Mid-Range (£20-40)', 'Premium (£40-60)', 'Luxury (>£60)']
            )
            category_counts = df['price_category'].value_counts()
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Top Products
        st.markdown("---")
        st.subheader("🏆 Top 10 Products by Price")
        top_products = df.nlargest(10, 'price')[['name', 'price', 'rating', 'created_at']]
        top_products['price'] = top_products['price'].apply(lambda x: f"£{x:.2f}")
        top_products['rating'] = top_products['rating'].apply(lambda x: f"{x}/5.0")
        st.dataframe(top_products, use_container_width=True, hide_index=True)
        
    else:
        st.warning("⚠️ No data available. Please scrape some data first!")

elif page == "📋 Data View":
    st.title("📋 Product Data View")
    
    df = load_data()
    
    if not df.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price_range = st.slider(
                "💰 Price Range (£)",
                float(df['price'].min()),
                float(df['price'].max()),
                (float(df['price'].min()), float(df['price'].max()))
            )
        
        with col2:
            rating_filter = st.multiselect(
                "⭐ Rating",
                options=sorted(df['rating'].unique()),
                default=sorted(df['rating'].unique())
            )
        
        with col3:
            search = st.text_input("🔍 Search Products", "")
        
        # Apply filters
        filtered_df = df[
            (df['priPrice'] = display_df['price'].apply(lambda x: f"£{x:.2f}")
        display_df['Rating'] = display_df['rating'].apply(lambda x: f"{x:.1f}/5.0")
        display_df['Date'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        final_display = display_df[['name', 'Price', 'Rating', 'Date']]
        final_display.columns = ['Product Name', 'Price', 'Rating', 'Date Added']
        
        st.dataframe(
            final_display,
            use_container_width=True,
            hide_index=True,
            height=500ay_df['price'] = display_df['price'].apply(lambda x: f"£{x:.2f}")
        display_df['rating'] = display_df['rating'].apply(lambda x: f"⭐ {x}/5.0")
        
        st.dataframe(
            display_df,
           markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.download_button(
                label="Download CSV",
                data=filtered_df.to_csv(index=False),
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )Scraping Tool":
    st.markdown('<h1 class="main-header">Data Collection Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Configure and execute web scraping operations</p>', unsafe_allow_html=True st.download_button(
            label="📥 Download as CSV",
            data=filtered_df.to_csv(index=False),
            file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No data available.")

elif page == "🚀 Scrape Data":
    st.title("🚀 Web Scraper")
    
    st.markdown("""
    ### Configure and run web scraping
    Extract product data from websites in real-time.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input(
            "Target URL",
            value="http://books.toscrape.com/catalogue/page-1.html",
            placeholder="https://example.com",
            help="Enter the website URL to scrape"
        )
    
    with col2:
        st.write("")
        st.write("")
        scrape_button = st.button("Start Scraping", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    if scrape_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize scraper
            status_text.text("Initializing scraper...")
            progress_bar.progress(10)
            scraper = WebScraper(url)
            
            # Scrape data
            status_text.text("Loading website with Selenium...")
            progress_bar.progress(30)
            scraper.scrape_data()
            
            # Clean data
            status_text.text("Processing and validating data...")
            progress_bar.progress(60)
            scraper.clean_data()
            
            # Store in database
            status_text.text("Storing in database...")
            progress_bar.progress(80)
            success = scraper.store_in_database()
            
            progress_bar.progress(100)
            status_text.text("Operation completed successfully")
            
            if success:
                st.success(f"Successfully extracted {len(scraper.cleaned_data)} records")
                
                # Show preview
                st.markdown("### Data Preview")
                preview_df = pd.DataFrame(scraper.cleaned_data[:10])
                preview_df['Price'] = preview_df['price'].apply(lambda x: f"£{x:.2f}")
                preview_df['Rating'] = preview_df['rating'].apply(lambda x: f"{x:.1f}/5.0")
                display_preview = preview_df[['name', 'Price', 'Rating']]
                display_preview.columns = ['Product Name', 'Price', 'Rating']
                st.dataframe(display_preview, use_container_width=True, hide_index=True)
                
                # Refresh data cache
                st.cache_data.clear()
                
                st.info("Navigate to Dashboard to view analytics")
            else:
                st.error("Failed to store data in database")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            prAnalytics":
    st.markdown('<h1 class="main-header">Advanced Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">In-depth statistical analysis and insights</p>', unsafe_allow_html=True
elif page == "📈 Analytics":
    st.title("📈 Advanced Analytics")
    
    df = load_data()Statistical Overview", "Trend Analysis", "Market Insights
    
    if not df.emarkdown("###
        tab1, tab2, tab3 = st.tabs(["📊 Statistical Analysis", "💹 Trends", "🔍 Deep Dive"])
        
        with tab1:
            st.subheader("📊 Statistical Summary")
            # Price Statistics")
                price_stats = df['price'].describe()
                stats_df = pd.DataFrame({
                    'Metric': ['Count', 'Mean', 'Std Dev', 'Min', 'Q1 (25%)', 'Median', 'Q3 (75%)', 'Max'],
                    'Value': [f"£{v:.2f}" for v in price_stats.values]
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True, height=320)
            
            with col2:
                st.markdown("#### Rating Statistics")
                rating_stats = df['rating'].describe()
                rating_df = pd.DataFrame({
                    'Metric': ['Count', 'Mean', 'Std Dev', 'Min', 'Q1 (25%)', 'Median', 'Q3 (75%)', 'Max'],
                    'Value': [f"{v:.2f}" for v in rating_stats.values]
                })
                st.dataframe(rating_df, use_container_width=True, hide_index=True, height=320)
            
            # Correlation
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Correlation Analysis")
            correlation = df['price'].corr(df['rating'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Correlation Coefficient", f"{correlation:.4f}")
            with col2:
                st.metric("R² Score", f"{correlation**2:.4f}")
            with col3:
                strength = "Strong" if abs(correlation) > 0.5 else "Moderate" if abs(correlation) > 0.3 else "Weak"
                st.metric("Relationship", strength)
            
            if correlation > 0.3:
                st.success("Positive correlation detected: Higher prices tend to have better ratings")
            elif correlation < -0.3:
               markdown("###gative correlation detected: Higher prices tend to have lower ratings")
            else:
                st.info("Weak correlation: Price and rating are largely independentbetter ratings")
            elif correlation < -0.5:
                st.error("📉 Strong negative c.agg({
                    'price': ['mean', 'min', 'max'],
                    'id': 'count'
                }).reset_index()
                daily_avg.columns = ['date', 'avg_price', 'min_price', 'max_price', 'count']
                
                # Price trend chart
                fig_trend = go.Figure()
                
                fig_trend.add_trace(go.Scatter(
                    x=daily_avg['date'],
                    y=daily_avg['avg_price'],
                    mode='lines+markers',
                    name='Average Price',
                    line=dict(color='#2563eb', width=3),
                    marker=dict(size=8)
                ))
                
                fig_trend.add_trace(go.Scatter(
                    x=daily_avg['date'],
               markdown("### Market Insights")
            
            # Value Analysis
            st.markdown("#### Best Value Products")
            df['value_score'] = (df['rating'] / df['price']) * 100
            best_value = df.nlargest(10, 'value_score')[['name', 'price', 'rating', 'value_score']].copy()
            best_value['Price'] = best_value['price'].apply(lambda x: f"£{x:.2f}")
            best_value['Rating'] = best_value['rating'].apply(lambda x: f"{x:.1f}/5.0")
            best_value['Value Score'] = best_value['value_score'].apply(lambda x: f"{x:.2f}")
            display_value = best_value[['name', 'Price', 'Rating', 'Value Score']]
            display_value.columns = ['Product Name', 'Price', 'Rating', 'Value Score']
            st.dataframe(display_value, use_container_width=True, hide_index=True, height=400)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Price outliers
            st.markdown("#### Price Anomaly Detection")
            q1 = df['price'].quantile(0.25)
            q3 = df['price'].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df['price'] < q1 - 1.5 * iqr) | (df['price'] > q3 + 1.5 * iqr)]
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Outliers Detected", len(outliers))
                st.metric("Q1 (25%)", f"£{q1:.2f}")
                st.metric("Q3 (75%)", f"£{q3:.2f}")
                st.metric("IQR", f"£{iqr:.2f}")
            Settings":
    st.markdown('<h1 class="main-header">System Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Database management and configuration</p>', unsafe_allow_html=True
                if not outliers.empty:
                    oDatabase Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear All Data", type="secondary", use_container_width=True):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE products")
                conn.commit()
                cursor.close()
                st.success("Database cleared successfully")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("Refresh Cache", type="secondary", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache refreshed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Database info
    st.markdown("### Database Information")
    stats = get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{stats.get('total', 0):,}")
    with col2:
        st.metric("Database", DB_CONFIG['database'])
    with col3:
        st.metric("Host", DB_CONFIG['host'])
    with col4:
        st.metric("User", DB_CONFIG['user'])
    
    # Configuration
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### System Configuration")
    
    with st.expander("View Configuration Details"):
        st.code(f"""
Database Configuration:
    Host: {DB_CONFIG['host']}
    User: {DB_CONFIG['user']}
    Database: {DB_CONFIG['database']}
    Connection: Active

Scraper Settings:
    Wait Time: 5 seconds
    Headless Mode: Enabled
    User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
    <br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9ca3af; font-size: 0.875rem;'>
    <p>Web Data Extraction & Analysis Platform | Enterprise Analytics Dashboard</p>
    <p>Built with Python, Streamlit, MySQL & Plotly | Professionalt Value Products (High Rating / Low Price)")
            df['value_score'] = (df['rating'] / df['price']) * 100
            best_value = df.nlargest(10, 'value_score')[['name', 'price', 'rating', 'value_score']]
            best_value['price'] = best_value['price'].apply(lambda x: f"£{x:.2f}")
            best_value['rating'] = best_value['rating'].apply(lambda x: f"{x}/5.0")
            best_value['value_score'] = best_value['value_score'].apply(lambda x: f"{x:.2f}")
            st.dataframe(best_value, use_container_width=True, hide_index=True)
            
            # Price outliers
            st.markdown("### 🚨 Price Outliers")
            q1 = df['price'].quantile(0.25)
            q3 = df['price'].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df['price'] < q1 - 1.5 * iqr) | (df['price'] > q3 + 1.5 * iqr)]
            
            if not outliers.empty:
                st.info(f"Found {len(outliers)} price outliers")
                outliers_display = outliers[['name', 'price', 'rating']]
                outliers_display['price'] = outliers_display['price'].apply(lambda x: f"£{x:.2f}")
                st.dataframe(outliers_display, use_container_width=True, hide_index=True)
            else:
                st.success("✅ No price outliers detected")
    else:
        st.warning("⚠️ No data available for analysis")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings & Database Management")
    
    st.markdown("### 🗄️ Database Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE products")
                conn.commit()
                cursor.close()
                st.success("✅ Database cleared successfully!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("🔄 Refresh Cache", type="secondary", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Cache refreshed!")
    
    st.markdown("---")
    
    # Database info
    st.markdown("### 📊 Database Information")
    stats = get_statistics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", stats.get('total', 0))
    with col2:
        st.metric("Database", DB_CONFIG['database'])
    with col3:
        st.metric("Host", DB_CONFIG['host'])
    
    # Configuration
    st.markdown("---")
    st.markdown("### ⚙️ Scraper Configuration")
    
    with st.expander("View Current Configuration"):
        st.code(f"""
Database Configuration:
    Host: {DB_CONFIG['host']}
    User: {DB_CONFIG['user']}
    Database: {DB_CONFIG['database']}

Scraper Settings:
    Wait Time: 5 seconds
    Headless Mode: True
    User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
        """, language="yaml")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌐 Web Data Extraction & Analysis Dashboard | Built with Streamlit</p>
    <p>💡 Interview-Ready Project | Data Engineering Portfolio</p>
</div>
""", unsafe_allow_html=True)
