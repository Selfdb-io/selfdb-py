"""
SelfDB Python Client - Storage Demo

This sample demonstrates using the storage capabilities of the SelfDB Python client.
"""

import os
import sys
import time
import dotenv

# Load .env file
dotenv.load_dotenv()

# Add the parent directory to the path for importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selfdb import SelfDB

def main():
    # Initialize client with anonymous key and storage URL from .env file
    print("Initializing SelfDB client...")
    selfdb = SelfDB(
        baseurl=os.getenv("baseurl"),
        anon_key=os.getenv("anon-key"),
        storageurl=os.getenv("storageurl")
    )
    
    # Login with test credentials
    # You need to replace these with valid credentials or create a user first
    print("\nLogging in...")
    try:
        selfdb.auth.sign_in_with_password(email="user@example.com", password="password123")
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")
        print("Note: You must be authenticated to create buckets and upload files.")
    
    # Storage operations - Note: This requires authentication
    bucket_name = f"demo-bucket-{int(time.time())}"
    try:
        print(f"\nCreating storage bucket '{bucket_name}'...")
        # Make sure you're authenticated with superuser privileges
        result = selfdb.create_bucket(name=bucket_name, is_public=True)
        print(f"Bucket created with ID: {result.get('id', 'unknown')}")
    except Exception as e:
        print(f"Error creating bucket: {e}")
        print("Note: Bucket creation requires authentication with superuser privileges.")
        print("Will try to use existing buckets instead...")
    
    # List buckets
    try:
        print("\nListing storage buckets:")
        buckets = selfdb.list_buckets()
        for bucket in buckets:
            print(f"- {bucket['name']} (Public: {bucket.get('is_public', False)})")
    except Exception as e:
        print(f"Error listing buckets: {e}")
    
    # Create a temporary file to upload
    try:
        test_file = "test_upload.txt"
        with open(test_file, "w") as f:
            f.write("This is a test file for SelfDB storage.")
        
        print(f"\nUploading file to bucket '{bucket_name}'...")
        # First we need to check if we have at least one bucket available
        buckets = selfdb.list_buckets()
        if not buckets:
            print("No buckets available. You need at least one bucket to upload files.")
            raise ValueError("No buckets available")
        
        # Use the first bucket if the one we tried to create doesn't exist
        use_bucket = bucket_name
        if not any(b['name'] == bucket_name for b in buckets):
            use_bucket = buckets[0]['name']
            print(f"Using existing bucket: {use_bucket}")
        
        # Upload the file using the new two-step process (initiate + upload)
        print(f"Initiating upload and uploading file to bucket '{use_bucket}'...")
        file_result = selfdb.upload_file(
            bucket_id=use_bucket,
            file_path=test_file
        )
        print(f"File uploaded successfully: {file_result.get('filename', 'unknown')}")
        
        # Get the file ID from the metadata
        file_id = file_result.get('id')
        if not file_id:
            print("Warning: Couldn't get file ID from response. Using filename as fallback.")
            file_id = file_result.get('filename', 'test_upload.txt')
            
        # Download the file
        print(f"\nDownloading file with ID: {file_id}...")
        output_file = "test_download.txt"
        selfdb.download_file(
            bucket_id=use_bucket,
            file_id=file_id,
            output_path=output_file
        )
        print(f"File downloaded to: {output_file}")
        
        # Read the downloaded file
        with open(output_file, 'r') as f:
            content = f.read()
            print(f"File content: {content}")
        
        # Cleanup
        os.remove(test_file)
        os.remove(output_file)
    except Exception as e:
        print(f"Error handling file: {e}")
        print(f"Detailed error information: {type(e).__name__}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main()