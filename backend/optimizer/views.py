# optimizer/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from .portfolio_logic import mean_variance_optimization, get_mock_market_data

@api_view(['POST'])
def optimize_portfolio(request):
    """
    API endpoint for portfolio optimization.
    
    Expected request data:
    {
        "assets": ["BTC", "ETH", "SOL", "USDC", ...],
        "risk_tolerance": 0.5,  # Value between 0 and 1
        "initial_weights": [0.25, 0.25, 0.25, 0.25]  # Optional
    }
    """
    try:
        # Extract data from request
        data = request.data
        assets = data.get('assets', [])
        risk_tolerance = data.get('risk_tolerance', 0.5)
        
        # Validate inputs
        if not assets:
            return Response(
                {"error": "At least one asset must be provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not 0 <= risk_tolerance <= 1:
            return Response(
                {"error": "Risk tolerance must be between 0 and 1"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get market data (in a real application, this would be fetched from a data provider)
        expected_returns, cov_matrix = get_mock_market_data(assets)
        
        # Run optimization
        optimization_result = mean_variance_optimization(
            expected_returns, 
            cov_matrix, 
            risk_tolerance
        )
        
        # Check for optimization errors
        if "error" in optimization_result:
            return Response(
                optimization_result, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Format the response
        weights = optimization_result["weights"]
        optimized_allocations = {asset: float(weight) for asset, weight in zip(assets, weights)}
        
        response = {
            "optimized_allocations": optimized_allocations,
            "expected_return": optimization_result["expected_return"],
            "expected_risk": optimization_result["expected_risk"],
            "sharpe_ratio": optimization_result["sharpe_ratio"]
        }
        
        return Response(response)
        
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )