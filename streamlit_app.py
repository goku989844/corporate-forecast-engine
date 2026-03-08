"""
Corporate Forecast Engine - Streamlit Web App
Interactive demo for hospitality financial forecasting
"""

import streamlit as st
import pandas as pd
import io
import os
import sys
from datetime import datetime
import tempfile
import shutil

# Page config
st.set_page_config(
    page_title="Corporate Forecast Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Import the forecast engine (will be imported after file is created)
def import_forecast_engine():
    """Import the forecast engine module"""
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import the DEMO version
        from Corp_Forecast_Engine_DEMO import CorpForecastEngine
        return CorpForecastEngine
    except ImportError as e:
        st.error(f"Error importing forecast engine: {e}")
        st.info("Please ensure Corp_Forecast_Engine_DEMO.py is in the same directory as this app.")
        return None

# Header
st.markdown('<div class="main-header">📊 Corporate Forecast Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Financial Forecasting for Hospitality Management Companies</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Forecast+Engine", use_container_width=True)
    
    st.markdown("### 🎯 Quick Start")
    st.markdown("""
    1. **Download** sample data files below
    2. **Upload** your data files (or use samples)
    3. **Configure** forecast parameters
    4. **Generate** your executive forecast
    5. **Download** Excel output
    """)
    
    st.markdown("---")
    
    st.markdown("### 📁 Sample Data Files")
    st.markdown("Download these to see the engine in action:")
    
    # Sample file download buttons (we'll create these)
    sample_files = {
        "Hotel Master Data": "INPUT_Hotel_Master_Data_2026.xlsx",
        "Payroll Data": "INPUT_Payroll_Data_2026.xlsx",
        "Trial Balance 2024": "INPUT_Trial_Balance_CORP_2024.xlsx",
        "Trial Balance 2025": "INPUT_Trial_Balance_CORP_2025.xlsx",
        "Trial Balance 2026": "INPUT_Trial_Balance_CORP_2026.xlsx",
        "Budget Data": "INPUT_Budget_Data_2026.xlsx",
        "Expense Data": "INPUT_Simplified_Expenses_2026.xlsx",
        "Revenue Forecast": "INPUT_Revenue_Forecast_2026.xlsx",
    }
    
    for name, filename in sample_files.items():
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                st.download_button(
                    label=f"📥 {name}",
                    data=f.read(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_{filename}"
                )

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload Data", "⚙️ Configure", "📊 Generate Forecast"])

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}
if 'config' not in st.session_state:
    st.session_state.config = {
        'bonus_2026': 30.0,
        'bonus_2027': 80.0,
        'bonus_2028': 80.0,
    }
if 'forecast_generated' not in st.session_state:
    st.session_state.forecast_generated = False
if 'output_file' not in st.session_state:
    st.session_state.output_file = None

# TAB 1: Upload Data
with tab1:
    st.markdown("## 📤 Upload Your Data Files")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **Required Files:**
    - Hotel Master Data (property details)
    - Payroll Data (employee information)
    - Trial Balance files (2024, 2025, 2026)
    - Budget Data (2026 budget)
    - Expense Data (variable expenses)
    - Revenue Forecast (hotel-level projections)
    
    **Or use the sample data files** available in the sidebar to test the engine!
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Core Data Files")
        
        hotel_file = st.file_uploader("🏨 Hotel Master Data", type=['xlsx'], key='hotel')
        if hotel_file:
            st.session_state.uploaded_files['hotel'] = hotel_file
            st.success(f"✓ Uploaded: {hotel_file.name}")
        
        payroll_file = st.file_uploader("👥 Payroll Data", type=['xlsx'], key='payroll')
        if payroll_file:
            st.session_state.uploaded_files['payroll'] = payroll_file
            st.success(f"✓ Uploaded: {payroll_file.name}")
        
        budget_file = st.file_uploader("💰 Budget Data", type=['xlsx'], key='budget')
        if budget_file:
            st.session_state.uploaded_files['budget'] = budget_file
            st.success(f"✓ Uploaded: {budget_file.name}")
        
        expense_file = st.file_uploader("📋 Expense Data", type=['xlsx'], key='expense')
        if expense_file:
            st.session_state.uploaded_files['expense'] = expense_file
            st.success(f"✓ Uploaded: {expense_file.name}")
    
    with col2:
        st.markdown("### Historical & Forecast Data")
        
        tb_2024 = st.file_uploader("📊 Trial Balance 2024", type=['xlsx'], key='tb2024')
        if tb_2024:
            st.session_state.uploaded_files['tb_2024'] = tb_2024
            st.success(f"✓ Uploaded: {tb_2024.name}")
        
        tb_2025 = st.file_uploader("📊 Trial Balance 2025", type=['xlsx'], key='tb2025')
        if tb_2025:
            st.session_state.uploaded_files['tb_2025'] = tb_2025
            st.success(f"✓ Uploaded: {tb_2025.name}")
        
        tb_2026 = st.file_uploader("📊 Trial Balance 2026", type=['xlsx'], key='tb2026')
        if tb_2026:
            st.session_state.uploaded_files['tb_2026'] = tb_2026
            st.success(f"✓ Uploaded: {tb_2026.name}")
        
        revenue_file = st.file_uploader("💵 Revenue Forecast", type=['xlsx'], key='revenue')
        if revenue_file:
            st.session_state.uploaded_files['revenue'] = revenue_file
            st.success(f"✓ Uploaded: {revenue_file.name}")
    
    # Upload status
    st.markdown("---")
    files_uploaded = len(st.session_state.uploaded_files)
    files_required = 8
    
    progress = files_uploaded / files_required
    st.progress(progress)
    st.markdown(f"**Files Uploaded:** {files_uploaded} / {files_required}")
    
    if files_uploaded == files_required:
        st.markdown('<div class="success-box">✅ All required files uploaded! Move to the Configure tab.</div>', unsafe_allow_html=True)

# TAB 2: Configure
with tab2:
    st.markdown("## ⚙️ Configure Forecast Parameters")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **Bonus Payout Assumptions:**
    Set the expected bonus payout percentage for each forecast year. 
    This affects the Bonus & Incentives (GL 50200) forecast.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 2026 Bonus Payout")
        bonus_2026 = st.slider(
            "Percentage of target",
            min_value=0,
            max_value=100,
            value=int(st.session_state.config['bonus_2026']),
            step=5,
            key='slider_2026'
        )
        st.session_state.config['bonus_2026'] = float(bonus_2026)
        st.info(f"💰 {bonus_2026}% of bonus targets")
    
    with col2:
        st.markdown("### 2027 Bonus Payout")
        bonus_2027 = st.slider(
            "Percentage of target",
            min_value=0,
            max_value=100,
            value=int(st.session_state.config['bonus_2027']),
            step=5,
            key='slider_2027'
        )
        st.session_state.config['bonus_2027'] = float(bonus_2027)
        st.info(f"💰 {bonus_2027}% of bonus targets")
    
    with col3:
        st.markdown("### 2028 Bonus Payout")
        bonus_2028 = st.slider(
            "Percentage of target",
            min_value=0,
            max_value=100,
            value=int(st.session_state.config['bonus_2028']),
            step=5,
            key='slider_2028'
        )
        st.session_state.config['bonus_2028'] = float(bonus_2028)
        st.info(f"💰 {bonus_2028}% of bonus targets")
    
    st.markdown("---")
    
    # Additional configuration options
    st.markdown("### 📝 Additional Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_legal = st.checkbox("Include Legal Expenses (GL 51451)", value=True)
        st.session_state.config['include_legal'] = include_legal
    
    with col2:
        include_depreciation = st.checkbox("Include Depreciation (GL 60100)", value=True)
        st.session_state.config['include_depreciation'] = include_depreciation
    
    st.markdown('<div class="success-box">✅ Configuration saved! Move to Generate Forecast tab.</div>', unsafe_allow_html=True)

# TAB 3: Generate Forecast
with tab3:
    st.markdown("## 📊 Generate Executive Forecast")
    
    # Check if ready to generate
    files_ready = len(st.session_state.uploaded_files) == 8
    
    if not files_ready:
        st.warning("⚠️ Please upload all required data files in the Upload Data tab first.")
    else:
        st.markdown('<div class="success-box">✅ All files uploaded and configuration complete!</div>', unsafe_allow_html=True)
        
        st.markdown("### 🚀 Ready to Generate")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🎯 Generate Executive Forecast", use_container_width=True):
                
                # Create progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Import engine
                    status_text.text("Loading forecast engine...")
                    progress_bar.progress(10)
                    
                    CorpForecastEngine = import_forecast_engine()
                    if not CorpForecastEngine:
                        st.error("Failed to load forecast engine. Please check that Corp_Forecast_Engine_DEMO.py is in the app directory.")
                        st.stop()
                    
                    # Create temporary directory for files
                    with tempfile.TemporaryDirectory() as temp_dir:
                        status_text.text("Preparing data files...")
                        progress_bar.progress(20)
                        
                        # Save uploaded files to temp directory with correct names
                        file_mapping = {
                            'hotel': 'INPUT_Hotel_Master_Data_2026.xlsx',
                            'payroll': 'INPUT_Payroll_Data_2026.xlsx',
                            'tb_2024': 'INPUT_Trial_Balance_CORP_2024.xlsx',
                            'tb_2025': 'INPUT_Trial_Balance_CORP_2025.xlsx',
                            'tb_2026': 'INPUT_Trial_Balance_CORP_2026.xlsx',
                            'budget': 'INPUT_Budget_Data_2026.xlsx',
                            'expense': 'INPUT_Simplified_Expenses_2026.xlsx',
                            'revenue': 'INPUT_Revenue_Forecast_2026.xlsx',
                        }
                        
                        for key, filename in file_mapping.items():
                            if key in st.session_state.uploaded_files:
                                file_path = os.path.join(temp_dir, filename)
                                with open(file_path, 'wb') as f:
                                    f.write(st.session_state.uploaded_files[key].getvalue())
                        
                        # Change to temp directory
                        original_dir = os.getcwd()
                        os.chdir(temp_dir)
                        
                        try:
                            status_text.text("Initializing forecast engine...")
                            progress_bar.progress(30)
                            
                            # Initialize engine
                            engine = CorpForecastEngine()
                            
                            # Set configuration
                            engine.exclude_legal = not st.session_state.config['include_legal']
                            engine.exclude_depreciation = not st.session_state.config['include_depreciation']
                            engine.config['bonus_adjustment'][2026] = st.session_state.config['bonus_2026'] / 100
                            engine.config['bonus_adjustment'][2027] = st.session_state.config['bonus_2027'] / 100
                            engine.config['bonus_adjustment'][2028] = st.session_state.config['bonus_2028'] / 100
                            
                            status_text.text("Loading data files...")
                            progress_bar.progress(40)
                            
                            # Load data
                            file_paths = engine._discover_input_files()
                            
                            if not engine.load_all_data(file_paths):
                                st.error("Failed to load data files. Please check file formats.")
                                st.stop()
                            
                            status_text.text("Generating forecasts...")
                            progress_bar.progress(60)
                            
                            # Generate forecast
                            output_file = engine.export_to_excel()
                            
                            if output_file and os.path.exists(output_file):
                                status_text.text("Finalizing output...")
                                progress_bar.progress(90)
                                
                                # Read the output file
                                with open(output_file, 'rb') as f:
                                    st.session_state.output_file = f.read()
                                
                                st.session_state.forecast_generated = True
                                
                                progress_bar.progress(100)
                                status_text.text("✅ Forecast generation complete!")
                                
                            else:
                                st.error("Failed to generate forecast output.")
                        
                        finally:
                            # Change back to original directory
                            os.chdir(original_dir)
                
                except Exception as e:
                    st.error(f"Error generating forecast: {str(e)}")
                    st.exception(e)
    
    # Show download button if forecast was generated
    if st.session_state.forecast_generated and st.session_state.output_file:
        st.markdown("---")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 🎉 Forecast Generated Successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Corporate_Forecast_Executive_{timestamp}.xlsx"
            
            st.download_button(
                label="📥 Download Executive Forecast",
                data=st.session_state.output_file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("""
        ### 📊 Your Forecast Includes:
        - **Executive Summary** - High-level overview
        - **Executive Scorecard** - One-page KPI dashboard
        - **Growth Analysis** - Portfolio expansion metrics
        - **Risk Dashboard** - Concentration analysis
        - **Current Month P&L** - Latest financial snapshot
        - **YTD P&L** - Year-to-date performance
        - **2026-2027 Forecasts** - Detailed monthly projections
        - **Annual Summary** - Multi-year trends
        - **KPI Dashboard** - Comprehensive metrics
        - **Pipeline Analysis** - Development tracking
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Corporate Forecast Engine v8.0 - DEMO Edition</strong></p>
    <p>AI-Powered Financial Forecasting for Hospitality Management Companies</p>
    <p style='font-size: 0.9rem;'>Built with Python • Streamlit • Pandas • OpenPyXL</p>
</div>
""", unsafe_allow_html=True)
