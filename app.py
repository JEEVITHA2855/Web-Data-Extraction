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
    /* Main content area */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Headers */
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
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1f2937;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #9ca3af;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #d1d5db !important;
    }
    
    /* Metric cards */
    .stMetric {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2563eb;
    }
    
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6c757d !important;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #059669 !important;
    }
    
    /* Tables */
    [data-testid="stDataFrame"] {
        background-color: white;
    }
    
    .dataframe {
        color: #1a1a1a !important;
    }
    
    .dataframe thead th {
        background-color: #f3f4f6 !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    .dataframe tbody td {
        color: #374151 !important;
    }
    
    /* Text inputs and filters */
    .stTextInput label,
    .stSlider label,
    .stMultiSelect label {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    .stTextInput input {
        color: #1a1a1a !important;
        background-color: white !important;
    }
    
    /* Section headers in main area */
    .main h3 {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        margin-bottom: 1rem;
    }
    
    .main h4 {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background-color: white !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Buttons */
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
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #2563eb;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #6c757d;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #2563eb;
        border-bottom-color: #2563eb;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #059669;
        color: white;
    }
    
    .stDownloadButton>button:hover {
        background-color: #047857;
    }
</style>
""", unsafe_allow_html=True)

# Database connection
def get_connection():
    """Create a fresh MySQL connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        st.error(f"⚠️ Database connection failed: {e}")
        return None

@st.cache_data(ttl=60)
def load_data():
    """Load data from MySQL database"""
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()
        
        query = "SELECT * FROM products ORDER BY created_at DESC"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def get_statistics():
    """Get analytics statistics"""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return {}
        
        cursor = conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM products")
        stats['total'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(price) FROM products")
        stats['avg_price'] = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT MAX(price) FROM products")
        stats['max_price'] = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(rating) FROM products")
        stats['avg_rating'] = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM products WHERE rating >= 4.5")
        stats['top_rated'] = cursor.fetchone()[0]
        
        cursor.close()
        return stats
    except:
        return {}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 2rem;'>Data Platform</h2>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "Data Explorer", "Scraping Tool", "Analytics", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
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
    st.markdown('<h1 class="main-header">Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time insights and performance metrics</p>', unsafe_allow_html=True)
    
    stats = get_statistics()
    df = load_data()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", f"{stats.get('total', 0):,}")
    
    with col2:
        st.metric("Average Price", f"£{stats.get('avg_price', 0):.2f}")
    
    with col3:
        st.metric("Quality Score", f"{stats.get('avg_rating', 0):.2f}/5.0")
    
    with col4:
        percentage = (stats.get('top_rated', 0) / max(stats.get('total', 1), 1)) * 100
        st.metric("Premium Products", f"{stats.get('top_rated', 0):,}", f"{percentage:.1f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Interactive Price Categories")
            
            # Create price categories
            df['price_category'] = pd.cut(
                df['price'], 
                bins=[0, 20, 40, 60, float('inf')],
                labels=['Budget (£0-20)', 'Mid-Range (£20-40)', 'Premium (£40-60)', 'Luxury (£60+)']
            )
            category_counts = df['price_category'].value_counts()
            
            # Calculate detailed stats for hover
            category_stats = df.groupby('price_category', observed=True).agg({
                'price': ['mean', 'min', 'max', 'count'],
                'rating': 'mean'
            }).round(2)
            
            # Beautiful gradient colors
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            
            # Create custom hover text and pull values
            hover_texts = []
            pull_values = []
            
            for cat in category_counts.index:
                if cat in category_stats.index:
                    stats_row = category_stats.loc[cat]
                    count = int(stats_row[('price', 'count')])
                    avg_price = stats_row[('price', 'mean')]
                    min_price = stats_row[('price', 'min')]
                    max_price = stats_row[('price', 'max')]
                    avg_rating = stats_row[('rating', 'mean')]
                    
                    hover_text = f"<b style='font-size:16px'>{cat}</b><br><br>"
                    hover_text += f"<b>Products:</b> {count}<br>"
                    hover_text += f"<b>Avg Price:</b> £{avg_price:.2f}<br>"
                    hover_text += f"<b>Range:</b> £{min_price:.2f} - £{max_price:.2f}<br>"
                    hover_text += f"<b>Avg Rating:</b> {avg_rating:.1f} ⭐<br>"
                    hover_text += f"<b>Share:</b> {(count/len(df)*100):.1f}%"
                    
                    hover_texts.append(hover_text)
                    pull_values.append(0.1 if count == category_counts.max() else 0.05)
            
            # Create impressive pie chart
            fig_pie = go.Figure()
            
            fig_pie.add_trace(go.Pie(
                labels=category_counts.index,
                values=category_counts.values,
                hole=0.4,
                marker=dict(
                    colors=colors[:len(category_counts)],
                    line=dict(color='white', width=4)
                ),
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Arial Black'),
                hovertext=hover_texts,
                hoverinfo='text',
                pull=pull_values,
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=13,
                    font_family="Arial",
                    bordercolor="#e5e7eb"
                ),
                insidetextorientation='radial'
            ))
            
            fig_pie.update_layout(
                height=450,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial", size=12, color='#1a1a1a'),
                margin=dict(l=20, r=20, t=60, b=20),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#cbd5e1",
                    borderwidth=2,
                    font=dict(size=12)
                ),
                annotations=[
                    dict(
                        text=f'<b>{len(df)}</b><br>Products',
                        x=0.5, y=0.5,
                        font_size=20,
                        showarrow=False,
                        font_color='#1a1a1a'
                    )
                ]
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            st.caption("💡 Hover over segments to see them bulge out with detailed statistics!")
        
        with col2:
            st.markdown("### 📈 Price Distribution")
            
            fig_hist = go.Figure()
            
            fig_hist.add_trace(go.Histogram(
                x=df['price'],
                nbinsx=20,
                marker_color='#3b82f6',
                marker_line_color='white',
                marker_line_width=2,
                opacity=0.8,
                hovertemplate='Price: £%{x:.2f}<br>Count: %{y}<extra></extra>'
            ))
            
            mean_price = df['price'].mean()
            median_price = df['price'].median()
            
            fig_hist.add_vline(
                x=mean_price,
                line_dash="dash",
                line_color="#10b981",
                line_width=3,
                annotation_text=f"Mean: £{mean_price:.2f}",
                annotation_position="top right"
            )
            
            fig_hist.add_vline(
                x=median_price,
                line_dash="dot",
                line_color="#f59e0b",
                line_width=3,
                annotation_text=f"Median: £{median_price:.2f}",
                annotation_position="bottom right"
            )
            
            fig_hist.update_layout(
                showlegend=False,
                height=450,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title='Price (£)',
                yaxis_title='Number of Products',
                font=dict(family="Arial", size=12, color='#1a1a1a'),
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                hovermode='x'
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⭐ Rating Distribution")
            
            rating_counts = df['rating'].value_counts().sort_index()
            colors_map = {1: '#ef4444', 2: '#f59e0b', 3: '#fbbf24', 4: '#84cc16', 5: '#10b981'}
            rating_colors = [colors_map.get(r, '#9ca3af') for r in rating_counts.index]
            
            fig_rating = go.Figure()
            
            fig_rating.add_trace(go.Bar(
                x=rating_counts.index,
                y=rating_counts.values,
                marker_color=rating_colors,
                marker_line_color='white',
                marker_line_width=2,
                text=rating_counts.values,
                textposition='outside',
                textfont=dict(size=13, color='#1a1a1a'),
                hovertemplate='<b>%{x} Stars</b><br>Products: %{y}<extra></extra>'
            ))
            
            fig_rating.update_layout(
                showlegend=False,
                height=450,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title='Rating (Stars)',
                yaxis_title='Number of Products',
                font=dict(family="Arial", size=12, color='#1a1a1a'),
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                bargap=0.15
            )
            
            st.plotly_chart(fig_rating, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 Price vs Rating Correlation")
            
            fig_scatter = go.Figure()
            
            fig_scatter.add_trace(go.Scatter(
                x=df['price'],
                y=df['rating'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=df['rating'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Rating"),
                    line=dict(width=2, color='white'),
                    opacity=0.7
                ),
                text=df['name'],
                hovertemplate='<b>%{text}</b><br>Price: £%{x:.2f}<br>Rating: %{y}/5.0<extra></extra>'
            ))
            
            # Add trend line
            z = np.polyfit(df['price'], df['rating'], 1)
            p = np.poly1d(z)
            fig_scatter.add_trace(go.Scatter(
                x=df['price'],
                y=p(df['price']),
                mode='lines',
                line=dict(color='#ef4444', width=3, dash='dash'),
                name='Trend',
                hoverinfo='skip'
            ))
            
            fig_scatter.update_layout(
                showlegend=False,
                height=450,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title='Price (£)',
                yaxis_title='Rating (Stars)',
                font=dict(family="Arial", size=12, color='#1a1a1a'),
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                hovermode='closest'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    else:
        st.warning("⚠️ No data available. Please scrape some products first!")

elif page == "Data Explorer":
    st.markdown('<h1 class="main-header">Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Search, filter, and export product data</p>', unsafe_allow_html=True)
    
    df = load_data()
    if not df.empty:
        # ...existing code for dashboard visualizations...
        pass
    else:
        st.info("No data available.")

elif page == "Scraping Tool":
    st.markdown('<h1 class="main-header">Data Collection Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Configure and execute web scraping operations</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        url = st.text_input(
            "Target URL",
            value="http://books.toscrape.com/catalogue/page-1.html",
            placeholder="https://example.com",
            help="Enter the website URL to scrape"
        )
    
    with col2:
        max_pages = st.number_input(
            "Pages to Scrape",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of pages to scrape (more pages = more data)"
        )
    
    with col3:
        st.write("")
        st.write("")
        scrape_button = st.button("Start Scraping", type="primary", use_container_width=True)
    
    st.info(f"📊 Will collect approximately {max_pages * 20} products ({max_pages} pages × ~20 products/page)")
    st.markdown("---")
    
    if scrape_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Initializing scraper...")
            progress_bar.progress(10)
            scraper = WebScraper(url, max_pages=max_pages)
            
            status_text.text(f"Loading {max_pages} page(s) with Selenium...")
            progress_bar.progress(30)
            scraper.scrape_data()
            
            status_text.text("Processing and validating data...")
            progress_bar.progress(60)
            scraper.clean_data()
            
            status_text.text("Storing in database...")
            progress_bar.progress(80)
            success = scraper.store_in_database()
            
            progress_bar.progress(100)
            status_text.text("Operation completed successfully")
            
            if success:
                st.success(f"Successfully extracted {len(scraper.cleaned_data)} records")
                
                st.markdown("### Data Preview")
                preview_df = pd.DataFrame(scraper.cleaned_data[:10])
                preview_df['Price'] = preview_df['price'].apply(lambda x: f"£{x:.2f}")
                preview_df['Rating'] = preview_df['rating'].apply(lambda x: f"{x:.1f}/5.0")
                display_preview = preview_df[['name', 'Price', 'Rating']]
                display_preview.columns = ['Product Name', 'Price', 'Rating']
                st.dataframe(display_preview, use_container_width=True, hide_index=True)
                
                st.cache_data.clear()
                st.info("Navigate to Dashboard to view analytics")
            else:
                st.error("Failed to store data in database")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            progress_bar.empty()

elif page == "Analytics":
    st.markdown('<h1 class="main-header">Advanced Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">In-depth statistical analysis and insights</p>', unsafe_allow_html=True)
    
    df = load_data()
    
    if not df.empty:
        tab1, tab2 = st.tabs(["Statistical Overview", "Market Insights"])
        
        with tab1:
            st.markdown("### Statistical Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Price Statistics")
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
        
        with tab2:
            st.markdown("### Best Value Products")
            df['value_score'] = (df['rating'] / df['price']) * 100
            best_value = df.nlargest(10, 'value_score')[['name', 'price', 'rating', 'value_score']].copy()
            best_value['Price'] = best_value['price'].apply(lambda x: f"£{x:.2f}")
            best_value['Rating'] = best_value['rating'].apply(lambda x: f"{x:.1f}/5.0")
            best_value['Value Score'] = best_value['value_score'].apply(lambda x: f"{x:.2f}")
            display_value = best_value[['name', 'Price', 'Rating', 'Value Score']]
            display_value.columns = ['Product Name', 'Price', 'Rating', 'Value Score']
            st.dataframe(display_value, use_container_width=True, hide_index=True, height=400)
    else:
        st.info("No data available for analysis")

elif page == "Settings":
    st.markdown('<h1 class="main-header">System Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Database management and configuration</p>', unsafe_allow_html=True)
    
    st.markdown("### Database Operations")
    
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

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9ca3af; font-size: 0.875rem;'>
    <p>Web Data Extraction & Analysis Platform | Enterprise Analytics Dashboard</p>
    <p>Built with Python, Streamlit, MySQL & Plotly | Professional Data Engineering Portfolio</p>
</div>
""", unsafe_allow_html=True)
