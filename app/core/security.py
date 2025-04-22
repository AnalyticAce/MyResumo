"""Security module for authentication and authorization functionality.

This module provides security-related utilities, authentication functions,
and authorization mechanisms used throughout the application to protect
routes, validate tokens, and manage user access.
"""

import bcrypt

if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})
