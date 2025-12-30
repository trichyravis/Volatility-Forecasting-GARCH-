
"""
═══════════════════════════════════════════════════════════════════════════════
VOLATILITY MODELS - GARCH & EGARCH (ENHANCED DEBUG VERSION)
Proper pandas Series handling + Comprehensive parameter extraction
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
    def print_all_params(results, model_name=""):
        """Debug function to print all available parameters"""
        print(f"\n{'='*70}")
        print(f"DEBUG: All Parameters for {model_name}")
        print(f"{'='*70}")
        print(f"Parameter names: {list(results.params.index)}")
        print(f"\nParameter values:")
        for name in results.params.index:
            val = results.params[name]
            se = results.std_err[name] if name in results.std_err else np.nan
            print(f"  {name:20s} = {val:12.8f} (SE: {se:10.8f})")
        print(f"{'='*70}\n")
    
    @staticmethod
    def fit_garch(returns: pd.Series, p: int = 1, q: int = 1, forecast_periods: int = 20) -> Tuple:
        """Fit GARCH(1,1) model and generate forecasts"""
        try:
            # KEEP AS PANDAS SERIES
            returns_clean = returns.dropna()
            
            if len(returns_clean) < 50:
                raise ValueError(f"Insufficient data: {len(returns_clean)} observations")
            
            model = arch_model(returns_clean, vol='Garch', p=p, q=q, rescale=False)
            
            try:
                results = model.fit(disp='off', show_warning=False, options={'maxiter': 1000})
            except:
                results = model.fit(disp='off', show_warning=False)
            
            # Debug print
            VolatilityModels.print_all_params(results, "GARCH")
            
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
            # KEEP AS PANDAS SERIES
            returns_clean = returns.dropna()
            
            if len(returns_clean) < 50:
                raise ValueError(f"Insufficient data: {len(returns_clean)} observations")
            
            model = arch_model(returns_clean, vol='EGarch', p=p, q=q, rescale=False)
            
            try:
                results = model.fit(disp='off', show_warning=False, options={'maxiter': 1000})
            except:
                results = model.fit(disp='off', show_warning=False)
            
            # Debug print
            VolatilityModels.print_all_params(results, "EGARCH")
            
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
        """Extract model parameters - handles all parameter names"""
        try:
            params = results.params
            std_err = results.std_err
            
            print(f"\nEXTRACTING PARAMETERS FROM {len(params)} available parameters")
            print(f"Available parameter names: {list(params.index)}")
            
            # Get Omega
            omega = None
            omega_se = None
            omega_key = None
            
            for key in ['Constant', 'const', 'mu', 'omega']:
                if key in params:
                    omega = float(params[key])
                    omega_se = float(std_err[key])
                    omega_key = key
                    print(f"✓ Found Omega as: {key}")
                    break
            
            if omega is None and len(params) > 0:
                try:
                    omega = float(params.iloc[0])
                    omega_se = float(std_err.iloc[0])
                    omega_key = params.index[0]
                    print(f"✓ Found Omega as first parameter: {omega_key}")
                except:
                    pass
            
            # Get Alpha
            alpha = None
            alpha_se = None
            for key in params.index:
                if 'alpha' in str(key).lower():
                    alpha = float(params[key])
                    alpha_se = float(std_err[key])
                    print(f"✓ Found Alpha as: {key}")
                    break
            
            # Get Beta
            beta = None
            beta_se = None
            for key in params.index:
                if 'beta' in str(key).lower():
                    beta = float(params[key])
                    beta_se = float(std_err[key])
                    print(f"✓ Found Beta as: {key}")
                    break
            
            # Get Gamma - COMPREHENSIVE SEARCH
            gamma = None
            gamma_se = None
            gamma_found = False
            
            print(f"\nSearching for Gamma parameter...")
            for key in params.index:
                key_lower = str(key).lower()
                print(f"  Checking: {key} (lower: {key_lower})")
                
                # Try all possible gamma-related names
                gamma_names = ['gamma', 'leverage', 'asymmetry', 'skew', 'news', 'arch_in_mean']
                if any(gname in key_lower for gname in gamma_names):
                    try:
                        gamma = float(params[key])
                        gamma_se = float(std_err[key])
                        print(f"✓ Found Gamma as: {key} = {gamma}")
                        gamma_found = True
                        break
                    except Exception as e:
                        print(f"  Error extracting {key}: {e}")
                        continue
            
            if not gamma_found:
                print(f"✗ Gamma parameter not found in results")
                print(f"  Total parameters: {len(params)}")
                print(f"  Parameter list: {list(params.index)}")
            
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
