"""
Authentication client for SelfDB.
"""
import datetime
from typing import Dict, Any

from .exceptions import AuthenticationError


class AuthClient:
    """Authentication client for managing SelfDB user sessions."""
    def __init__(self, client):
        self._client = client
        self.access_token: str = None  # type: ignore
        self.refresh_token: str = None  # type: ignore
        self.token_expires_at: datetime.datetime = None  # type: ignore
        self.user_info: Dict[str, Any] = {}

    def sign_in_with_password(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user with email and password.
        """
        data = {"username": email, "password": password}
        response = self._client._request(
            "post",
            "/auth/login",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self.access_token = response.get("access_token")
        self.refresh_token = response.get("refresh_token")
        self.token_expires_at = datetime.datetime.now() + datetime.timedelta(minutes=60)
        self.user_info = {
            "user_id": response.get("user_id"),
            "email": response.get("email"),
            "is_superuser": response.get("is_superuser"),
        }
        return response

    def sign_up(self, email: str, password: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Register a new user.
        """
        user_data = {"email": email, "password": password, **kwargs}
        return self._client._request("post", "/auth/register", json=user_data)

    def refresh(self) -> Dict[str, Any]:
        """
        Refresh the access token using the stored refresh token.
        """
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available. Please login first.")
        data = {"refresh_token": self.refresh_token}
        response = self._client._request("post", "/auth/refresh", json=data)
        self.access_token = response.get("access_token")
        self.refresh_token = response.get("refresh_token", self.refresh_token)
        self.token_expires_at = datetime.datetime.now() + datetime.timedelta(minutes=60)
        return response

    def sign_out(self) -> None:
        """
        Clear the current authentication session.
        """
        self.access_token = None  # type: ignore
        self.refresh_token = None  # type: ignore
        self.token_expires_at = None  # type: ignore
        self.user_info = {}

    def set_anon_key(self, anon_key: str) -> None:
        """
        Set or update the anonymous access key.
        """
        self._client.anon_key = anon_key