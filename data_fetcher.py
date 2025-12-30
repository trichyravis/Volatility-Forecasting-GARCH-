"""
═══════════════════════════════════════════════════════════════════════════════
DATA FETCHER - VOLATILITY FORECASTING APP
Real-time data from Yahoo Finance
═══════════════════════════════════════════════════════════════════════════════
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import time

class DataFetcher:
    """Fetch and process financial data from Yahoo Finance"""
    
    # Mapping of assets to Yahoo Finance symbols
    ASSET_MAPPING = {
        # Nifty Indices
        "NIFTY 50 Index": "^NSEI",
        "NIFTY Bank Index": "^NSEBANK",
        "NIFTY IT Index": "^CNXIT",
        
        # Top Nifty Stocks
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "Reliance": "RELIANCE.NS",
        "Axis Bank": "AXISBANK.NS",
        "Maruti": "MARUTI.NS",
        "ITC": "ITC.NS",
        "Bajaj Finance": "BAJAJFINSV.NS",
        "Wipro": "WIPRO.NS",
        "Kotak Bank": "KOTAKBANK.NS",
        "State Bank of India": "SBIN.NS",
        "Larsen & Toubro": "LT.NS",
        "Hindustan Unilever": "HINDUNILVR.NS",
        "Asian Paints": "ASIANPAINT.NS",
        
        # International Indices
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
        "Russell 2000": "^RUT",
        
        # Commodities
        "Gold": "GC=F",
        "Silver": "SI=F",
        "Crude Oil": "CL=F",
        "Natural Gas": "NG=F",
        "Copper": "HG=F",
        "Aluminum": "ALI=F",
    }
    
    @staticmethod
    def fetch_stock_data(
        symbol: str,
        period: str = "3y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch stock/index/commodity data from Yahoo Finance
        
        Args:
            symbol: Yahoo Finance symbol
            period: Time period (e.g., "1y", "3y", "10y")
            interval: Data interval (default: "1d" for daily)
        
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            print(f"📊 Fetching data for {symbol}...")
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data is None or len(data) == 0:
                print(f"❌ No data retrieved for {symbol}")
                return None
            
            # Remove rows with NaN
            data = data.dropna()
            
            if len(data) < 100:
                print(f"⚠️ Warning: Only {len(data)} trading days available")
                return None
            
            print(f"✅ Fetched {len(data)} trading days for {symbol}")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def fetch_multiple_assets(
        symbols: list,
        period: str = "3y"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple assets
        
        Args:
            symbols: List of Yahoo Finance symbols
            period: Time period
        
        Returns:
            Dictionary mapping symbol to data
        """
        data_dict = {}
        
        for symbol in symbols:
            data = DataFetcher.fetch_stock_data(symbol, period)
            if data is not None:
                data_dict[symbol] = data
            time.sleep(0.5)  # Rate limiting
        
        return data_dict
    
    @staticmethod
    def calculate_returns(prices: pd.Series, method: str = "log") -> pd.Series:
        """
        Calculate returns from price series
        
        Args:
            prices: Series of prices
            method: "log" (default) or "simple"
        
        Returns:
            Series of returns (in percentage)
        """
        if method == "log":
            returns = np.log(prices / prices.shift(1)).dropna()
        else:
            returns = ((prices / prices.shift(1)) - 1).dropna()
        
        return returns * 100  # Convert to percentage
    
    @staticmethod
    def calculate_rolling_volatility(
        prices: pd.Series,
        window: int = 20
    ) -> pd.Series:
        """
        Calculate rolling volatility
        
        Args:
            prices: Series of prices
            window: Rolling window size (default: 20 days)
        
        Returns:
            Series of rolling volatility
        """
        returns = DataFetcher.calculate_returns(prices)
        rolling_vol = returns.rolling(window=window).std()
        return rolling_vol
    
    @staticmethod
    def get_asset_info(symbol: str) -> Dict:
        """
        Get additional asset information
        
        Args:
            symbol: Yahoo Finance symbol
        
        Returns:
            Dictionary with asset information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "name": info.get("longName", "Unknown"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "currency": info.get("currency", "USD"),
                "marketCap": info.get("marketCap", "N/A"),
                "52WeekHigh": info.get("fiftyTwoWeekHigh", "N/A"),
                "52WeekLow": info.get("fiftyTwoWeekLow", "N/A"),
            }
        except Exception as e:
            print(f"Warning: Could not fetch info for {symbol}: {e}")
            return {}
    
    @staticmethod
    def validate_data(data: pd.DataFrame, min_observations: int = 100) -> Tuple[bool, str]:
        """
        Validate fetched data for analysis
        
        Args:
            data: DataFrame to validate
            min_observations: Minimum required observations
        
        Returns:
            Tuple of (is_valid, message)
        """
        if data is None:
            return False, "Data is None"
        
        if len(data) < min_observations:
            return False, f"Insufficient data: {len(data)} < {min_observations}"
        
        if data['Close'].isnull().any():
            return False, "Data contains NaN values"
        
        if (data['Close'] == 0).any():
            return False, "Data contains zero prices"
        
        return True, "Data validation passed"

# Example usage
if __name__ == "__main__":
    # Test fetching data
    data = DataFetcher.fetch_stock_data("^NSEI", period="3y")
    if data is not None:
        print(f"Data shape: {data.shape}")
        print(data.head())
        
        # Calculate returns
        returns = DataFetcher.calculate_returns(data['Close'])
        print(f"\nReturns statistics:")
        print(f"Mean: {returns.mean():.4f}%")
        print(f"Std: {returns.std():.4f}%")
