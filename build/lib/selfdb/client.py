"""
Unified SelfDB Python Client.
"""

import requests
from urllib.parse import urljoin
from typing import Optional, Dict, Any, Union

from .auth import AuthClient
from .storage import StorageClient
from .query import TableQueryBuilder
from .functions import FunctionsClient
from .exceptions import APIError, AuthenticationError, ResourceNotFoundError, ValidationError


class SelfDB:
    """
    Unified SelfDB Client.
    """
    def __init__(
        self,
        baseurl: str,
        anon_key: Optional[str] = None,
        storageurl: Optional[str] = None,
    ):
        # Base API URL
        self.base_url = baseurl.rstrip("/")
        if not self.base_url.endswith("/api/v1"):
            self.base_url = urljoin(self.base_url, "/api/v1")
        # Anonymous key
        self.anon_key = anon_key
        # Storage URL
        if storageurl:
            self.storage_url = storageurl.rstrip("/")
        else:
            base_server = "/".join(self.base_url.split("/")[:-2])
            self.storage_url = urljoin(base_server, "/storage")
        # HTTP session
        self.session = requests.Session()
        # Sub-clients
        self.auth = AuthClient(self)
        self.storage = StorageClient(self)
        self.functions = FunctionsClient(self)

    def _get_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.auth.access_token:
            headers["Authorization"] = f"Bearer {self.auth.access_token}"
        if self.anon_key:
            headers["apikey"] = self.anon_key
        return headers

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None,
        json: Any = None,
        headers: Optional[Dict[str, str]] = None,
        files: Any = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        request_headers = self._get_headers()
        if headers:
            request_headers.update(headers)
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=request_headers,
            files=files,
        )
        if response.ok:
            if response.status_code == 204:
                return None
            try:
                return response.json()
            except ValueError:
                return response.content
        # Error handling
        status = response.status_code
        if status == 401:
            raise AuthenticationError("Authentication failed")
        if status == 404:
            raise ResourceNotFoundError(f"Resource not found: {path}")
        if status == 422:
            raise ValidationError(response.text)
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise APIError(status, detail, response)

    def table(self, table_name: str) -> TableQueryBuilder:
        """Start a fluent query builder for a table."""
        return TableQueryBuilder(self, table_name)

    def invoke_function(self, name: str, payload: Dict[str, Any]) -> Any:
        """Invoke a server-side function."""
        return self.functions.invoke(name, payload)

    # Table management
    def list_tables(self) -> Any:
        return self._request("get", "/tables")

    def create_table(
        self,
        name: str,
        columns: Any,
        description: Optional[str] = None,
        if_not_exists: bool = False,
    ) -> Any:
        data = {"name": name, "columns": columns, "if_not_exists": if_not_exists}
        if description:
            data["description"] = description
        return self._request("post", "/tables", json=data)

    # Direct CRUD operations
    def get_table_data(self, table_name: str, **kwargs: Any) -> Any:
        return self._request("get", f"/tables/{table_name}/data", params=kwargs)

    def insert_table_data(self, table_name: str, data: Dict[str, Any]) -> Any:
        return self._request("post", f"/tables/{table_name}/data", json=data)

    def update_table_data(
        self,
        table_name: str,
        id: Union[str, int],
        id_column: str,
        data: Dict[str, Any],
    ) -> Any:
        params = {"id_column": id_column}
        return self._request(
            "put", f"/tables/{table_name}/data/{id}", params=params, json=data
        )

    def delete_table_data(
        self,
        table_name: str,
        id: Union[str, int],
        id_column: str,
    ) -> Any:
        params = {"id_column": id_column}
        return self._request(
            "delete", f"/tables/{table_name}/data/{id}", params=params
        )

    # Storage aliases
    def list_buckets(self) -> Any:
        return self._request("get", "/buckets")

    def create_bucket(self, name: str, is_public: bool = True) -> Any:
        data = {"name": name, "is_public": is_public}
        return self._request("post", "/buckets", json=data)

    def upload_file(
        self,
        bucket_id: str,
        file_path: Optional[str] = None,
        file_content: Any = None,
        file_name: Optional[str] = None,
    ) -> Any:
        return self.storage.from_(bucket_id).upload(
            file_path=file_path, file_content=file_content, file_name=file_name
        )

    def download_file(
        self,
        bucket_id: str,
        file_id: str,
        output_path: Optional[str] = None,
    ) -> Any:
        return self.storage.from_(bucket_id).download(file_id, output_path)
