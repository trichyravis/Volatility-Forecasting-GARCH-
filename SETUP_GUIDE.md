"""
═══════════════════════════════════════════════════════════════════════════════
VOLATILITY FORECASTING APP - SETUP & DEPLOYMENT GUIDE
Complete Instructions to Get Running
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK START (5 MINUTES)
# ═══════════════════════════════════════════════════════════════════════════════

## Step 1: Install Python (if needed)
───────────────────────────────────
- Python 3.8 or higher
- Download from: https://www.python.org/downloads/


## Step 2: Clone/Download Project
──────────────────────────────────
Option A: Clone with Git
```bash
git clone <repository-url>
cd volatility_forecasting_app
```

Option B: Download manually
- Download all files to a folder
- Navigate to that folder in terminal


## Step 3: Install Dependencies (2 minutes)
──────────────────────────────────────────
```bash
pip install -r requirements.txt
```

This installs:
✓ streamlit - Web framework
✓ pandas - Data manipulation
✓ numpy - Numerical computing
✓ yfinance - Yahoo Finance API
✓ arch - GARCH models
✓ plotly - Interactive charts
✓ scipy - Scientific computing
✓ statsmodels - Time series analysis
✓ matplotlib - Static plots
✓ scikit-learn - Machine learning


## Step 4: Run the App (30 seconds)
─────────────────────────────────
```bash
streamlit run app.py
```

This will:
1. Start Streamlit server
2. Open browser automatically
3. Show the app at http://localhost:8501


## Step 5: Start Analyzing!
──────────────────────────
✅ Select asset class
✅ Choose specific asset
✅ Set time period
✅ View forecasts!

---

# ═══════════════════════════════════════════════════════════════════════════════
# DETAILED SETUP
# ═══════════════════════════════════════════════════════════════════════════════

## Option 1: Windows Setup

### 1. Install Python
- Download from python.org
- During installation: CHECK "Add Python to PATH"
- Click "Install Now"

### 2. Open Command Prompt
- Press Windows + R
- Type: cmd
- Press Enter

### 3. Navigate to Project
```cmd
cd path\to\volatility_forecasting_app
```

### 4. Create Virtual Environment (Recommended)
```cmd
python -m venv venv
venv\Scripts\activate
```

### 5. Install Requirements
```cmd
pip install -r requirements.txt
```

### 6. Run App
```cmd
streamlit run app.py
```

### 7. View in Browser
- Automatically opens http://localhost:8501
- Or manually visit that URL


## Option 2: Mac Setup

### 1. Install Python
```bash
# Using Homebrew (if not installed: /bin/bash -c "$(curl -fsSL...)")
brew install python3
```

### 2. Navigate to Project
```bash
cd /path/to/volatility_forecasting_app
```

### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Run App
```bash
streamlit run app.py
```

### 6. View in Browser
- Visit http://localhost:8501


## Option 3: Linux Setup

### 1. Install Python
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### 2. Navigate to Project
```bash
cd /path/to/volatility_forecasting_app
```

### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Run App
```bash
streamlit run app.py
```

### 6. View in Browser
- Visit http://localhost:8501

---

# ═══════════════════════════════════════════════════════════════════════════════
# TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════════════════════

## Issue: "Python not found"
──────────────────────────
**Solution:**
1. Ensure Python is installed
2. Add Python to PATH:
   - Windows: Control Panel → System → Environment Variables
   - Add Python installation path
3. Restart terminal/command prompt
4. Try again

## Issue: "pip: command not found"
─────────────────────────────────
**Solution:**
1. Python not in PATH
2. Use python -m pip instead:
```bash
python -m pip install -r requirements.txt
```

## Issue: "No module named 'streamlit'"
──────────────────────────────────────
**Solution:**
1. Ensure you activated virtual environment:
   - Windows: venv\Scripts\activate
   - Mac/Linux: source venv/bin/activate
2. Reinstall requirements:
```bash
pip install streamlit
```

## Issue: "ModuleNotFoundError: arch"
────────────────────────────────────
**Solution:**
```bash
pip install arch
```

## Issue: "App won't load data"
─────────────────────────────
**Solution:**
1. Check internet connection
2. Verify Yahoo Finance is accessible
3. Try different asset
4. Check firewall settings

## Issue: "Port 8501 already in use"
──────────────────────────────────
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

## Issue: "Browser doesn't open automatically"
──────────────────────────────────────────────
**Solution:**
1. Manually visit http://localhost:8501
2. Check terminal for the exact URL
3. Copy/paste the URL from terminal

---

# ═══════════════════════════════════════════════════════════════════════════════
# DEPLOYMENT OPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

## Option 1: Streamlit Cloud (EASIEST & FREE!)
──────────────────────────────────────────────

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repo
4. Select branch (main) and file (app.py)
5. Click Deploy!

### Step 3: Share
- Get public URL
- Share with anyone
- No setup needed on user side!

### Pros:
✓ Completely free
✓ Auto-updates from GitHub
✓ Public URL
✓ Always running
✓ No server needed

### Cons:
✗ Limited compute
✗ Cold start delay
✗ Rate limits on data fetching


## Option 2: Heroku
──────────────────

### Setup:
1. Create Heroku account
2. Install Heroku CLI
3. Create Procfile:
```
web: streamlit run app.py --server.port=$PORT --server.headless=true
```

### Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Pros:
✓ More control
✓ Custom domain
✓ Better performance

### Cons:
✗ Paid after free tier
✗ More setup required


## Option 3: AWS EC2
───────────────────

### Setup:
1. Create EC2 instance
2. Install dependencies
3. Clone repository
4. Run app with gunicorn

### Pros:
✓ Full control
✓ Scalable
✓ Professional setup

### Cons:
✗ Paid service
✗ Complex setup
✗ Requires DevOps knowledge


## Option 4: DigitalOcean Droplet
──────────────────────────────────

### Setup:
1. Create Droplet
2. SSH into server
3. Install Python
4. Deploy app
5. Setup Nginx reverse proxy

### Pros:
✓ Affordable
✓ Good performance
✓ Easy deployment

### Cons:
✗ Monthly cost (~$5-20)
✗ Some setup required


## Recommended for Different Users

**Individual/Learner:**
→ Streamlit Cloud (free, easy, shareable)

**Small Business/Team:**
→ DigitalOcean ($5-20/month, good balance)

**Enterprise:**
→ AWS EC2 (scalable, professional, pricey)

---

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

## Customize App Appearance

Edit `config.py`:

```python
# Change colors
COLORS = {
    "primary_dark": "#003366",    # Sidebar background
    "accent_gold": "#FFD700",     # Highlights
    # ... more colors
}

# Change fonts
TYPOGRAPHY = {
    "font_primary": "Times New Roman",
    "font_secondary": "Arial",
}
```

## Customize Data Sources

Edit `app.py` sidebar:

```python
available_assets = [
    "Your Asset 1",
    "Your Asset 2",
    # ...
]
symbols = [
    "SYMBOL1.NS",
    "SYMBOL2.NS",
    # ...
]
```

## Customize Models

In `app.py`, modify default settings:

```python
years = st.slider("Years:", 1, 20, 5)  # Default 5 years
forecast_days = st.slider("Days:", 5, 90, 30)  # Default 30 days
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════

## If App is Slow

### 1. Cache Data
Add to app.py after imports:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_data(symbol, period):
    return DataFetcher.fetch_stock_data(symbol, period)
```

### 2. Reduce Historical Data
```python
# Default: 3 years
# Try: 1-2 years for faster loading
years = st.slider("Years:", 1, 5, 2)
```

### 3. Simplify Forecasts
```python
# Default: 20 days
# Try: 10 days for faster computation
forecast_days = st.slider("Days:", 5, 30, 10)
```

### 4. Reduce Assets List
Comment out less-used assets in sidebar

### 5. Upgrade Hardware (if deployed)
- More CPU → Faster computation
- More RAM → Handles more data
- SSD → Faster I/O

---

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE
# ═══════════════════════════════════════════════════════════════════════════════

## Regular Updates

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Check for Broken Assets
Test Yahoo Finance symbols regularly - they may change

### Monitor Performance
- Check error logs
- Monitor slow operations
- Optimize as needed

## Backup

```bash
# Create backup
zip -r backup_$(date +%Y%m%d).zip .

# Restore from backup
unzip backup_*.zip
```

## Logging

Add to app.py for debugging:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Fetched data for {symbol}")
logger.error(f"Error: {str(e)}")
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

```
volatility_forecasting_app/
│
├── 📄 app.py                   # Main application (EDIT FOR CONTENT)
├── 📄 data_fetcher.py          # Data module (Yahoo Finance)
├── 📄 volatility_models.py     # GARCH/EGARCH models
│
├── 🎨 config.py                # Design config (EDIT FOR COLORS)
├── 🎨 styles.py                # Design CSS
├── 🎨 components.py            # Design components
│
├── 📦 requirements.txt          # Dependencies (RUN: pip install -r)
├── 📖 README.md                 # Full documentation
├── 📖 SETUP_GUIDE.md            # This file
│
└── 📁 .streamlit/ (optional)
    └── config.toml              # Streamlit config
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# NEXT STEPS
# ═══════════════════════════════════════════════════════════════════════════════

### Immediate (Today)
✓ Install and run locally
✓ Test with different assets
✓ Understand the models

### Short-term (This Week)
✓ Customize colors/branding
✓ Add your own assets
✓ Deploy to Streamlit Cloud
✓ Share with others

### Long-term (This Month)
✓ Add more models (TARCH, ARCH)
✓ Implement multi-asset correlation
✓ Add Value at Risk metrics
✓ Create backtesting module
✓ Add machine learning predictions

---

# ═══════════════════════════════════════════════════════════════════════════════
# FINAL CHECKLIST
# ═══════════════════════════════════════════════════════════════════════════════

Before Going Live:

- [ ] ✓ App runs locally without errors
- [ ] ✓ All assets load correctly
- [ ] ✓ Models fit successfully
- [ ] ✓ Plots display properly
- [ ] ✓ No Python errors in console
- [ ] ✓ Load times are acceptable
- [ ] ✓ Customized with your branding
- [ ] ✓ Deployed to cloud (optional)
- [ ] ✓ URL tested in different browsers
- [ ] ✓ Disclaimer is visible
- [ ] ✓ Documentation complete
- [ ] ✓ Shared with intended users

---

# ═══════════════════════════════════════════════════════════════════════════════
# YOU'RE READY!
# ═══════════════════════════════════════════════════════════════════════════════

You now have a professional volatility forecasting platform!

**What to do:**
1. Run: streamlit run app.py
2. Analyze some assets
3. Understand the models
4. Share with others
5. Deploy to cloud (optional)
6. Build more features (optional)

**Questions?**
- Check README.md
- Review the code comments
- See volatility_models.py for theory
- Consult data_fetcher.py for data handling

---

## Happy Forecasting! 📊

Build professional volatility insights!
Trade wisely. Analyze responsibly. Learn deeply! 🚀

═══════════════════════════════════════════════════════════════════════════════
"""
