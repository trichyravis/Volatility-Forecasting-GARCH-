
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
    
    # Initialize session state for asset selection
    if 'last_asset_class' not in st.session_state:
        st.session_state.last_asset_class = "Equity Indices"
    if 'selected_asset_index' not in st.session_state:
        st.session_state.selected_asset_index = 0
    
    # Asset selection - with visible styling
    st.markdown("**Asset Class:**")
    asset_type = st.selectbox(
        label="Asset Class",
        options=["Equity Indices", "Nifty Stocks", "International Indices", "Commodities"],
        help="Choose asset class",
        key="asset_class_selector",
        index=["Equity Indices", "Nifty Stocks", "International Indices", "Commodities"].index(st.session_state.last_asset_class),
        label_visibility="collapsed"
    )
    
    # Track if asset class changed
    if asset_type != st.session_state.last_asset_class:
        st.session_state.last_asset_class = asset_type
        st.session_state.selected_asset_index = 0
    
    # Asset choice based on class
    if asset_type == "Equity Indices":
        available_assets = ["NIFTY 50 Index", "NIFTY Bank Index", "NIFTY IT Index"]
        symbols = ["^NSEI", "^NSEBANK", "^CNXIT"]
    
    elif asset_type == "Nifty Stocks":
        available_assets = [
            "TCS", "Infosys", "HDFC Bank", "ICICI Bank", "Reliance", 
            "Axis Bank", "Maruti", "ITC", "Bajaj Finance", "Wipro",
            "Kotak Bank", "State Bank of India", "Larsen & Toubro"
        ]
        symbols = [
            "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "RELIANCE.NS",
            "AXISBANK.NS", "MARUTI.NS", "ITC.NS", "BAJAJFINSV.NS", "WIPRO.NS",
            "KOTAKBANK.NS", "SBIN.NS", "LT.NS"
        ]
    
    elif asset_type == "International Indices":
        available_assets = ["S&P 500", "NASDAQ", "Dow Jones", "Russell 2000"]
        symbols = ["^GSPC", "^IXIC", "^DJI", "^RUT"]
    
    else:  # Commodities
        available_assets = ["Gold", "Silver", "Crude Oil", "Natural Gas", "Copper"]
        symbols = ["GC=F", "SI=F", "CL=F", "NG=F", "HG=F"]
    
    # Ensure selected index is valid
    if st.session_state.selected_asset_index >= len(available_assets):
        st.session_state.selected_asset_index = 0
    
    # Select Asset - with visible styling
    st.markdown("**Select Asset:**")
    selected_asset = st.selectbox(
        label="Select Asset",
        options=available_assets,
        help="Choose specific asset",
        key="asset_selector",
        index=st.session_state.selected_asset_index,
        label_visibility="collapsed"
    )
    
    # Update selected index
    st.session_state.selected_asset_index = available_assets.index(selected_asset)
    
    asset_index = available_assets.index(selected_asset)
    symbol = symbols[asset_index]
    
    st.markdown("---")
    
    # Model selection with radio buttons - only ONE option can be selected
    st.markdown("<span style='color: #DC3545; font-weight: 700; font-size: 14px;'>🔧 Select Models:</span>", unsafe_allow_html=True)
    models = st.radio(
        "Models",
        options=["GARCH(1,1)", "EGARCH(1,1)", "Both"],
        default="GARCH(1,1)",
        help="Choose ONE volatility model for analysis",
        key="model_selector",
        label_visibility="collapsed",
        horizontal=False
    )
    
    st.markdown("---")
    
    # Period selection
    st.write("### ⏱️ TIME PERIOD")
    years = st.slider("**Years of Historical Data:**", 1, 10, 3, help="Historical data for model training", key="years_slider")
    
    forecast_days = st.slider("**Forecast Period (Days):**", 5, 60, 20, help="Number of days to forecast", key="forecast_days_slider")
    
    st.markdown("---")
    
    # Configuration info
    with st.expander("⚙️ Selected Configuration"):
        st.markdown(f"**Asset Class:** <span style='color: #DC3545; font-weight: 700;'>{asset_type}</span>", unsafe_allow_html=True)
        st.markdown(f"**Selected Asset:** <span style='color: #DC3545; font-weight: 700;'>{selected_asset}</span>", unsafe_allow_html=True)
        st.markdown(f"**Symbol:** <span style='color: #DC3545; font-weight: 700; font-family: monospace;'>{symbol}</span>", unsafe_allow_html=True)
        st.markdown(f"**Years:** <span style='color: #DC3545; font-weight: 700;'>{years}</span>", unsafe_allow_html=True)
        st.markdown(f"**Forecast Days:** <span style='color: #DC3545; font-weight: 700;'>{forecast_days}</span>", unsafe_allow_html=True)
        st.markdown(f"**Models:** <span style='color: #DC3545; font-weight: 700;'>{models}</span>", unsafe_allow_html=True)
    
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

# Fetch data with better error handling
data_fetch_placeholder = st.empty()
with data_fetch_placeholder.container():
    with st.spinner(f"📊 Fetching {selected_asset} ({symbol}) data..."):
        try:
            data = DataFetcher.fetch_stock_data(symbol, period=f"{years}y")
            
            if data is None:
                st.error(f"❌ No data available for {selected_asset} ({symbol}). Please try another asset.")
                st.info("💡 Tip: Try selecting a different asset or increasing the historical data period.")
                st.stop()
            
            if len(data) < 100:
                st.warning(f"⚠️ Only {len(data)} trading days available for {selected_asset}. Model may be less reliable.")
                if len(data) < 50:
                    st.error(f"❌ Insufficient data ({len(data)} days < 50 minimum). Please try another asset.")
                    st.stop()
            
            # Calculate returns
            returns = np.log(data['Close'] / data['Close'].shift(1)).dropna() * 100
            
            st.success(f"✅ Loaded {len(data)} trading days for {selected_asset}")
            
        except Exception as e:
            st.error(f"❌ Error fetching data for {selected_asset}: {str(e)}")
            st.info("💡 Possible causes:\n- Invalid ticker symbol\n- Yahoo Finance service issue\n- Network connectivity problem\n\nPlease try another asset.")
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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Price & Returns",
    "🔮 GARCH(1,1) Forecast",
    "⚡ EGARCH(1,1) Forecast",
    "📈 Model Comparison",
    "📋 Statistics",
    "📚 Learning & Theory"
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
    # Check if GARCH is selected
    if "GARCH(1,1)" not in models and "Both" not in models:
        st.info("ℹ️ **GARCH(1,1) model not selected.** Please select 'GARCH(1,1)' or 'Both' in the sidebar to view this analysis.")
    else:
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
                
                # Model parameters - SAFE EXTRACTION WITH BETTER LOGIC
                st.markdown("**Model Parameters:**")
                try:
                    params = garch_results.params
                    std_err = garch_results.std_err
                    
                    print(f"DEBUG - Available GARCH params: {list(params.index)}")
                    
                    # Get Omega - try multiple names and first position
                    omega = None
                    omega_se = None
                    for key in ['Constant', 'const', 'mu']:
                        if key in params:
                            omega = float(params[key])
                            omega_se = float(std_err[key])
                            break
                    
                    if omega is None and len(params) > 0:
                        try:
                            omega = float(params.iloc[0])
                            omega_se = float(std_err.iloc[0])
                        except:
                            pass
                    
                    # Get Alpha
                    alpha = None
                    alpha_se = None
                    for key in params.index:
                        if 'alpha' in str(key).lower():
                            alpha = float(params[key])
                            alpha_se = float(std_err[key])
                            break
                    
                    # Get Beta
                    beta = None
                    beta_se = None
                    for key in params.index:
                        if 'beta' in str(key).lower():
                            beta = float(params[key])
                            beta_se = float(std_err[key])
                            break
                    
                    # Format values for display
                    def format_param(val):
                        if val is None or pd.isna(val):
                            return "N/A"
                        return f"{float(val):.6f}"
                    
                    params_garch = pd.DataFrame({
                        'Parameter': ['ω (Omega)', 'α (Alpha)', 'β (Beta)'],
                        'Coefficient': [format_param(omega), format_param(alpha), format_param(beta)],
                        'Std Error': [format_param(omega_se), format_param(alpha_se), format_param(beta_se)]
                    })
                    st.dataframe(params_garch, use_container_width=True)
                except Exception as param_error:
                    st.info(f"⚠️ Parameter extraction issue: {str(param_error)}")
                    print(f"Parameter extraction error: {param_error}")
                
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
    # Check if EGARCH is selected
    if "EGARCH(1,1)" not in models and "Both" not in models:
        st.info("ℹ️ **EGARCH(1,1) model not selected.** Please select 'EGARCH(1,1)' or 'Both' in the sidebar to view this analysis.")
    else:
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
                
                # Model parameters - SAFE EXTRACTION WITH BETTER LOGIC
                st.markdown("**Model Parameters:**")
                try:
                    params = egarch_results.params
                    std_err = egarch_results.std_err
                    
                    print(f"DEBUG - Available EGARCH params: {list(params.index)}")
                    
                    # Get Omega - try multiple names and first position
                    omega = None
                    omega_se = None
                    for key in ['Constant', 'const', 'mu']:
                        if key in params:
                            omega = float(params[key])
                            omega_se = float(std_err[key])
                            break
                    
                    if omega is None and len(params) > 0:
                        try:
                            omega = float(params.iloc[0])
                            omega_se = float(std_err.iloc[0])
                        except:
                            pass
                    
                    # Get Alpha
                    alpha = None
                    alpha_se = None
                    for key in params.index:
                        if 'alpha' in str(key).lower():
                            alpha = float(params[key])
                            alpha_se = float(std_err[key])
                            break
                    
                    # Get Beta
                    beta = None
                    beta_se = None
                    for key in params.index:
                        if 'beta' in str(key).lower():
                            beta = float(params[key])
                            beta_se = float(std_err[key])
                            break
                    
                    # Get Gamma - try multiple variations
                    gamma = None
                    gamma_se = None
                    for key in params.index:
                        key_lower = str(key).lower()
                        # Try multiple possible gamma names
                        if any(g in key_lower for g in ['gamma', 'leverage', 'asymmetry']):
                            try:
                                gamma = float(params[key])
                                gamma_se = float(std_err[key])
                                print(f"Found Gamma as: {key}")
                                break
                            except:
                                continue
                    
                    # Format values for display
                    def format_param(val):
                        if val is None or pd.isna(val):
                            return "N/A"
                        return f"{float(val):.6f}"
                    
                    params_egarch = pd.DataFrame({
                        'Parameter': ['ω (Omega)', 'α (Alpha)', 'β (Beta)', 'γ (Gamma)'],
                        'Coefficient': [format_param(omega), format_param(alpha), format_param(beta), format_param(gamma)],
                        'Std Error': [format_param(omega_se), format_param(alpha_se), format_param(beta_se), format_param(gamma_se)]
                    })
                    st.dataframe(params_egarch, use_container_width=True)
                    
                    # Show different note based on whether Gamma was estimated
                    if gamma is None:
                        st.info("💡 **Note:** γ (Gamma) parameter not estimated. This can occur with certain model specifications or data characteristics. The asymmetry/leverage effect may be constrained or not identified in this dataset.")
                    else:
                        st.info("💡 **Note:** γ (Gamma) parameter captures asymmetric effects (leverage effect) - negative shocks have larger impact on volatility than positive shocks")
                except Exception as param_error:
                    st.info(f"⚠️ Parameter extraction issue: {str(param_error)}")
                    print(f"EGARCH param error: {param_error}")
                
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
# TAB 6: LEARNING & THEORY
# ═══════════════════════════════════════════════════════════════════════════════

with tab6:
    st.markdown("# 📚 Learning & Theory: GARCH & EGARCH Models")
    
    # Overview Section
    st.markdown("---")
    st.markdown("## 🎯 Overview")
    st.info("""
    This section explains the theoretical foundations of GARCH and EGARCH volatility models,
    including their mathematical basis, assumptions, inputs, and practical interpretations.
    """)
    
    # Create tabs for organized learning
    learn_tab1, learn_tab2, learn_tab3, learn_tab4, learn_tab5 = st.tabs([
        "📖 GARCH(1,1)",
        "⚡ EGARCH(1,1)",
        "🔬 Comparison",
        "📊 Forecasting",
        "💡 Interpretation"
    ])
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # GARCH EXPLANATION TAB
    # ═══════════════════════════════════════════════════════════════════════════════
    with learn_tab1:
        st.markdown("## GARCH(1,1) Model - Generalized Autoregressive Conditional Heteroskedasticity")
        
        st.markdown("### 📐 Mathematical Formula")
        st.latex(r"""
        \sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2
        """)
        
        st.markdown("### 🔑 Parameter Meanings")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### ω (Omega)")
            st.write("""
            **Constant term**
            - Long-run average volatility
            - Baseline volatility level
            - Must be positive
            """)
        
        with col2:
            st.markdown("#### α (Alpha)")
            st.write("""
            **Shock coefficient**
            - Measures immediate reaction to shocks
            - Response to unexpected returns
            - Range: 0 to 1
            """)
        
        with col3:
            st.markdown("#### β (Beta)")
            st.write("""
            **Persistence coefficient**
            - Measures volatility persistence
            - How quickly shocks fade
            - Range: 0 to 1
            """)
        
        st.markdown("### 💼 Model Inputs")
        st.markdown("""
        1. **Historical Returns:** Daily/weekly price changes
        2. **Time Period:** Historical data for model training (e.g., 3 years)
        3. **Forecast Horizon:** Future days to forecast volatility
        """)
        
        st.markdown("### 📋 Key Assumptions")
        st.markdown("""
        1. **Symmetric Response:** Positive and negative shocks have equal impact
        2. **Mean Reversion:** Volatility reverts to long-run average
        3. **Conditional Normality:** Returns follow normal distribution
        4. **Constant Parameters:** Model coefficients are stable over time
        5. **Stationarity:** Time series properties don't change over time
        """)
        
        st.markdown("### ✨ Advantages")
        st.success("""
        ✅ **Simplicity:** Easy to understand and implement
        ✅ **Interpretability:** Clear meaning of each parameter
        ✅ **Effectiveness:** Works well for many financial series
        ✅ **Computational Efficiency:** Fast to estimate and forecast
        ✅ **Stability:** Stable estimates for most datasets
        ✅ **Symmetric:** Good for markets without leverage effects
        """)
        
        st.markdown("### ⚠️ Limitations")
        st.warning("""
        ❌ **Symmetric Response:** Ignores leverage effect (negative shocks ≠ positive shocks)
        ❌ **Parameter Constraints:** Both α and β must be <1 (restrictive)
        ❌ **Slow Adaptation:** May not capture rapid volatility changes
        ❌ **Mean Reversion:** Assumes volatility reverts to constant level
        """)
        
        st.markdown("### 🎯 Best Use Cases")
        st.markdown("""
        - **Commodities:** Gold, oil, agricultural products
        - **Symmetric Markets:** Markets without leverage effect
        - **Stable Periods:** When leverage effect is minimal
        - **Quick Forecasts:** When speed and simplicity are priorities
        """)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # EGARCH EXPLANATION TAB
    # ═══════════════════════════════════════════════════════════════════════════════
    with learn_tab2:
        st.markdown("## EGARCH(1,1) Model - Exponential GARCH")
        
        st.markdown("### 📐 Mathematical Formula")
        st.latex(r"""
        \log(\sigma_t^2) = \omega + \alpha \frac{\epsilon_{t-1}}{|\sigma_{t-1}|} + \gamma \frac{\epsilon_{t-1}}{\sigma_{t-1}} + \beta \log(\sigma_{t-1}^2)
        """)
        
        st.markdown("### 🔑 Parameter Meanings")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("#### ω (Omega)")
            st.write("""
            **Intercept**
            - Baseline log-volatility
            - Can be negative
            """)
        
        with col2:
            st.markdown("#### α (Alpha)")
            st.write("""
            **Shock magnitude**
            - Symmetric response component
            - Size effect
            """)
        
        with col3:
            st.markdown("#### β (Beta)")
            st.write("""
            **Persistence**
            - Volatility clustering
            - Memory effect
            """)
        
        with col4:
            st.markdown("#### γ (Gamma)")
            st.write("""
            **Leverage effect**
            - Asymmetric response
            - Good news ≠ Bad news
            """)
        
        st.markdown("### 💼 Model Inputs")
        st.markdown("""
        1. **Historical Returns:** Daily/weekly price changes
        2. **Time Period:** Historical data for model training (e.g., 3 years)
        3. **Forecast Horizon:** Future days to forecast volatility
        """)
        
        st.markdown("### 📋 Key Assumptions")
        st.markdown("""
        1. **Asymmetric Response:** Negative shocks have larger impact (leverage effect)
        2. **Log-Volatility Model:** Uses logarithm of variance (more stable)
        3. **Mean Reversion:** Volatility reverts to long-run average
        4. **Conditional Normality:** Returns follow normal distribution
        5. **Stationarity:** Time series properties don't change over time
        """)
        
        st.markdown("### ✨ Advantages")
        st.success("""
        ✅ **Leverage Effect:** Captures asymmetric response to shocks
        ✅ **Log-Specification:** More stable, no negativity constraints
        ✅ **Better Fit:** Often provides better fit than GARCH
        ✅ **Realistic:** Reflects actual market behavior (bad news > good news)
        ✅ **Flexibility:** No constraint that α+β<1
        ✅ **Equity Markets:** Particularly good for stocks with leverage effects
        """)
        
        st.markdown("### ⚠️ Limitations")
        st.warning("""
        ❌ **Complexity:** More parameters and more difficult to interpret
        ❌ **Convergence:** Sometimes hard to estimate reliably
        ❌ **Gamma N/A:** Not all datasets show leverage effects
        ❌ **Computational Cost:** Slower to estimate and forecast
        ❌ **Parameter Identification:** Gamma may not be identified in some data
        """)
        
        st.markdown("### 🎯 Best Use Cases")
        st.markdown("""
        - **Equity Markets:** Stocks where bad news > good news effect
        - **High Volatility Assets:** Where leverage effect is pronounced
        - **Risk Management:** More accurate tail risk estimation
        - **Option Pricing:** Better for modeling implied volatility
        """)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # COMPARISON TAB
    # ═══════════════════════════════════════════════════════════════════════════════
    with learn_tab3:
        st.markdown("## GARCH vs EGARCH: Side-by-Side Comparison")
        
        comparison_df = pd.DataFrame({
            'Feature': [
                'Response to Shocks',
                'Leverage Effect',
                'Parameters',
                'Complexity',
                'Estimation Speed',
                'Positivity Constraint',
                'Log-Specification',
                'Best For',
                'Convergence',
                'Gamma Parameter'
            ],
            'GARCH(1,1)': [
                'Symmetric',
                'No',
                '3 (ω, α, β)',
                'Simple',
                'Fast',
                'Yes (α+β<1)',
                'No',
                'Commodities, stable markets',
                'Easy',
                'N/A'
            ],
            'EGARCH(1,1)': [
                'Asymmetric',
                'Yes (γ parameter)',
                '4 (ω, α, β, γ)',
                'Complex',
                'Slower',
                'No',
                'Yes',
                'Equities, risk management',
                'Sometimes difficult',
                'Captures asymmetry'
            ]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        st.markdown("### 📊 Model Selection Recommendation")
        
        col_g, col_e = st.columns(2)
        
        with col_g:
            st.success("""
            ### Choose GARCH When:
            - ✅ Simplicity and speed matter
            - ✅ No leverage effect visible
            - ✅ Commodities or symmetric markets
            - ✅ Quick preliminary analysis needed
            - ✅ Stable convergence required
            """)
        
        with col_e:
            st.info("""
            ### Choose EGARCH When:
            - ⚡ Leverage effect is present
            - ⚡ Better fit is more important
            - ⚡ Equity/stock markets
            - ⚡ Risk management focus
            - ⚡ Can tolerate estimation complexity
            """)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # FORECASTING TAB
    # ═══════════════════════════════════════════════════════════════════════════════
    with learn_tab4:
        st.markdown("## 🔮 Volatility Forecasting Process")
        
        st.markdown("### Step-by-Step Process")
        
        steps_data = {
            'Step': ['1️⃣ Data Preparation', '2️⃣ Model Estimation', '3️⃣ Diagnostic Checks', 
                     '4️⃣ Forecast Generation', '5️⃣ Interpretation'],
            'Description': [
                'Clean historical data, calculate returns',
                'Estimate ω, α, β (and γ for EGARCH) parameters',
                'Check model fit (AIC, BIC), residual diagnostics',
                'Project conditional volatility into future',
                'Analyze forecasts, assess confidence'
            ]
        }
        
        st.write(pd.DataFrame(steps_data))
        
        st.markdown("### 📈 Forecast Methodology")
        st.markdown("""
        **One-Step Ahead Forecasting:**
        - Use last observed returns and volatility
        - Generate forecast for next period
        - Update with new information
        
        **Multi-Step Forecasting:**
        - Use forecasted conditional volatility
        - Volatility tends toward long-run average
        - Uncertainty increases with forecast horizon
        """)
        
        st.markdown("### 🎯 Model Fit Statistics")
        st.markdown("""
        **AIC (Akaike Information Criterion):**
        - Lower is better
        - Penalizes model complexity
        - Use for model comparison
        
        **BIC (Bayesian Information Criterion):**
        - Lower is better
        - Stronger penalty for complexity
        - Preferred for model selection
        
        **Log-Likelihood:**
        - Higher is better
        - Goodness of fit measure
        - Basis for information criteria
        """)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # INTERPRETATION TAB
    # ═══════════════════════════════════════════════════════════════════════════════
    with learn_tab5:
        st.markdown("## 💡 Interpretation & Practical Use")
        
        st.markdown("### Understanding the Parameters")
        
        st.markdown("""
        #### ω (Omega) Interpretation
        - **Meaning:** Long-run average volatility level
        - **High ω:** Markets are naturally volatile
        - **Low ω:** Markets are stable
        - **Example:** ω=0.05 means 5% baseline daily volatility
        
        #### α (Alpha) Interpretation
        - **High α (0.1-0.3):** Quick response to shocks
        - **Low α (0.01-0.05):** Slow response to shocks
        - **Example:** α=0.15 means 15% of yesterday's shock enters today's volatility
        
        #### β (Beta) Interpretation
        - **High β (0.8-0.95):** Volatility is persistent
        - **Low β (0.3-0.6):** Volatility quickly reverts to mean
        - **Example:** β=0.85 means 85% of yesterday's volatility stays today
        
        #### γ (Gamma) EGARCH Interpretation
        - **Positive γ:** Negative shocks increase volatility more
        - **Magnitude of γ:** Strength of leverage effect
        - **Example:** γ=0.15 means asymmetry is moderate
        - **Note:** Often N/A for some datasets (means no leverage effect)
        """)
        
        st.markdown("### Reading Forecast Results")
        
        st.markdown("""
        **Volatility Forecast Values:**
        - **Higher volatility forecast:** Market expects higher uncertainty
        - **Lower volatility forecast:** Market expects stability
        - **Increasing trend:** Shocks are accumulating
        - **Decreasing trend:** Volatility reverting to mean
        
        **Using Forecasts:**
        1. **Risk Management:** Set wider stop-losses for high volatility
        2. **Options Trading:** Higher volatility → higher option premiums
        3. **Portfolio Allocation:** Adjust asset weights based on volatility
        4. **Hedging:** More hedging needed in high volatility periods
        """)
        
        st.markdown("### Practical Guidance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### For Traders")
            st.markdown("""
            - **Rising volatility:** Consider reducing position sizes
            - **Falling volatility:** May signal reversal opportunity
            - **Forecast accuracy:** Improves near-term (1-5 days)
            - **Confidence:** Declines for longer horizons
            """)
        
        with col2:
            st.markdown("#### For Risk Managers")
            st.markdown("""
            - **VaR Calculation:** Use model-based volatility
            - **Margin Requirements:** Adjust based on forecasts
            - **Stress Testing:** Scenario analysis with high volatility
            - **Monitoring:** Watch α for shock sensitivity
            """)
        
        st.markdown("### ⚠️ Important Reminders")
        st.warning("""
        - **Past volatility ≠ Future volatility:** Use forecasts cautiously
        - **Model assumptions may not hold:** Test regularly
        - **Structural breaks:** Models struggle with regime changes
        - **Tail events:** Models underestimate extreme moves
        - **Combine with analysis:** Don't rely solely on quantitative models
        """)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")

# Use the professional Footer component from template
Footer.render(
    title="🏔️ THE MOUNTAIN PATH - VOLATILITY FORECASTING PLATFORM",
    description="Professional GARCH & EGARCH Volatility Analysis",
    author="Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience",
    social_links={
        "LinkedIn": "https://www.linkedin.com/in/trichyravis",
        "GitHub": "https://github.com/trichyravis"
    },
    disclaimer="⚠️ **DISCLAIMER:** Educational Purpose Only. This tool is for research and educational purposes. Not financial advice. Always consult qualified financial advisors before making investment decisions. Past volatility does not guarantee future results."
)
