"""
═══════════════════════════════════════════════════════════════════════════════
THE MOUNTAIN PATH - VOLATILITY FORECASTING PLATFORM
Advanced GARCH & EGARCH Analysis for Financial Markets
═══════════════════════════════════════════════════════════════════════════════

Prof. V. Ravichandran
28+ Years Corporate Finance & Banking Experience
10+ Years Academic Excellence
"""

# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════

A professional-grade Streamlit application for volatility forecasting using advanced
econometric models. Analyze real-time market data and forecast volatility using:

✅ **GARCH(1,1)** - Generalized Autoregressive Conditional Heteroskedasticity
✅ **EGARCH(1,1)** - Exponential GARCH with leverage effects
✅ **Real-time Data** - Yahoo Finance integration
✅ **Multiple Assets** - Stocks, Indices, Commodities
✅ **Professional Design** - Using Mountain Path Design Template

---

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════════════════════════════════════════════

## Asset Selection
✓ **NIFTY 50 & Sector Indices**
  - NIFTY 50 Index
  - NIFTY Bank Index
  - NIFTY IT Index

✓ **Top Nifty Stocks**
  - TCS, Infosys, HDFC Bank, ICICI Bank, Reliance
  - Axis Bank, Maruti, ITC, Bajaj Finance, Wipro
  - Kotak Bank, SBI, L&T, HUL, Asian Paints

✓ **International Indices**
  - S&P 500
  - NASDAQ
  - Dow Jones
  - Russell 2000

✓ **Commodities**
  - Gold, Silver
  - Crude Oil, Natural Gas
  - Copper, Aluminum

## Analysis Features
✓ **Price & Returns Analysis**
  - Historical price charts
  - Returns distribution
  - Statistical summaries

✓ **GARCH(1,1) Forecasting**
  - Model fitting and parameter estimation
  - Conditional volatility
  - Short-term forecasts
  - AIC/BIC model comparison

✓ **EGARCH(1,1) Forecasting**
  - Asymmetric volatility modeling
  - Leverage effect capture
  - Tail risk analysis
  - Model diagnostics

✓ **Model Comparison**
  - Side-by-side forecast comparison
  - Information criteria comparison
  - Model selection guidance
  - Performance metrics

✓ **Statistical Analysis**
  - Returns statistics (mean, std, skew, kurtosis)
  - Volatility metrics
  - ACF/PACF plots
  - Risk measures

---

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK START
# ═══════════════════════════════════════════════════════════════════════════════

## Installation

1. **Clone/Download the project**
```bash
cd volatility_forecasting_app
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run app.py
```

4. **Open in browser**
```
http://localhost:8501
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# USAGE GUIDE
# ═══════════════════════════════════════════════════════════════════════════════

## Step 1: Select Asset Class
Choose from:
- Equity Indices (Nifty, S&P500, Nasdaq, etc.)
- Nifty Stocks (TCS, Infosys, Banks, etc.)
- International Indices (S&P500, Nasdaq, Dow Jones)
- Commodities (Gold, Silver, Oil, etc.)

## Step 2: Select Specific Asset
Choose the specific stock, index, or commodity to analyze

## Step 3: Set Time Period
- Select years of historical data (1-10 years)
- Typical: 3-5 years for model training
- More data = better model estimation

## Step 4: Set Forecast Period
- Select number of days to forecast (5-60 days)
- Typical: 20 days (1 month)

## Step 5: Select Models
Choose:
- GARCH(1,1) for symmetric volatility
- EGARCH(1,1) for asymmetric/leverage effects
- Both for comparison

## Step 6: Analyze Results
Navigate tabs:
- 📊 Price & Returns - Historical data visualization
- 🔮 GARCH Forecast - GARCH(1,1) results
- ⚡ EGARCH Forecast - EGARCH(1,1) results
- 📈 Comparison - Model comparison
- 📋 Statistics - Detailed statistics

---

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL THEORY
# ═══════════════════════════════════════════════════════════════════════════════

## GARCH(1,1) Model

**Equation:**
```
σ_t² = ω + α*ε_{t-1}² + β*σ_{t-1}²
```

**Parameters:**
- **ω (Omega)**: Constant baseline volatility
- **α (Alpha)**: ARCH effect - impact of past shocks (0-1)
- **β (Beta)**: GARCH effect - volatility persistence (0-1)
- **σ_t²**: Conditional variance

**Interpretation:**
- α measures how quickly volatility responds to shocks
- β measures how long volatility persists
- α + β close to 1 = high volatility persistence
- Higher α = faster response, shorter memory
- Higher β = slower decay, longer memory

**When to use:**
- General volatility forecasting
- Symmetric markets (indices, commodities)
- When simplicity is needed
- Undergraduate to master level analysis

---

## EGARCH(1,1) Model

**Equation:**
```
log(σ_t²) = ω + α*(|ε_{t-1}|/σ_{t-1}) + γ*(ε_{t-1}/σ_{t-1}) + β*log(σ_{t-1}²)
```

**Parameters:**
- **ω (Omega)**: Constant
- **α (Alpha)**: Magnitude effect (shock size impact)
- **β (Beta)**: Persistence
- **γ (Gamma)**: Leverage/asymmetry effect (CRITICAL!)

**Interpretation:**
- γ captures asymmetric response to shocks
- If γ < 0: negative shocks increase volatility more (leverage effect)
- If γ = 0: symmetric response (same as GARCH)
- If γ > 0: positive shocks increase volatility more (rare)
- Log specification ensures positive volatility
- Better captures tail risk and market crashes

**When to use:**
- Equity market volatility (leverage effect present)
- Options pricing
- Risk management
- When asymmetry matters
- Advanced professional analysis

---

## Model Selection

**Information Criteria:**

**AIC (Akaike Information Criterion):**
```
AIC = 2k - 2ln(L)
```
- Lower is better
- k = number of parameters
- L = log-likelihood
- Balances fit and complexity

**BIC (Bayesian Information Criterion):**
```
BIC = k*ln(n) - 2ln(L)
```
- More stringent penalty
- n = number of observations
- Prefers simpler models

**Decision Rule:**
- If AIC or BIC is lower → that model is better
- Difference > 10 → strong evidence for better model
- Difference 5-10 → moderate evidence
- Difference < 5 → models are comparable

---

# ═══════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════

## Why Volatility Forecasting?

1. **Risk Management**
   - Portfolio volatility forecasting
   - Value at Risk (VaR) calculation
   - Position sizing

2. **Options Pricing**
   - Implied volatility comparison
   - Option valuation
   - Hedging strategies

3. **Trading Strategies**
   - Volatility arbitrage
   - Mean reversion strategies
   - Regime identification

4. **Regulatory Requirements**
   - Basel III capital requirements
   - Risk reporting
   - Stress testing

## Volatility Types

**Historical Volatility:**
- Calculated from past returns
- Backward-looking
- σ = std(returns)

**Conditional Volatility:**
- Time-varying (σ_t)
- From GARCH/EGARCH models
- Accounts for volatility clustering

**Implied Volatility:**
- From options market
- Forward-looking
- Market expectation

**Realized Volatility:**
- Sum of squared intraday returns
- High-frequency data
- Actual market volatility

---

# ═══════════════════════════════════════════════════════════════════════════════
# FILE STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

```
volatility_forecasting_app/
├── app.py                      # Main Streamlit application
├── data_fetcher.py            # Yahoo Finance data module
├── volatility_models.py        # GARCH & EGARCH models
├── config.py                  # Design template config
├── styles.py                  # Design template styles
├── components.py              # Design template components
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE DESCRIPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

## app.py - Main Application
- Streamlit interface
- Sidebar controls
- Tab-based analysis
- Data fetching and model fitting
- Visualization and reporting

## data_fetcher.py - Data Management
- Yahoo Finance integration
- Data validation
- Returns calculation
- Rolling volatility computation
- Multi-asset data fetching

## volatility_models.py - Model Implementation
- GARCH(1,1) fitting and forecasting
- EGARCH(1,1) fitting and forecasting
- Model comparison and selection
- Parameter extraction
- Confidence interval calculation
- Rolling window forecasting

## Template Files
- **config.py**: Colors, fonts, configuration
- **styles.py**: CSS styling and HTML generators
- **components.py**: Pre-built UI components

---

# ═══════════════════════════════════════════════════════════════════════════════
# INTERPRETATION GUIDE
# ═══════════════════════════════════════════════════════════════════════════════

## Current Volatility Metrics

**Daily Volatility (%):**
- Calculated from 20-day rolling window
- Example: 2.5% means typical daily move is ±2.5%

**Annualized Volatility:**
- Daily volatility × √252 (trading days)
- Example: 2.5% daily = 2.5% × 15.87 = 39.7% annual
- Used for comparing with other assets

**Sharpe Ratio:**
- (Annual Return - Risk-free Rate) / Annual Volatility
- > 1.0: Good risk-adjusted returns
- > 2.0: Excellent risk-adjusted returns
- < 0: Returns worse than risk-free rate

## Returns Distribution

**Mean:**
- Average daily return
- Positive = average gains, Negative = average losses

**Skewness:**
- -1.0: Left-skewed (large negative returns possible)
- 0.0: Symmetric
- +1.0: Right-skewed (large positive returns possible)

**Kurtosis:**
- > 3: Fat tails (extreme moves likely)
- = 3: Normal distribution
- < 3: Thin tails (extreme moves less likely)

## GARCH/EGARCH Parameters

**High α (>0.2):**
- Fast response to shocks
- Market reacts quickly to news
- Shorter volatility memory

**High β (>0.7):**
- Volatility persists long after shocks
- Slow mean reversion
- High volatility clustering

**α + β ≈ 1.0:**
- Nearly integrated process
- Very persistent volatility
- Long memory effects

**γ < 0 (EGARCH):**
- Leverage effect present
- Bad news → bigger volatility increase
- Typical for stocks

---

# ═══════════════════════════════════════════════════════════════════════════════
# COMMON ISSUES & SOLUTIONS
# ═══════════════════════════════════════════════════════════════════════════════

### Issue: "Insufficient data for asset"
**Solution:** 
- Try longer time period (5-10 years)
- Select different asset
- Check internet connection

### Issue: "Model fitting error"
**Solution:**
- Try shorter historical period
- Select asset with more trading activity
- Check data for gaps/missing values

### Issue: "Convergence warning"
**Solution:**
- Model still produces results (usually reliable)
- Try different forecast horizon
- Use simpler model (GARCH instead of EGARCH)

### Issue: "Plots not showing"
**Solution:**
- Try refresh browser (Ctrl+R)
- Check browser console for errors
- Ensure Plotly is installed

### Issue: "High volatility forecasts"
**Solution:**
- This may be correct for volatile assets
- Compare with historical volatility
- Check model parameters for appropriateness

---

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════════════════════

## Example 1: NIFTY 50 Analysis

**Current Stats:**
- Volatility: 1.8% daily
- Annual: 28.5%
- Sharpe: 1.2

**GARCH Results:**
- AIC: 2850 (good fit)
- α = 0.15 (moderate shock response)
- β = 0.80 (high persistence)
- α + β = 0.95 (strong clustering)

**Interpretation:**
Market is moderately volatile with clustering. Shocks persist for extended periods.
Good fit. Use for risk management.

---

## Example 2: Gold Price Analysis

**Current Stats:**
- Volatility: 1.2% daily
- Annual: 19.0%
- Sharpe: 0.8

**EGARCH Results:**
- AIC: 2200 (better than GARCH)
- γ = -0.25 (moderate leverage)
- This indicates asymmetric response

**Interpretation:**
Gold shows asymmetric behavior (unusual). May indicate demand changes with market sentiment.
EGARCH better captures behavior. Use for options pricing.

---

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED FEATURES
# ═══════════════════════════════════════════════════════════════════════════════

**Coming Soon:**
- Multi-asset portfolio volatility
- Correlation dynamics (DCC-GARCH)
- Realized volatility computation
- High-frequency data support
- Value at Risk (VaR) calculation
- Expected Shortfall (CVaR) metrics
- Volatility surface for options
- GARCH in Mean (risk premium estimation)
- TARCH (Threshold GARCH) model
- Component GARCH (long/short-term volatility)

---

# ═══════════════════════════════════════════════════════════════════════════════
# DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════

### Streamlit Cloud (FREE!)

1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository
5. Done! Share your link!

### Environment Setup

Create `.streamlit/config.toml`:
```
[theme]
primaryColor = "#003366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false

[logger]
level = "error"
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCES & RESOURCES
# ═══════════════════════════════════════════════════════════════════════════════

**Books:**
- "Forecasting Volatility in Financial Markets" - David G. Luenberger
- "The Arch Model and Related Topics" - Tim Bollerslev
- "Multivariate Time Series Analysis" - Ruey S. Tsay

**Papers:**
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity"
- Nelson, D. B. (1991). "Conditional Heteroskedasticity in Asset Returns"

**Libraries:**
- ARCH: https://arch.readthedocs.io/
- Statsmodels: https://www.statsmodels.org/
- Yfinance: https://github.com/ranaroussi/yfinance

**Websites:**
- Yahoo Finance: https://finance.yahoo.com
- Investopedia GARCH: https://www.investopedia.com/terms/g/garch.asp

---

# ═══════════════════════════════════════════════════════════════════════════════
# DISCLAIMER
# ═══════════════════════════════════════════════════════════════════════════════

⚠️ **EDUCATIONAL PURPOSE ONLY**

This tool is for educational and research purposes only. It is NOT financial advice.

- Past volatility does NOT guarantee future results
- Model forecasts can be wrong
- Do NOT make investment decisions based solely on these forecasts
- Always consult qualified financial advisors
- Volatility is unpredictable and can spike unexpectedly
- Use for learning, risk management understanding, and research only

**The creator and maintainers are not liable for any financial losses or damages.**

---

# ═══════════════════════════════════════════════════════════════════════════════
# SUPPORT & CONTACT
# ═══════════════════════════════════════════════════════════════════════════════

**Questions? Issues?**
- Review the documentation above
- Check the README section
- Verify data with Yahoo Finance
- Check browser console for errors

**Contact:**
Prof. V. Ravichandran
- LinkedIn: https://www.linkedin.com/in/trichyravis
- GitHub: https://github.com/trichyravis

---

**Happy Forecasting! 📊**

Build your volatility insights with GARCH & EGARCH models!
Use this knowledge wisely. Trade responsibly. 🚀

═══════════════════════════════════════════════════════════════════════════════
"""
