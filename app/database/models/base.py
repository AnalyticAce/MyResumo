"""Base model module for shared model functionality.

This module provides the BaseSchema class which serves as the foundation
for all models in the application, ensuring consistent configuration and behavior.
"""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base Pydantic model class for all application schemas.

    This base class provides common configuration and functionality
    shared across all model classes in the application.
    """

    class Config:
        """Configuration for Pydantic model behavior.

        This configuration enables ORM mode (from_attributes), allows
        population by field name, and configures other shared model behaviors.
        """

        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
