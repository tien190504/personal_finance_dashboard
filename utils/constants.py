"""
Constants for Asset Classes, Risk Levels, and Default Assumptions.
"""

ASSET_CONFIG = {
    "Savings": {
        "risk_level": "Low",
        "volatility": 0.01,  # 1%
        "expected_return": 0.04, # 4% APY
        "description": "High liquidity, capital preservation focus. FD/High-Yield Savings."
    },
    "Bonds": {
        "risk_level": "Low-Medium",
        "volatility": 0.05,
        "expected_return": 0.06,
        "description": "Fixed income securities, government/corporate bonds."
    },
    "Index Funds": {
        "risk_level": "Medium-High",
        "volatility": 0.15,
        "expected_return": 0.10, # S&P 500 historical avg
        "description": "Diversified equity exposure. S&P 500 / Total Market."
    },
    "Crypto": {
        "risk_level": "Very High",
        "volatility": 0.80,
        "expected_return": 0.15, # Higher reward potential, high variance
        "description": "Digital assets, high volatility, speculative."
    }
}
