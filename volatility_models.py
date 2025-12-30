
"""
═══════════════════════════════════════════════════════════════════════════════
VOLATILITY MODELS - GARCH & EGARCH (FIXED VERSION)
Proper pandas Series handling + Safe parameter extraction
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from arch import arch_model
from typing import Tuple
import warnings
warnings.filterwarnings('ignore')

class VolatilityModels:
    
    @staticmethod
    def fit_garch(returns: pd.Series, p: int = 1, q: int = 1, forecast_periods: int = 20) -> Tuple:
        """Fit GARCH(1,1) model and generate forecasts"""
        try:
            # KEEP AS PANDAS SERIES - critical!
            returns_clean = returns.dropna()
            
            if len(returns_clean) < 50:
                raise ValueError(f"Insufficient data: {len(returns_clean)} observations")
            
            model = arch_model(returns_clean, vol='Garch', p=p, q=q, rescale=False)
            
            try:
                results = model.fit(disp='off', show_warning=False, options={'maxiter': 1000})
            except:
                results = model.fit(disp='off', show_warning=False)
            
            try:
                forecast_obj = results.forecast(horizon=forecast_periods)
                forecast_variance = forecast_obj.variance.values[-1, :]
                forecast_volatility = np.sqrt(forecast_variance)
            except:
                cond_vol = results.conditional_volatility
                last_vol = cond_vol.iloc[-1]
                forecast_volatility = np.full(forecast_periods, last_vol)
            
            return results, forecast_volatility
            
        except Exception as e:
            print(f"GARCH Error: {str(e)}")
            raise
    
    @staticmethod
    def fit_egarch(returns: pd.Series, p: int = 1, q: int = 1, forecast_periods: int = 20) -> Tuple:
        """Fit EGARCH(1,1) model and generate forecasts"""
        try:
            # KEEP AS PANDAS SERIES - critical!
            returns_clean = returns.dropna()
            
            if len(returns_clean) < 50:
                raise ValueError(f"Insufficient data: {len(returns_clean)} observations")
            
            model = arch_model(returns_clean, vol='EGarch', p=p, q=q, rescale=False)
            
            try:
                results = model.fit(disp='off', show_warning=False, options={'maxiter': 1000})
            except:
                results = model.fit(disp='off', show_warning=False)
            
            try:
                forecast_obj = results.forecast(horizon=forecast_periods)
                forecast_variance = forecast_obj.variance.values[-1, :]
                forecast_volatility = np.sqrt(forecast_variance)
            except:
                cond_vol = results.conditional_volatility
                last_vol = cond_vol.iloc[-1]
                forecast_volatility = np.full(forecast_periods, last_vol)
            
            return results, forecast_volatility
            
        except Exception as e:
            print(f"EGARCH Error: {str(e)}")
            raise
    
    @staticmethod
    def compare_models(returns: pd.Series) -> dict:
        """Compare GARCH and EGARCH models"""
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
            print(f"Comparison Error: {str(e)}")
            return None
    
    @staticmethod
    def extract_model_parameters(results) -> dict:
        """Extract model parameters safely"""
        try:
            params = results.params
            std_err = results.std_err
            
            # Get Omega (Constant) - try multiple names
            if 'Constant' in params:
                omega = params['Constant']
                omega_se = std_err['Constant']
            elif 'const' in params:
                omega = params['const']
                omega_se = std_err['const']
            else:
                omega = None
                omega_se = None
            
            # Get Alpha
            alpha = params.get('alpha[1]', None)
            alpha_se = std_err.get('alpha[1]', None) if alpha is not None else None
            
            # Get Beta
            beta = params.get('beta[1]', None)
            beta_se = std_err.get('beta[1]', None) if beta is not None else None
            
            return {
                "omega": omega,
                "omega_se": omega_se,
                "alpha": alpha,
                "alpha_se": alpha_se,
                "beta": beta,
                "beta_se": beta_se,
            }
        except Exception as e:
            print(f"Parameter extraction error: {str(e)}")
            return {}
