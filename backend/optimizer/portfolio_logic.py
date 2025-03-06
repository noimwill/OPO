# optimizer/portfolio_logic.py
import numpy as np
import cvxpy as cp

def mean_variance_optimization(expected_returns, cov_matrix, risk_tolerance):
    """
    Performs mean-variance portfolio optimization.
    
    Parameters:
    expected_returns (np.array): Expected returns for each asset
    cov_matrix (np.array): Covariance matrix of returns
    risk_tolerance (float): Between 0 and 1, where 0 is minimum risk, 1 is maximum return
    
    Returns:
    dict: Optimized weights, expected return, risk, and Sharpe ratio
    """
    n = len(expected_returns)
    
    # Define variables
    weights = cp.Variable(n)
    
    # Define objective for risk-adjusted return (quadratic utility function)
    # Higher risk_tolerance means more focus on return vs. risk
    risk_aversion = 1 - risk_tolerance  # Convert risk_tolerance to risk_aversion parameter
    returns = expected_returns @ weights
    risk = cp.quad_form(weights, cov_matrix)
    objective = cp.Maximize(returns - risk_aversion * risk)
    
    # Define constraints
    constraints = [
        cp.sum(weights) == 1,  # Fully invested
        weights >= 0  # No short-selling
    ]
    
    # Solve the optimization problem
    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    # Check if the problem was solved successfully
    if problem.status != cp.OPTIMAL:
        return {"error": "Optimization problem could not be solved."}
    
    # Calculate metrics
    optimized_weights = weights.value
    expected_portfolio_return = float(expected_returns @ optimized_weights)
    expected_portfolio_risk = float(np.sqrt(optimized_weights @ cov_matrix @ optimized_weights))
    sharpe_ratio = expected_portfolio_return / expected_portfolio_risk if expected_portfolio_risk > 0 else 0
    
    # Round values for better readability
    optimized_weights = np.round(optimized_weights, 4)
    
    return {
        "weights": optimized_weights,
        "expected_return": round(expected_portfolio_return, 4),
        "expected_risk": round(expected_portfolio_risk, 4),
        "sharpe_ratio": round(sharpe_ratio, 4)
    }

def get_mock_market_data(assets):
    """
    Generate mock market data for demonstration purposes.
    In a real application, this would be fetched from a market data API.
    
    Parameters:
    assets (list): List of asset symbols
    
    Returns:
    tuple: (expected_returns, covariance_matrix)
    """
    # Mock expected annual returns for common assets
    returns_data = {
        'BTC': 0.20,
        'ETH': 0.25,
        'SOL': 0.30,
        'AVAX': 0.22,
        'BNB': 0.18,
        'USDC': 0.04,
        'USDT': 0.04,
        'DAI': 0.04,
        'LINK': 0.15,
        'DOT': 0.17,
        'ADA': 0.16,
        'XRP': 0.13,
        'MATIC': 0.23,
        'DOGE': 0.10,
        'UNI': 0.14,
        'SHIB': 0.08,
        'AAVE': 0.19,
        'MKR': 0.21
    }
    
    # Default for assets not in our mock data
    default_return = 0.15
    
    # Create expected returns vector
    expected_returns = np.array([returns_data.get(asset, default_return) for asset in assets])
    
    # Generate a realistic covariance matrix
    n = len(assets)
    
    # Base volatilities (standard deviations)
    volatilities = np.array([
        0.80 if asset in ['BTC', 'ETH', 'SOL', 'AVAX', 'DOGE', 'SHIB'] else
        0.60 if asset in ['BNB', 'LINK', 'DOT', 'ADA', 'XRP', 'MATIC', 'UNI', 'AAVE', 'MKR'] else
        0.05 if asset in ['USDC', 'USDT', 'DAI'] else
        0.50  # default
        for asset in assets
    ])
    
    # Correlation matrix (simplified)
    # Higher correlation between similar asset types
    correlation = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                correlation[i, j] = 1.0
            elif (assets[i] in ['USDC', 'USDT', 'DAI']) and (assets[j] in ['USDC', 'USDT', 'DAI']):
                correlation[i, j] = 0.95  # Stablecoins highly correlated
            elif (assets[i] in ['BTC', 'ETH']) and (assets[j] in ['BTC', 'ETH']):
                correlation[i, j] = 0.80  # Major cryptos correlated
            else:
                correlation[i, j] = 0.50  # Base correlation
            
            # Ensure symmetry
            correlation[j, i] = correlation[i, j]
    
    # Create covariance matrix from correlation and volatilities
    cov_matrix = np.outer(volatilities, volatilities) * correlation
    
    return expected_returns, cov_matrix