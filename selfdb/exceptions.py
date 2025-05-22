"""
Custom exceptions for the SelfDB client library.
"""


class SelfDBException(Exception):
    """Base exception for SelfDB client errors."""
    pass


class AuthenticationError(SelfDBException):
    """Raised when authentication fails."""
    pass


class ResourceNotFoundError(SelfDBException):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(SelfDBException):
    """Raised when request validation fails."""
    pass


class APIError(SelfDBException):
    """Raised when the SelfDB API returns an error."""
    
    def __init__(self, status_code, message, response=None):
        self.status_code = status_code
        self.response = response
        super().__init__(f"API Error ({status_code}): {message}")