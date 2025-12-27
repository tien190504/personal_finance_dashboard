import numpy as np
import pandas as pd
from typing import Tuple, List

def calculate_compound_interest(
    principal: float,
    monthly_contribution: float,
    annual_rate: float,
    years: int
) -> pd.DataFrame:
    """
    Calculates the projected growth of an investment over time.
    
    Args:
        principal: Initial investment amount.
        monthly_contribution: Amount added each month.
        annual_rate: Expected annual return rate (as a decimal, e.g., 0.05 for 5%).
        years: Investment duration in years.
        
    Returns:
        pd.DataFrame: A DataFrame containing 'Year', 'Balance', 'Total Principal', and 'Interest'.
    """
    months = years * 12
    monthly_rate = annual_rate / 12
    
    data = []
    current_balance = principal
    total_principal = principal
    
    for month in range(1, months + 1):
        interest = current_balance * monthly_rate
        current_balance += interest + monthly_contribution
        total_principal += monthly_contribution
        
        if month % 12 == 0:
            data.append({
                "Year": month // 12,
                "Balance": round(current_balance, 2),
                "Total Principal": round(total_principal, 2),
                "Interest": round(current_balance - total_principal, 2)
            })
            
    return pd.DataFrame(data)

def calculate_risk_projection(
    principal: float,
    years: int,
    mean_return: float,
    volatility: float,
    simulations: int = 1000
) -> Tuple[float, float, float]:
    """
    Simulates investment returns using Monte Carlo to estimate risk ranges.
    
    Args:
        principal: Initial investment.
        years: Number of years.
        mean_return: Annual expected return (decimal).
        volatility: Annual standard deviation (volatility) (decimal).
        simulations: Number of simulations to run.
        
    Returns:
        Tuple[float, float, float]: (5th Percentile, Median, 95th Percentile) ending balances.
    """
    # Simple Geometric Brownian Motion
    dt = 1  # yearly steps
    returns = np.random.normal(
        (mean_return - 0.5 * volatility**2) * dt,
        volatility * np.sqrt(dt),
        (years, simulations)
    )
    
    # Cumulative returns
    price_paths = principal * np.exp(np.cumsum(returns, axis=0))
    
    final_values = price_paths[-1, :]
    
    return (
        np.percentile(final_values, 5),
        np.percentile(final_values, 50),
        np.percentile(final_values, 95)
    )
