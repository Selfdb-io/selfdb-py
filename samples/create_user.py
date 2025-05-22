"""
SelfDB Python Client - Create User

This sample demonstrates creating a user for testing purposes.
"""

import os
import sys
import dotenv

# Load .env file
dotenv.load_dotenv()

# Add the parent directory to the path for importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selfdb import SelfDB
from selfdb.exceptions import SelfDBException

def main():
    # Initialize client with anonymous key
    print("Initializing SelfDB client...")
    selfdb = SelfDB(
        baseurl=os.getenv("baseurl", "http://localhost:8000/api/v1"),
        anon_key=os.getenv("anon-key")
    )
    
    # Register a new test user
    try:
        print("\nCreating a test user...")
        user = selfdb.auth.sign_up(
            email="user@example.com",
            password="password123",
            full_name="Test User"
        )
        print(f"User created successfully: {user.get('email')}")
    except SelfDBException as e:
        if "already exists" in str(e):
            print("User already exists. Try logging in with these credentials.")
        else:
            print(f"Failed to create user: {e}")
    
    # Try to login with the newly created user
    try:
        print("\nTesting login...")
        result = selfdb.auth.sign_in_with_password(email="user@example.com", password="password123")
        print("Login successful!")
        print(f"User details: {result.get('email')} (ID: {result.get('user_id')})")
        print(f"Access token: {selfdb.auth.access_token[:20]}... (truncated)")
        print(f"Refresh token: {selfdb.auth.refresh_token[:20]}... (truncated)")
    except Exception as e:
        print(f"Login failed: {e}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main()
