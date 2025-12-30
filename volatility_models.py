
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
        """Extract model parameters safely - handles all parameter names"""
        try:
            params = results.params
            std_err = results.std_err
            
            # Print all available parameters for debugging
            print(f"Available parameters: {list(params.index)}")
            print(f"Parameter values:\n{params}")
            
            # Get Omega - try all possible names
            omega = None
            omega_se = None
            for key in ['Constant', 'const', 'mu']:
                if key in params:
                    omega = float(params[key])
                    omega_se = float(std_err[key])
                    print(f"Found Omega as: {key}")
                    break
            
            # If still not found, check if it's the first parameter
            if omega is None and len(params) > 0:
                try:
                    omega = float(params.iloc[0])
                    omega_se = float(std_err.iloc[0])
                    print(f"Found Omega as first parameter: {params.index[0]}")
                except:
                    omega = None
                    omega_se = None
            
            # Get Alpha - try all variations
            alpha = None
            alpha_se = None
            for key in params.index:
                key_str = str(key).lower()
                if 'alpha' in key_str:
                    alpha = float(params[key])
                    alpha_se = float(std_err[key])
                    print(f"Found Alpha as: {key}")
                    break
            
            # Get Beta - try all variations
            beta = None
            beta_se = None
            for key in params.index:
                key_str = str(key).lower()
                if 'beta' in key_str:
                    beta = float(params[key])
                    beta_se = float(std_err[key])
                    print(f"Found Beta as: {key}")
                    break
            
            # Get Gamma - try all variations
            gamma = None
            gamma_se = None
            gamma_found = False
            
            for key in params.index:
                key_str = str(key).lower()
                # Try multiple gamma names
                if any(g in key_str for g in ['gamma', 'leverage', 'asymmetry', 'skewness']):
                    try:
                        gamma = float(params[key])
                        gamma_se = float(std_err[key])
                        print(f"Found Gamma as: {key}")
                        gamma_found = True
                        break
                    except:
                        continue
            
            if not gamma_found:
                print("Gamma parameter not found in results")
            
            return {
                "omega": omega,
                "omega_se": omega_se,
                "alpha": alpha,
                "alpha_se": alpha_se,
                "beta": beta,
                "beta_se": beta_se,
                "gamma": gamma,
                "gamma_se": gamma_se,
            }
        except Exception as e:
            print(f"Parameter extraction error: {str(e)}")
            return {}
