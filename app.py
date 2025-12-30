
"""
═══════════════════════════════════════════════════════════════════════════════
THE MOUNTAIN PATH - WORLD OF FINANCE
Volatility Forecasting Platform - GARCH & EGARCH Models
Real-time Analysis of Stocks, Indices & Commodities
═══════════════════════════════════════════════════════════════════════════════

Prof. V. Ravichandran
28+ Years Corporate Finance & Banking Experience
10+ Years Academic Excellence
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from arch import arch_model
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT CUSTOM MODULES
# ═══════════════════════════════════════════════════════════════════════════════

from config import PAGE_CONFIG, COLORS, THEME
from styles import apply_main_styles
from components import HeroHeader, SidebarNavigation, MetricsDisplay, TabsDisplay, Footer
from data_fetcher import DataFetcher
from volatility_models import VolatilityModels

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Volatility Forecasting - GARCH & EGARCH",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles from template
apply_main_styles()

# ═══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════════

HeroHeader.render(
    title="THE MOUNTAIN PATH • VOLATILITY FORECASTING",
    subtitle="Advanced GARCH & EGARCH Analysis",
    description="Real-time volatility analysis for Stocks • Indices • Commodities | NIFTY50 • S&P500 • Gold • Silver",
    emoji="📊"
)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("---")
    st.write("### 📊 VOLATILITY FORECASTING")
    st.write("GARCH(1,1) & EGARCH Model Analysis")
    st.markdown("---")
    
    # Asset selection
    col_asset_type = st.columns(1)
    with col_asset_type[0]:
        asset_type = st.selectbox(
            "**Asset Class:**",
            options=["Equity Indices", "Nifty Stocks", "International Indices", "Commodities"],
            help="Choose asset class",
            key="asset_class_selector"
        )
    
    # Asset choice based on class
    if asset_type == "Equity Indices":
        available_assets = ["NIFTY 50 Index", "NIFTY Bank Index", "NIFTY IT Index"]
        symbols = ["^NSEI", "^NSEBANK", "^CNXIT"]
    
    elif asset_type == "Nifty Stocks":
        available_assets = [
            "TCS", "Infosys", "HDFC Bank", "ICICI Bank", "Reliance", 
            "Axis Bank", "Maruti", "ITC", "Bajaj Finance", "Wipro"
        ]
        symbols = [
            "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "RELIANCE.NS",
            "AXISBANK.NS", "MARUTI.NS", "ITC.NS", "BAJAJFINSV.NS", "WIPRO.NS"
        ]
    
    elif asset_type == "International Indices":
        available_assets = ["S&P 500", "NASDAQ", "Dow Jones"]
        symbols = ["^GSPC", "^IXIC", "^DJI"]
    
    else:  # Commodities
        available_assets = ["Gold", "Silver", "Crude Oil", "Natural Gas"]
        symbols = ["GC=F", "SI=F", "CL=F", "NG=F"]
    
    col_asset_select = st.columns(1)
    with col_asset_select[0]:
        selected_asset = st.selectbox(
            "**Select Asset:**",
            options=available_assets,
            help="Choose specific asset",
            key="asset_selector"
        )
    
    asset_index = available_assets.index(selected_asset)
    symbol = symbols[asset_index]
    
    st.markdown("---")
    
    # Period selection
    st.write("### ⏱️ TIME PERIOD")
    years = st.slider("**Years of Historical Data:**", 1, 10, 3, help="Historical data for model training", key="years_slider")
    
    forecast_days = st.slider("**Forecast Period (Days):**", 5, 60, 20, help="Number of days to forecast", key="forecast_days_slider")
    
    st.markdown("---")
    
    # Model selection
    models = st.multiselect(
        "**Select Models:**",
        options=["GARCH(1,1)", "EGARCH(1,1)", "Both"],
        default=["GARCH(1,1)"],
        help="Choose volatility models to compare",
        key="model_selector"
    )
    
    st.markdown("---")
    st.write("**About This Tool**")
    st.write("""
    Advanced volatility forecasting using:
    - 📊 **GARCH(1,1)** - Generalized ARCH
    - ⚡ **EGARCH** - Exponential GARCH (asymmetric)
    - 📈 Real-time Yahoo Finance data
    - 🔮 Rolling window forecasts
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("### 📈 VOLATILITY ANALYSIS")

# Fetch data
with st.spinner(f"📊 Fetching {selected_asset} data..."):
    try:
        data = DataFetcher.fetch_stock_data(symbol, period=f"{years}y")
        
        if data is None or len(data) < 100:
            st.error(f"❌ Insufficient data for {selected_asset}. Please try another asset or longer period.")
            st.stop()
        
        # Calculate returns
        returns = np.log(data['Close'] / data['Close'].shift(1)).dropna() * 100
        
        st.success(f"✅ Loaded {len(data)} trading days for {selected_asset}")
        
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL FITTING & FORECASTING
# ═══════════════════════════════════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_volatility = returns.std()
    st.metric("Current Volatility", f"{current_volatility:.4f}%")

with col2:
    annual_volatility = current_volatility * np.sqrt(252)
    st.metric("Annualized Volatility", f"{annual_volatility:.2f}%")

with col3:
    mean_return = returns.mean()
    st.metric("Mean Daily Return", f"{mean_return:.4f}%")

with col4:
    sharpe_ratio = (returns.mean() * 252) / (returns.std() * np.sqrt(252))
    st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# TABS FOR DIFFERENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Price & Returns",
    "🔮 GARCH(1,1) Forecast",
    "⚡ EGARCH(1,1) Forecast",
    "📈 Model Comparison",
    "📋 Statistics"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: PRICE & RETURNS VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("#### 📊 Price History & Returns Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price chart
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color=COLORS['primary_dark'], width=2)
        ))
        fig_price.update_layout(
            title=f"{selected_asset} - Price History ({years} Years)",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        # Returns distribution
        fig_returns = px.histogram(
            x=returns,
            nbins=50,
            title=f"{selected_asset} - Daily Returns Distribution",
            labels={'x': 'Daily Returns (%)', 'y': 'Frequency'},
            color_discrete_sequence=[COLORS['primary_light']]
        )
        fig_returns.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_returns, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: GARCH(1,1) FORECAST
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("#### 🔮 GARCH(1,1) Model Analysis & Forecast")
    
    with st.spinner("⏳ Fitting GARCH(1,1) model..."):
        try:
            garch_results, garch_forecast = VolatilityModels.fit_garch(
                returns, 
                forecast_periods=forecast_days
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("AIC", f"{garch_results.aic:.2f}")
            with col2:
                st.metric("BIC", f"{garch_results.bic:.2f}")
            with col3:
                st.metric("Log-Likelihood", f"{garch_results.loglikelihood:.2f}")
            
            # Model parameters
            st.markdown("**Model Parameters:**")
            params_garch = pd.DataFrame({
                'Parameter': ['ω (Omega)', 'α (Alpha)', 'β (Beta)'],
                'Coefficient': [
                    garch_results.params['Constant'],
                    garch_results.params['alpha[1]'],
                    garch_results.params['beta[1]']
                ],
                'Std Error': [
                    garch_results.std_err['Constant'],
                    garch_results.std_err['alpha[1]'],
                    garch_results.std_err['beta[1]']
                ]
            })
            st.dataframe(params_garch, use_container_width=True)
            
            # Forecast visualization
            st.markdown("**Volatility Forecast:**")
            
            forecast_index = pd.date_range(
                start=data.index[-1],
                periods=forecast_days + 1,
                freq='D'
            )[1:]
            
            fig_garch = go.Figure()
            
            # Historical volatility
            historical_vol = returns.rolling(20).std()
            fig_garch.add_trace(go.Scatter(
                x=historical_vol.index,
                y=historical_vol,
                mode='lines',
                name='Historical Volatility (20-day)',
                line=dict(color=COLORS['primary_dark'], width=2)
            ))
            
            # Conditional volatility
            fig_garch.add_trace(go.Scatter(
                x=data.index,
                y=np.sqrt(garch_results.conditional_volatility) * np.sqrt(252),
                mode='lines',
                name='GARCH(1,1) Conditional Vol',
                line=dict(color=COLORS['primary_light'], width=2)
            ))
            
            # Forecast
            fig_garch.add_trace(go.Scatter(
                x=forecast_index,
                y=garch_forecast * np.sqrt(252),
                mode='lines+markers',
                name='GARCH(1,1) Forecast',
                line=dict(color=COLORS['accent_gold'], width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            fig_garch.update_layout(
                title=f"{selected_asset} - GARCH(1,1) Volatility Forecast",
                xaxis_title="Date",
                yaxis_title="Annualized Volatility (%)",
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )
            st.plotly_chart(fig_garch, use_container_width=True)
            
            # Forecast table
            st.markdown("**Forecast Values (Next 20 days):**")
            forecast_df = pd.DataFrame({
                'Date': forecast_index[:20],
                'Forecasted Volatility (%)': (garch_forecast[:20] * np.sqrt(252)).round(4),
                'Confidence Level': '68%'
            })
            st.dataframe(forecast_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error fitting GARCH model: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: EGARCH(1,1) FORECAST
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("#### ⚡ EGARCH(1,1) Model Analysis & Forecast")
    
    with st.spinner("⏳ Fitting EGARCH(1,1) model..."):
        try:
            egarch_results, egarch_forecast = VolatilityModels.fit_egarch(
                returns,
                forecast_periods=forecast_days
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("AIC", f"{egarch_results.aic:.2f}")
            with col2:
                st.metric("BIC", f"{egarch_results.bic:.2f}")
            with col3:
                st.metric("Log-Likelihood", f"{egarch_results.loglikelihood:.2f}")
            
            # Model parameters
            st.markdown("**Model Parameters:**")
            params_egarch = pd.DataFrame({
                'Parameter': ['ω (Omega)', 'α (Alpha)', 'β (Beta)', 'γ (Gamma)'],
                'Coefficient': [
                    egarch_results.params['Constant'],
                    egarch_results.params['alpha[1]'],
                    egarch_results.params['beta[1]'],
                    egarch_results.params['gamma[1]']
                ],
                'Std Error': [
                    egarch_results.std_err['Constant'],
                    egarch_results.std_err['alpha[1]'],
                    egarch_results.std_err['beta[1]'],
                    egarch_results.std_err['gamma[1]']
                ]
            })
            st.dataframe(params_egarch, use_container_width=True)
            
            st.info("💡 **Note:** γ (Gamma) parameter captures asymmetric effects (leverage effect)")
            
            # Forecast visualization
            st.markdown("**Volatility Forecast:**")
            
            forecast_index = pd.date_range(
                start=data.index[-1],
                periods=forecast_days + 1,
                freq='D'
            )[1:]
            
            fig_egarch = go.Figure()
            
            # Historical volatility
            historical_vol = returns.rolling(20).std()
            fig_egarch.add_trace(go.Scatter(
                x=historical_vol.index,
                y=historical_vol,
                mode='lines',
                name='Historical Volatility (20-day)',
                line=dict(color=COLORS['primary_dark'], width=2)
            ))
            
            # Conditional volatility
            fig_egarch.add_trace(go.Scatter(
                x=data.index,
                y=np.sqrt(egarch_results.conditional_volatility) * np.sqrt(252),
                mode='lines',
                name='EGARCH(1,1) Conditional Vol',
                line=dict(color=COLORS['primary_light'], width=2)
            ))
            
            # Forecast
            fig_egarch.add_trace(go.Scatter(
                x=forecast_index,
                y=egarch_forecast * np.sqrt(252),
                mode='lines+markers',
                name='EGARCH(1,1) Forecast',
                line=dict(color=COLORS['accent_gold'], width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            fig_egarch.update_layout(
                title=f"{selected_asset} - EGARCH(1,1) Volatility Forecast",
                xaxis_title="Date",
                yaxis_title="Annualized Volatility (%)",
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )
            st.plotly_chart(fig_egarch, use_container_width=True)
            
            # Forecast table
            st.markdown("**Forecast Values (Next 20 days):**")
            forecast_df = pd.DataFrame({
                'Date': forecast_index[:20],
                'Forecasted Volatility (%)': (egarch_forecast[:20] * np.sqrt(252)).round(4),
                'Confidence Level': '68%'
            })
            st.dataframe(forecast_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error fitting EGARCH model: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: MODEL COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("#### 📈 GARCH vs EGARCH Comparison")
    
    with st.spinner("⏳ Comparing models..."):
        try:
            garch_results, garch_forecast = VolatilityModels.fit_garch(returns, forecast_days)
            egarch_results, egarch_forecast = VolatilityModels.fit_egarch(returns, forecast_days)
            
            # Model comparison metrics
            st.markdown("**Model Performance Metrics:**")
            
            comparison_df = pd.DataFrame({
                'Metric': ['AIC', 'BIC', 'Log-Likelihood'],
                'GARCH(1,1)': [
                    f"{garch_results.aic:.2f}",
                    f"{garch_results.bic:.2f}",
                    f"{garch_results.loglikelihood:.2f}"
                ],
                'EGARCH(1,1)': [
                    f"{egarch_results.aic:.2f}",
                    f"{egarch_results.bic:.2f}",
                    f"{egarch_results.loglikelihood:.2f}"
                ]
            })
            st.dataframe(comparison_df, use_container_width=True)
            
            # Forecast comparison
            st.markdown("**Forecast Comparison:**")
            
            forecast_index = pd.date_range(
                start=data.index[-1],
                periods=forecast_days + 1,
                freq='D'
            )[1:]
            
            fig_compare = go.Figure()
            
            fig_compare.add_trace(go.Scatter(
                x=forecast_index,
                y=garch_forecast * np.sqrt(252),
                mode='lines+markers',
                name='GARCH(1,1)',
                line=dict(color=COLORS['primary_light'], width=3)
            ))
            
            fig_compare.add_trace(go.Scatter(
                x=forecast_index,
                y=egarch_forecast * np.sqrt(252),
                mode='lines+markers',
                name='EGARCH(1,1)',
                line=dict(color=COLORS['accent_gold'], width=3)
            ))
            
            fig_compare.update_layout(
                title=f"{selected_asset} - GARCH vs EGARCH Forecast Comparison",
                xaxis_title="Date",
                yaxis_title="Annualized Volatility (%)",
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )
            st.plotly_chart(fig_compare, use_container_width=True)
            
            # Which model is better?
            st.markdown("**Model Selection Recommendation:**")
            
            if garch_results.aic < egarch_results.aic:
                better_model = "GARCH(1,1)"
                aic_diff = egarch_results.aic - garch_results.aic
            else:
                better_model = "EGARCH(1,1)"
                aic_diff = garch_results.aic - egarch_results.aic
            
            st.success(f"✅ **Recommended Model:** {better_model} (Better AIC by {aic_diff:.2f})")
            
            st.info(f"""
            **Model Selection Insights:**
            
            - **GARCH(1,1):** Simpler model, symmetric volatility response
            - **EGARCH(1,1):** Captures asymmetric effects (leverage effect)
            
            **When to use GARCH:** Symmetric markets, simpler forecasting
            **When to use EGARCH:** Equity markets with leverage effects
            """)
            
        except Exception as e:
            st.error(f"❌ Error comparing models: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5: DETAILED STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("#### 📋 Detailed Statistical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Returns Statistics:**")
        stats_df = pd.DataFrame({
            'Metric': ['Mean', 'Std Dev', 'Skewness', 'Kurtosis', 'Min', 'Max'],
            'Value': [
                f"{returns.mean():.4f}%",
                f"{returns.std():.4f}%",
                f"{returns.skew():.4f}",
                f"{returns.kurtosis():.4f}",
                f"{returns.min():.4f}%",
                f"{returns.max():.4f}%"
            ]
        })
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.markdown("**Volatility Statistics:**")
        vol_df = pd.DataFrame({
            'Period': ['20-day', 'Annual'],
            'Volatility': [
                f"{returns.rolling(20).std().mean():.4f}%",
                f"{returns.std() * np.sqrt(252):.2f}%"
            ]
        })
        st.dataframe(vol_df, use_container_width=True)
    
    # ACF plot
    st.markdown("**Returns Autocorrelation:**")
    from statsmodels.graphics.tsaplots import plot_acf
    
    col1, col2 = st.columns(2)
    
    with col1:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 4))
        plot_acf(returns, lags=40, ax=ax, title='ACF of Returns')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 4))
        plot_acf(returns**2, lags=40, ax=ax, title='ACF of Squared Returns')
        st.pyplot(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")

# Create footer using pure Streamlit components
st.markdown("""
<style>
    .footer-container {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 2px solid #003366;
        background-color: #f8f9fa;
    }
    .footer-title {
        color: #003366;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .footer-text {
        color: #555;
        font-size: 14px;
        margin: 5px 0;
    }
    .footer-author {
        color: #666;
        font-size: 13px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🏔️ THE MOUNTAIN PATH - VOLATILITY FORECASTING PLATFORM")
    st.markdown("**Professional GARCH & EGARCH Volatility Analysis**")
    st.markdown("Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience")
    
    # Social links
    st.markdown("")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/trichyravis)")
    with col_b:
        st.markdown("[🐙 GitHub](https://github.com/trichyravis)")
    with col_c:
        st.markdown("[📧 Email](mailto:contact@mountainpath.com)")
    
    st.markdown("---")
    
    # Disclaimer
    st.warning("""
    **⚠️ Disclaimer:** Educational Purpose Only.  
    This tool is for research and educational purposes. Not financial advice.  
    Always consult qualified financial advisors before making investment decisions.  
    Past volatility does not guarantee future results.
    """)
    
    st.markdown("")
    st.markdown("© 2025 The Mountain Path - World of Finance | All Rights Reserved")
    st.markdown("*Built with ❤️ using Streamlit, GARCH & EGARCH Models*")
