"""
═══════════════════════════════════════════════════════════════════════════════
VOLATILITY MODELS - GARCH & EGARCH
Generalized Autoregressive Conditional Heteroskedasticity Models
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from arch import arch_model
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class VolatilityModels:
    """
    Implement GARCH(1,1) and EGARCH(1,1) models for volatility forecasting
    """
    
    @staticmethod
    def fit_garch(
        returns: pd.Series,
        p: int = 1,
        q: int = 1,
        forecast_periods: int = 20
    ) -> Tuple:
        """
        Fit GARCH(p,q) model and generate forecasts
        
        GARCH(1,1) Model:
        ────────────────
        σ_t² = ω + α*ε_{t-1}² + β*σ_{t-1}²
        
        Where:
        - ω (omega): Constant (baseline volatility)
        - α (alpha): Impact of past shocks
        - β (beta): Persistence of volatility
        - σ_t²: Conditional variance
        - ε_t: Residuals
        
        Args:
            returns: Series of returns (in %)
            p: ARCH order (default: 1)
            q: GARCH order (default: 1)
            forecast_periods: Number of periods to forecast
        
        Returns:
            Tuple of (results_object, forecast_array)
        """
        try:
            # Standardize returns
            returns_std = returns * 100  # Convert to basis points for better numerical stability
            
            # Fit GARCH model
            model = arch_model(
                returns_std,
                vol='Garch',
                p=p,
                q=q,
                rescale=False
            )
            
            results = model.fit(disp='off')
            
            # Generate forecast
            forecast = results.get_forecast(horizon=forecast_periods)
            forecast_variance = forecast.variance.values[-1, :] / 10000  # Convert back to variance
            forecast_volatility = np.sqrt(forecast_variance)
            
            return results, forecast_volatility
            
        except Exception as e:
            print(f"❌ Error fitting GARCH model: {str(e)}")
            raise
    
    @staticmethod
    def fit_egarch(
        returns: pd.Series,
        p: int = 1,
        q: int = 1,
        forecast_periods: int = 20
    ) -> Tuple:
        """
        Fit EGARCH(p,q) model and generate forecasts
        
        EGARCH(1,1) Model:
        ──────────────────
        log(σ_t²) = ω + α*(|ε_{t-1}|/σ_{t-1}) + γ*(ε_{t-1}/σ_{t-1}) + β*log(σ_{t-1}²)
        
        Where:
        - ω (omega): Constant
        - α (alpha): Magnitude effect (volatility response to shocks)
        - β (beta): Persistence parameter
        - γ (gamma): Leverage/asymmetry effect (negative shocks have bigger impact)
        
        Key Features:
        - Asymmetric response to positive/negative shocks
        - Captures leverage effect (bad news increases volatility more)
        - Log specification ensures positive volatility
        
        Args:
            returns: Series of returns (in %)
            p: ARCH order (default: 1)
            q: GARCH order (default: 1)
            forecast_periods: Number of periods to forecast
        
        Returns:
            Tuple of (results_object, forecast_array)
        """
        try:
            # Standardize returns
            returns_std = returns * 100
            
            # Fit EGARCH model
            model = arch_model(
                returns_std,
                vol='EGarch',
                p=p,
                q=q,
                rescale=False
            )
            
            results = model.fit(disp='off')
            
            # Generate forecast
            forecast = results.get_forecast(horizon=forecast_periods)
            forecast_variance = forecast.variance.values[-1, :] / 10000
            forecast_volatility = np.sqrt(forecast_variance)
            
            return results, forecast_volatility
            
        except Exception as e:
            print(f"❌ Error fitting EGARCH model: {str(e)}")
            raise
    
    @staticmethod
    def compare_models(returns: pd.Series) -> dict:
        """
        Fit both GARCH and EGARCH, return comparison metrics
        
        Args:
            returns: Series of returns
        
        Returns:
            Dictionary with comparison results
        """
        try:
            garch_results, _ = VolatilityModels.fit_garch(returns, forecast_periods=1)
            egarch_results, _ = VolatilityModels.fit_egarch(returns, forecast_periods=1)
            
            return {
                "GARCH(1,1)": {
                    "AIC": garch_results.aic,
                    "BIC": garch_results.bic,
                    "LogLikelihood": garch_results.loglikelihood,
                },
                "EGARCH(1,1)": {
                    "AIC": egarch_results.aic,
                    "BIC": egarch_results.bic,
                    "LogLikelihood": egarch_results.loglikelihood,
                }
            }
        except Exception as e:
            print(f"❌ Error comparing models: {str(e)}")
            return None
    
    @staticmethod
    def extract_model_parameters(results) -> dict:
        """
        Extract and format model parameters
        
        Args:
            results: ARCH model results object
        
        Returns:
            Dictionary of parameters
        """
        params = {
            "Omega (ω)": results.params.get('Constant', np.nan),
            "Alpha (α)": results.params.get('alpha[1]', np.nan),
            "Beta (β)": results.params.get('beta[1]', np.nan),
        }
        
        # Add gamma if EGARCH
        if 'gamma[1]' in results.params:
            params["Gamma (γ)"] = results.params['gamma[1]']
        
        return params
    
    @staticmethod
    def rolling_forecast(
        returns: pd.Series,
        window: int = 500,
        forecast_horizon: int = 1,
        model_type: str = "GARCH"
    ) -> pd.DataFrame:
        """
        Generate rolling forecast for out-of-sample evaluation
        
        Args:
            returns: Series of returns
            window: Rolling window size
            forecast_horizon: Forecast horizon
            model_type: "GARCH" or "EGARCH"
        
        Returns:
            DataFrame with rolling forecasts
        """
        forecasts = []
        dates = []
        
        for i in range(window, len(returns) - forecast_horizon):
            try:
                returns_window = returns.iloc[i-window:i]
                
                if model_type == "GARCH":
                    _, forecast = VolatilityModels.fit_garch(
                        returns_window,
                        forecast_periods=forecast_horizon
                    )
                else:
                    _, forecast = VolatilityModels.fit_egarch(
                        returns_window,
                        forecast_periods=forecast_horizon
                    )
                
                forecasts.append(forecast[-1])
                dates.append(returns.index[i + forecast_horizon])
                
            except Exception as e:
                continue
        
        return pd.DataFrame({
            'Date': dates,
            'Forecast': forecasts
        })
    
    @staticmethod
    def calculate_forecast_confidence_interval(
        forecast_volatility: np.ndarray,
        confidence_level: float = 0.95
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate confidence intervals for forecasts
        
        Args:
            forecast_volatility: Array of forecasted volatilities
            confidence_level: Confidence level (default: 95%)
        
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        z_score = 1.96 if confidence_level == 0.95 else 1.645  # 90%
        
        # Assume standard error increases with forecast horizon
        std_error = forecast_volatility * np.sqrt(np.arange(1, len(forecast_volatility) + 1)) * 0.1
        
        lower_bound = np.maximum(forecast_volatility - z_score * std_error, 0)
        upper_bound = forecast_volatility + z_score * std_error
        
        return lower_bound, upper_bound

# Model Documentation
"""
═══════════════════════════════════════════════════════════════════════════════
GARCH(1,1) vs EGARCH(1,1) - Key Differences
═══════════════════════════════════════════════════════════════════════════════

GARCH(1,1):
───────────
Equation: σ_t² = ω + α*ε_{t-1}² + β*σ_{t-1}²

Characteristics:
✓ Simple, widely used model
✓ Symmetric response to positive/negative shocks
✓ Easy to interpret parameters
✓ Computational efficiency
✗ Cannot capture asymmetric volatility effects

When to use:
- General volatility forecasting
- Indices with symmetric behavior
- When simplicity is preferred
- Commodity markets


EGARCH(1,1):
────────────
Equation: log(σ_t²) = ω + α*(|ε_{t-1}|/σ_{t-1}) + γ*(ε_{t-1}/σ_{t-1}) + β*log(σ_{t-1}²)

Characteristics:
✓ Captures leverage effect (asymmetry)
✓ Negative shocks have larger impact
✓ Log specification ensures positive variance
✓ Better for equity markets
✗ More complex, harder to interpret
✗ Computationally more intensive

When to use:
- Equity market volatility
- Asset with leverage effects
- When capturing tail risk is important
- Options pricing


Parameter Interpretation:
────────────────────────
α (Alpha): 
  - Speed of volatility mean reversion
  - Higher = faster response to shocks
  - Range: [0, 1)

β (Beta):
  - Persistence of volatility
  - Higher = longer memory
  - Range: [0, 1)
  - α + β close to 1 = high persistence

γ (Gamma, EGARCH only):
  - Leverage/asymmetry effect
  - Negative = bad news increases volatility more
  - Zero = symmetric response


Model Selection Criteria:
────────────────────────
AIC (Akaike Information Criterion):
- Lower is better
- Penalizes model complexity
- Formula: 2k - 2ln(L)
  where k = parameters, L = likelihood

BIC (Bayesian Information Criterion):
- More stringent penalty for complexity
- Formula: k*ln(n) - 2ln(L)
  where n = observations

Log-Likelihood:
- Higher is better
- Measures goodness of fit

Use AIC/BIC for model selection!
═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    # Example usage
    import yfinance as yf
    
    # Fetch sample data
    data = yf.download("^NSEI", period="3y", progress=False)
    returns = np.log(data['Close'] / data['Close'].shift(1)).dropna() * 100
    
    print("Fitting GARCH(1,1)...")
    garch_results, garch_forecast = VolatilityModels.fit_garch(returns, forecast_periods=20)
    print(f"GARCH AIC: {garch_results.aic:.2f}")
    print(f"GARCH Forecast (first 5 days): {garch_forecast[:5] * np.sqrt(252)}")
    
    print("\nFitting EGARCH(1,1)...")
    egarch_results, egarch_forecast = VolatilityModels.fit_egarch(returns, forecast_periods=20)
    print(f"EGARCH AIC: {egarch_results.aic:.2f}")
    print(f"EGARCH Forecast (first 5 days): {egarch_forecast[:5] * np.sqrt(252)}")
