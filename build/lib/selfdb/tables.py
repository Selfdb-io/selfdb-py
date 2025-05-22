"""
Table operations for SelfDB client.
"""

from typing import Dict, Any, List, Optional, Union


def list_tables_method(self) -> List[Dict[str, Any]]:
    """
    List all tables in the database.
    
    Returns:
    --------
    list
        List of table information dictionaries
    """
    return self._request("get", "/tables")


def get_table_method(self, table_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific table.
    
    Parameters:
    -----------
    table_name : str
        Name of the table
    
    Returns:
    --------
    dict
        Table information including columns, constraints, etc.
    """
    return self._request("get", f"/tables/{table_name}")


def create_table_method(self, 
                     name: str, 
                     columns: List[Dict[str, Any]], 
                     description: Optional[str] = None,
                     if_not_exists: bool = False) -> Dict[str, Any]:
    """
    Create a new table.
    
    Parameters:
    -----------
    name : str
        Name of the table
    columns : list of dict
        List of column definitions
        Example: [
            {
                "name": "id",
                "type": "serial",
                "nullable": False,
                "primary_key": True
            },
            {
                "name": "name",
                "type": "varchar(100)",
                "nullable": False
            }
        ]
    description : str, optional
        Table description
    if_not_exists : bool, optional
        Whether to use IF NOT EXISTS clause, by default False
    
    Returns:
    --------
    dict
        Created table information
    """
    data = {
        "name": name,
        "columns": columns,
        "if_not_exists": if_not_exists
    }
    if description:
        data["description"] = description
        
    return self._request("post", "/tables", json=data)


def update_table_method(self, 
                      table_name: str, 
                      new_name: Optional[str] = None,
                      description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a table's properties.
    
    Parameters:
    -----------
    table_name : str
        Current table name
    new_name : str, optional
        New table name
    description : str, optional
        Table description
    
    Returns:
    --------
    dict
        Updated table information
    """
    data = {}
    if new_name:
        data["new_name"] = new_name
    if description:
        data["description"] = description
        
    return self._request("put", f"/tables/{table_name}", json=data)


def delete_table_method(self, table_name: str) -> Dict[str, Any]:
    """
    Delete a table.
    
    Parameters:
    -----------
    table_name : str
        Name of the table to delete
    
    Returns:
    --------
    dict
        Success message
    """
    return self._request("delete", f"/tables/{table_name}")


def get_table_data_method(self, 
                       table_name: str, 
                       page: int = 1, 
                       page_size: int = 50,
                       order_by: Optional[str] = None,
                       filter_column: Optional[str] = None,
                       filter_value: Optional[str] = None) -> Dict[str, Any]:
    """
    Get data from a table with pagination and filtering.
    
    Parameters:
    -----------
    table_name : str
        Name of the table
    page : int, optional
        Page number, by default 1
    page_size : int, optional
        Number of records per page, by default 50
    order_by : str, optional
        Column to order by, e.g., "column_name ASC" or "column_name DESC"
    filter_column : str, optional
        Column to filter by
    filter_value : str, optional
        Value to filter by
    
    Returns:
    --------
    dict
        Table data with pagination metadata
    """
    params = {
        "page": page,
        "page_size": page_size
    }
    if order_by:
        params["order_by"] = order_by
    if filter_column and filter_value is not None:
        params["filter_column"] = filter_column
        params["filter_value"] = filter_value
        
    return self._request("get", f"/tables/{table_name}/data", params=params)


def insert_table_data_method(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert data into a table.
    
    Parameters:
    -----------
    table_name : str
        Name of the table
    data : dict
        Data to insert as key-value pairs
    
    Returns:
    --------
    dict
        Inserted row data
    """
    return self._request("post", f"/tables/{table_name}/data", json=data)


def update_table_data_method(self, 
                          table_name: str, 
                          id: Union[str, int],
                          id_column: str,
                          data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a specific row in a table.
    
    Parameters:
    -----------
    table_name : str
        Name of the table
    id : str or int
        ID of the row to update
    id_column : str
        Name of the primary key column
    data : dict
        Updated row data
    
    Returns:
    --------
    dict
        Updated row data
    """
    params = {"id_column": id_column}
    return self._request(
        "put", 
        f"/tables/{table_name}/data/{id}", 
        params=params, 
        json=data
    )


def delete_table_data_method(self, 
                           table_name: str, 
                           id: Union[str, int],
                           id_column: str) -> Dict[str, Any]:
    """
    Delete a specific row from a table.
    
    Parameters:
    -----------
    table_name : str
        Name of the table
    id : str or int
        ID of the row to delete
    id_column : str
        Name of the primary key column
    
    Returns:
    --------
    dict
        Success message
    """
    params = {"id_column": id_column}
    return self._request("delete", f"/tables/{table_name}/data/{id}", params=params)