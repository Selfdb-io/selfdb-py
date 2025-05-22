"""
Functions client for SelfDB.
"""
from typing import Any, Dict


class FunctionsClient:
    """Client for invoking server-side functions."""
    def __init__(self, client):
        self._client = client

    def invoke(self, name: str, payload: Dict[str, Any]) -> Any:
        """Invoke a named function with a JSON payload."""
        return self._client._request("post", f"/functions/{name}", json=payload) 