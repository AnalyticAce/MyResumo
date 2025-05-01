"""Token usage API router.

This module provides API endpoints for accessing token usage data
and analytics for OpenAI API calls throughout the application.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, List, Optional

from app.database.models.token_usage import TokenUsageSummary
from app.utils.token_tracker import TokenTracker

router = APIRouter(
    prefix="/api/token-usage",
    tags=["token-usage"],
    responses={404: {"description": "Not found"}},
)


@router.get("/summary", response_model=TokenUsageSummary)
async def get_token_usage_summary(
    days: int = Query(30, description="Number of days to include in the summary"),
    feature: Optional[str] = Query(None, description="Filter by specific feature (optional)"),
    user_id: Optional[str] = Query(None, description="Filter by specific user (optional)"),
) -> TokenUsageSummary:
    """Get a summary of token usage statistics.
    
    This endpoint provides aggregate token usage statistics including
    total tokens consumed, estimated costs, and breakdowns by model and feature.
    
    Args:
        days: Number of days to include in the summary (default: 30)
        feature: Filter by specific feature (optional)
        user_id: Filter by specific user (optional)
        
    Returns:
        TokenUsageSummary: Summary of token usage statistics
    """
    try:
        summary = TokenTracker.get_usage_summary(
            days=days,
            feature=feature,
            user_id=user_id,
        )
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating token usage summary: {str(e)}"
        )


@router.get("/export")
async def export_token_usage_data(
    format: str = Query("json", description="Output format ('json' or 'dict')")
) -> Dict:
    """Export token usage data for external analysis.
    
    This endpoint provides detailed token usage data in either JSON or dictionary format,
    suitable for export and further analysis.
    
    Args:
        format: Output format ('json' or 'dict')
        
    Returns:
        Raw token usage data in the requested format
    """
    try:
        data = TokenTracker.export_usage_data(format=format)
        return {"data": data}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error exporting token usage data: {str(e)}"
        )


@router.get("/pricing")
async def get_model_pricing() -> Dict:
    """Get the current pricing for different OpenAI models.
    
    This endpoint returns the pricing information used by the token tracker
    to calculate estimated costs.
    
    Returns:
        Dict: Model pricing information
    """
    from app.utils.token_tracker import MODEL_PRICING
    
    return {
        "model_pricing": MODEL_PRICING,
        "note": "Prices are in USD per 1000 tokens"
    }