
"""
═══════════════════════════════════════════════════════════════════════════════
VOLATILITY MODELS - GARCH & EGARCH
Generalized Autoregressive Conditional Heteroskedasticity Models
BULLETPROOF VERSION WITH ROBUST ERROR HANDLING
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
    Bulletproof version with extensive error handling and fallbacks
    """
    
    @staticmethod
    def fit_garch(
        returns: pd.Series,
        p: int = 1,
        q: int = 1,
        forecast_periods: int = 20
    ) -> Tuple:
        """
        Fit GARCH(p,q) model and generate forecasts - BULLETPROOF VERSION
        
        GARCH(1,1) Model:
        ────────────────
        σ_t² = ω + α*ε_{t-1}² + β*σ_{t-1}²
        """
        try:
            # Ensure returns are clean
            returns_clean = returns.dropna().values
            
            if len(returns_clean) < 50:
                raise ValueError(f"Insufficient data: {len(returns_clean)} observations")
            
            # Fit GARCH model with robust settings
            model = arch_model(
                returns_clean,
                vol='Garch',
                p=p,
                q=q,
                rescale=False
            )
            
            # Fit with multiple tries
            try:
                results = model.fit(
                    disp='off',
                    show_warning=False,
                    options={'maxiter': 1000}
                )
            except:
                # Fallback: simpler fitting
                results = model.fit(disp='off', show_warning=False)
            
            # Generate forecast
            try:
                forecast_obj = results.forecast(horizon=forecast_periods)
                forecast_variance = forecast_obj.variance.values[-1, :]
                forecast_volatility = np.sqrt(forecast_variance) * 100
            except:
                # Fallback forecast
                cond_vol = results.conditional_volatility
                last_vol = cond_vol.iloc[-1]
                forecast_volatility = np.full(forecast_periods, last_vol * 100)
            
            return results, forecast_volatility
            
        except Exception as e:
            print(f"❌ GARCH Error: {str(e)}")
            raise
    
    @staticmethod
    def fit_egarch(
        returns: pd.Series,
        p: int = 1,
        q: int = 1,
        forecast_periods: int = 20
    ) -> Tuple:
        """
        Fit EGARCH(p,q) model and generate forecasts - BULLETPROOF VERSION
        """
        try:
            # Ensure returns are clean
            returns_clean = returns.dropna().values
            
            if len(returns_clean) < 50:
                raise ValueError(f"Insufficient data: {len(returns_clean)} observations")
            
            # Fit EGARCH model
            model = arch_model(
                returns_clean,
                vol='EGarch',
                p=p,
                q=q,
                rescale=False
            )
            
            # Fit with multiple tries
            try:
                results = model.fit(
                    disp='off',
                    show_warning=False,
                    options={'maxiter': 1000}
                )
            except:
                results = model.fit(disp='off', show_warning=False)
            
            # Generate forecast
            try:
                forecast_obj = results.forecast(horizon=forecast_periods)
                forecast_variance = forecast_obj.variance.values[-1, :]
                forecast_volatility = np.sqrt(forecast_variance) * 100
            except:
                # Fallback forecast
                cond_vol = results.conditional_volatility
                last_vol = cond_vol.iloc[-1]
                forecast_volatility = np.full(forecast_periods, last_vol * 100)
            
            return results, forecast_volatility
            
        except Exception as e:
            print(f"❌ EGARCH Error: {str(e)}")
            raise
    
    @staticmethod
    def safe_get_param(params, keys_to_try):
        """
        Safely extract parameter, trying multiple key names
        """
        if isinstance(params, dict):
            for key in keys_to_try:
                if key in params:
                    return params[key]
        
        return np.nan
    
    @staticmethod
    def compare_models(returns: pd.Series) -> dict:
        """
        Fit both GARCH and EGARCH, return comparison metrics
        """
        try:
            garch_results, _ = VolatilityModels.fit_garch(returns, forecast_periods=1)
            egarch_results, _ = VolatilityModels.fit_egarch(returns, forecast_periods=1)
            
            return {
                "GARCH(1,1)": {
                    "AIC": float(garch_results.aic),
                    "BIC": float(garch_results.bic),
                    "LogLikelihood": float(garch_results.loglikelihood),
                },
                "EGARCH(1,1)": {
                    "AIC": float(egarch_results.aic),
                    "BIC": float(egarch_results.bic),
                    "LogLikelihood": float(egarch_results.loglikelihood),
                }
            }
        except Exception as e:
            print(f"❌ Comparison Error: {str(e)}")
            return None
    
    @staticmethod
    def extract_model_parameters(results) -> dict:
        """
        Extract model parameters with safe fallbacks
        """
        try:
            params = results.params
            std_err = results.std_err
            
            # Try multiple key names
            constant_keys = ['Constant', 'const', 'Intercept']
            omega = VolatilityModels.safe_get_param(params, constant_keys)
            omega_se = VolatilityModels.safe_get_param(std_err, constant_keys)
            
            alpha_keys = ['alpha[1]', 'Alpha', 'alpha']
            alpha = VolatilityModels.safe_get_param(params, alpha_keys)
            alpha_se = VolatilityModels.safe_get_param(std_err, alpha_keys)
            
            beta_keys = ['beta[1]', 'Beta', 'beta']
            beta = VolatilityModels.safe_get_param(params, beta_keys)
            beta_se = VolatilityModels.safe_get_param(std_err, beta_keys)
            
            return {
                "Omega (ω)": omega,
                "Omega SE": omega_se,
                "Alpha (α)": alpha,
                "Alpha SE": alpha_se,
                "Beta (β)": beta,
                "Beta SE": beta_se,
            }
        except Exception as e:
            print(f"⚠️ Parameter extraction error: {str(e)}")
            return {}
