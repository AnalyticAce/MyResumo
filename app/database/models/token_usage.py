"""Token usage tracking model for LLM API calls.

This module provides the TokenUsage model for tracking and analyzing
token consumption across OpenAI API calls throughout the application.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from app.database.models.base import BaseSchema


class TokenUsage(BaseSchema):
    """Model for tracking token usage in LLM API calls.

    This model stores detailed information about token consumption
    for each API call, including prompt tokens, completion tokens,
    total tokens, model used, and metadata about the request context.

    Attributes:
        id: Unique identifier for the token usage record
        timestamp: When the API call was made
        endpoint: The specific API endpoint or function that was called
        model_name: The name of the LLM model used (e.g., "gpt-3.5-turbo")
        prompt_tokens: Number of tokens used in the prompt/input
        completion_tokens: Number of tokens used in the completion/output
        total_tokens: Total tokens used (prompt + completion)
        request_id: Optional request ID for correlation
        user_id: Optional ID of the user who triggered the request
        feature: The feature or component using the API (e.g., "resume_optimization")
        status: Success or error status of the API call
        cost_usd: Estimated cost in USD based on token usage and model pricing
        metadata: Additional context about the request (optional JSON data)
    """

    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    endpoint: str
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    feature: str
    status: str = "success"
    cost_usd: float
    metadata: Optional[dict] = None


class TokenUsageSummary(BaseSchema):
    """Summary model for aggregated token usage statistics.

    This model provides aggregated views of token usage for reporting
    and analytics purposes.

    Attributes:
        total_api_calls: Total number of API calls made
        total_prompt_tokens: Total prompt tokens consumed
        total_completion_tokens: Total completion tokens consumed
        total_tokens: Total tokens consumed
        total_cost_usd: Total estimated cost in USD
        period_start: Start of the reporting period
        period_end: End of the reporting period
        usage_by_model: Breakdown of usage by model
        usage_by_feature: Breakdown of usage by feature
    """

    total_api_calls: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    total_cost_usd: float
    period_start: datetime
    period_end: datetime
    usage_by_model: dict
    usage_by_feature: dict