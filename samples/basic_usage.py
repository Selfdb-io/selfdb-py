"""
SelfDB Python Client - Basic Usage Example

This sample demonstrates basic usage of the SelfDB Python client library.
"""

import os
import sys
import time
import dotenv
from pydantic import BaseModel
from typing import List, Optional

# Load .env file
dotenv.load_dotenv()

# Add the parent directory to the path for importing the library
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selfdb import SelfDB

class Column(BaseModel):
    name: str
    type: str
    nullable: bool
    primary_key: bool = False
    default: Optional[str] = None

class CreateTableSchema(BaseModel):
    name: str
    columns: List[Column]
    if_not_exists: bool = False
    description: Optional[str] = None

def main():
    # Initialize client with anonymous key from .env file
    print("Initializing SelfDB client...")
    selfdb = SelfDB(
        baseurl=os.getenv("baseurl", "http://localhost:8000/api/v1"),
        anon_key=os.getenv("anon-key")
    )
    
    # Login with test credentials
    # You need to replace these with valid credentials or create a user first
    print("\nLogging in...")
    try:
        selfdb.auth.sign_in_with_password(email="user@example.com", password="password123")
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")
        print("Continuing with anonymous access...")
    
    
    # List tables
    try:
        print("\nListing tables:")
        tables = selfdb.list_tables()
        for table in tables:
            print(f"- {table['name']}")
    except Exception as e:
        print(f"Error listing tables: {e}")
    
    # Create a simple table
    table_name = f"demo_table_{int(time.time())}"
    table_schema = CreateTableSchema(
        name=table_name,
        columns=[
            Column(name="id", type="serial", nullable=False, primary_key=True),
            Column(name="name", type="varchar(100)", nullable=False),
            Column(name="created_at", type="timestamp", nullable=True, default="CURRENT_TIMESTAMP"),
        ],
        if_not_exists=True,
        description="Demo table created by SelfDB Python client"
    )
    try:
        print(f"\nCreating table '{table_name}'...")
        selfdb.create_table(**table_schema.dict())
        print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
        print(f"Will try to continue with other operations...")
    
    # Insert data using fluent builder
    try:
        print(f"\nInserting data into '{table_name}'...")
        for i in range(1, 4):
            result = selfdb.table(table_name).insert({"name": f"Item {i}"}).execute()
            print(f"Inserted item with ID: {result.get('id', 'unknown')}")
    except Exception as e:
        print(f"Error inserting data: {e}")
    
    # Query data using fluent builder
    try:
        print(f"\nQuerying data from '{table_name}':")
        response = selfdb.table(table_name).select("*").execute()
        print(f"Total records: {response['metadata']['total_count']}")
        for item in response["data"]:
            print(f"- ID: {item['id']}, Name: {item['name']}, Created: {item['created_at']}")
    except Exception as e:
        print(f"Error querying data: {e}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main()