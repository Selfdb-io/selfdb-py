"""
Storage client for SelfDB.
"""
from typing import Any, Dict, Optional, Union, BinaryIO, List
import os
import requests
from .exceptions import APIError
import uuid


class StorageClient:
    """Client for managing storage buckets and files."""
    def __init__(self, client):
        self._client = client

    def from_(self, bucket_id: str) -> 'Bucket':
        """Select a bucket by name or ID for file operations."""
        return Bucket(self._client, bucket_id)


class Bucket:
    """Fluent interface for file operations within a specific bucket."""
    def __init__(self, client, bucket_id: str):
        self._client = client
        self._bucket = bucket_id

    def upload(
        self,
        file_path: Optional[str] = None,
        file_content: Optional[BinaryIO] = None,
        file_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a file to the selected bucket using a presigned URL."""
        bucket_id = self._bucket
        # Resolve bucket name to UUID if needed
        try:
            uuid.UUID(str(bucket_id))
        except (ValueError, TypeError):
            # bucket_id might be a name; look up real UUID
            buckets = self._client.list_buckets()
            match = next((b for b in buckets if b.get('name') == bucket_id), None)
            if not match:
                raise ValueError(f"No bucket found with name: {bucket_id}")
            bucket_id = match.get('id')
        # Prepare file content
        if file_path:
            file_name = file_name or os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            with open(file_path, 'rb') as f:
                file_data = f.read()
        elif file_content and file_name:
            current_pos = file_content.tell()
            file_content.seek(0, os.SEEK_END)
            file_size = file_content.tell()
            file_content.seek(current_pos)
            file_data = file_content.read()
        else:
            raise ValueError("Provide either file_path or both file_content and file_name.")

        content_type = "application/octet-stream"

        # Step 1: initiate the upload and get presigned URL
        init_payload = {
            'filename': file_name,
            'content_type': content_type,
            'size': file_size,
            'bucket_id': bucket_id,
        }
        init_response = self._client._request(
            'post', '/files/initiate-upload', json=init_payload
        )
        file_metadata = init_response.get('file_metadata', {})
        presigned = init_response.get('presigned_upload_info', {})
        upload_url = presigned.get('upload_url')
        upload_method = presigned.get('upload_method', 'PUT')
        if not upload_url:
            raise ValueError('Missing presigned upload URL from server response')

        # Step 2: upload file to storage service
        headers = self._client._get_headers()
        if upload_method.upper() == 'POST':
            files = {'file': (file_name, file_data, content_type)}
            resp = requests.post(upload_url, files=files, headers=headers)
        else:
            headers['Content-Type'] = content_type
            resp = requests.request(upload_method, upload_url, data=file_data, headers=headers)

        if not resp.ok:
            raise APIError(resp.status_code, resp.text)
        return file_metadata

    def download(
        self,
        file_id: str,
        output_path: Optional[str] = None,
    ) -> Union[bytes, str]:
        """Download a file from the selected bucket."""
        bucket_id = self._bucket
        
        # Resolve bucket name to UUID if needed
        try:
            uuid.UUID(str(bucket_id))
        except (ValueError, TypeError):
            # bucket_id might be a name; look up real UUID
            buckets = self._client.list_buckets()
            match = next((b for b in buckets if b.get('name') == bucket_id), None)
            if not match:
                raise ValueError(f"No bucket found with name: {bucket_id}")
            bucket_id = match.get('id')
        
        # First get download info
        try:
            response = self._client._request(
                "get", f"/files/{file_id}/download-info", 
                params={"bucket_id": bucket_id}
            )
            download_url = response.get("download_url")
            if not download_url:
                raise ValueError("No download URL provided in response")
        except Exception as e:
            # Try public download if first attempt fails
            try:
                response = self._client._request(
                    "get", f"/files/public/{file_id}/download-info"
                )
                download_url = response.get("download_url")
                if not download_url:
                    raise ValueError("No download URL provided in response")
            except:
                raise e
        
        # Download the file
        headers = self._client._get_headers()
        dl_response = requests.get(download_url, headers=headers, stream=True)
        
        if not dl_response.ok:
            raise APIError(dl_response.status_code, dl_response.text)
        
        if output_path:
            with open(output_path, 'wb') as f:
                for chunk in dl_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return output_path
        else:
            return dl_response.content

    def list(self) -> List[Dict[str, Any]]:
        """List files in the selected bucket."""
        return self._client._request(
            "get", "/files", params={"bucket_id": self._bucket}
        )
