# SelfDB Python Client

A Python client library for interacting with SelfDB.

## Installation

```bash
pip install selfdb
```

## Configuration

You can configure the client using environment variables:

### Sample .env File

Create a `.env` file in your project directory with the following content:

```
# SelfDB Python Client Environment Variables
baseurl="http://localhost:8000/api/v1"
anon-key="3f09464d7930d7f89f53b121bf21f03627bf89d24b1a5f25258e4632245d99b6"
storageurl="http://localhost:8001"
```

Then load them in your code:

```python
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

from selfdb import SelfDBClient

# Initialize client with config from environment
client = SelfDBClient(
    baseurl=os.getenv("baseurl"),
    anon_key=os.getenv("anon-key"),
    storageurl=os.getenv("storageurl")
)
```

## Usage

### Basic Setup

```python
from selfdb import SelfDB

# Initialize client with your SelfDB URL and anonymous key
selfdb = SelfDB(
    baseurl="http://localhost:8000/api/v1",
    anon_key="your-anon-key",
    storageurl="http://localhost:8001"  # Optional: URL to storage service
)

# Authenticate with email/password
selfdb.auth.sign_in_with_password("user@example.com", "password")
print(selfdb.auth.user_info)  # Contains user_id, email, is_superuser
```

### Authentication

```python
# Sign in with email & password
selfdb.auth.sign_in_with_password("user@example.com", "password")

# Register a new user
selfdb.auth.sign_up("new-user@example.com", "password")

# Refresh tokens
selfdb.auth.refresh()

# Logout (clears credentials)
selfdb.auth.sign_out()

# Set anonymous key for public access
selfdb.auth.set_anon_key("your-anon-key")
```

### Table Operations

```python
# Direct table methods
t = selfdb.list_tables()
new_table = selfdb.create_table(
    name="products",
    columns=[
        {"name": "id", "type": "serial", "nullable": False, "primary_key": True},
        {"name": "name", "type": "varchar(100)", "nullable": False},
        {"name": "price", "type": "decimal(10,2)", "nullable": False},
        {"name": "created_at", "type": "timestamp", "nullable": True, "default": "CURRENT_TIMESTAMP"},
    ],
    description="Product catalog",
    if_not_exists=True
)

# Fluent query builder
inserted = selfdb.table("products").insert({"name": "Example", "price": 29.99}).execute()
rows = selfdb.table("products")\
    .select("*")\
    .filter("price", "eq", 29.99)\
    .order("name ASC")\
    .limit(10)\
    .execute()

# Direct CRUD operations
data_page = selfdb.get_table_data("products", page=1, page_size=10, order_by="name ASC", filter_column="price", filter_value=29.99)
updated = selfdb.update_table_data("products", id=1, id_column="id", data={"price": 39.99})
selfdb.delete_table_data("products", id=2, id_column="id")
```

### Storage Operations

```python
# List buckets
buckets = selfdb.list_buckets()

# Create a new bucket
new_bucket = selfdb.create_bucket("my-files", is_public=True)

# Upload a file (presigned URL)
upload_meta = selfdb.upload_file(bucket_id="my-files", file_path="path/to/local/file.jpg")

# Download a file (to disk or get bytes)
content = selfdb.download_file(bucket_id="my-files", file_id="file-id")
file_path = selfdb.download_file(bucket_id="my-files", file_id="file-id", output_path="downloaded.jpg")
```

### Functions

```python
# Invoke a server-side function
result = selfdb.invoke_function("calculate_tax", {"product_id": 123, "quantity": 3})
```

## Sample Applications

Check the `samples` directory for example applications:
- `basic_usage.py`: Basic client usage with table operations
- `storage_demo.py`: Storage operations demonstration
- `create_user.py`: User registration example

## Error Handling

The library provides specific exception types:
- `AuthenticationError`: Authentication issues
- `ResourceNotFoundError`: Resource not found
- `ValidationError`: Input validation problems
- `APIError`: General API errors

```python
from selfdb.exceptions import AuthenticationError, ResourceNotFoundError

try:
    client.login("user@example.com", "wrong-password")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## License

This project is licensed under the terms of the LICENSE.md file.