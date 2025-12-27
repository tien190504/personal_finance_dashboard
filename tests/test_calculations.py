import pytest
import pandas as pd
from utils.calculations import calculate_compound_interest, calculate_risk_projection

def test_compound_interest_basic():
    # 1000 principal, 0 monthly, 10% rate, 1 year
    # Expected: 1100 approx
    df = calculate_compound_interest(1000, 0, 0.10, 1)
    
    assert not df.empty
    last_row = df.iloc[-1]
    # 1000 * 1.1 = 1100? No, monthly compounding is usually (1+r/12)^12
    # 1000 * (1 + 0.10/12)^12 approx 1104.71
    assert 1100 <= last_row['Balance'] <= 1105
    assert last_row['Year'] == 1

def test_compound_interest_with_contribution():
    # 0 principal, 100 monthly, 0% rate, 1 year
    # Expected: 1200
    df = calculate_compound_interest(0, 100, 0.0, 1)
    last_row = df.iloc[-1]
    assert last_row['Balance'] == 1200
    assert last_row['Total Principal'] == 1200

def test_risk_projection_shapes():
    p5, p50, p95 = calculate_risk_projection(1000, 10, 0.07, 0.15)
    assert p5 < p50 < p95
    assert p5 > 0  # Should be positive usually
