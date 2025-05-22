"""
Fluent query builder for table-level CRUD operations.
"""
from typing import Any, Dict, Optional


class TableQueryBuilder:
    """Build and execute queries on a specific table using fluent interface."""
    def __init__(self, client, table_name: str):
        self._client = client
        self._table = table_name
        self._select_fields: Optional[str] = None
        self._filters: list = []
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None
        self._page: Optional[int] = None
        self._page_size: Optional[int] = None
        self._insert_data: Optional[Dict[str, Any]] = None

    def select(self, columns: str) -> 'TableQueryBuilder':
        """Specify columns to select, e.g. '*', 'id,name'."""
        self._select_fields = columns
        return self

    def filter(self, column: str, operator: str, value: Any) -> 'TableQueryBuilder':
        """Add a filter clause. Currently only 'eq' is supported."""
        if operator != 'eq':
            raise NotImplementedError("Only 'eq' operator is supported for now.")
        self._filters.append((column, value))
        return self

    def order(self, order_by: str) -> 'TableQueryBuilder':
        """Specify ORDER BY clause, e.g. 'id ASC'."""
        self._order_by = order_by
        return self

    def limit(self, limit: int) -> 'TableQueryBuilder':
        """Limit the number of records returned."""
        self._limit = limit
        return self

    def paginate(self, page_size: int) -> 'TableQueryBuilder':
        """Start pagination with specific page size."""
        self._page_size = page_size
        self._page = 1
        return self

    def page(self, page: int) -> 'TableQueryBuilder':
        """Jump to a specific page in pagination."""
        self._page = page
        return self

    def insert(self, data: Dict[str, Any]) -> 'TableQueryBuilder':
        """Insert a new record into the table."""
        self._insert_data = data
        return self

    def execute(self) -> Any:
        """Execute the built query or mutation."""
        # Handle insert
        if self._insert_data is not None:
            return self._client._request(
                "post", f"/tables/{self._table}/data", json=self._insert_data
            )
        # Build params for select
        params: Dict[str, Any] = {}
        if self._page is not None:
            params['page'] = self._page
        if self._page_size is not None:
            params['page_size'] = self._page_size
        if self._order_by:
            params['order_by'] = self._order_by
        if self._limit is not None:
            params['limit'] = self._limit
        # Use only the last filter
        if self._filters:
            column, value = self._filters[-1]
            params['filter_column'] = column
            params['filter_value'] = value
        return self._client._request(
            "get", f"/tables/{self._table}/data", params=params
        ) 