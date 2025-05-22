"""Tests for SelfDB client."""

import unittest
from unittest.mock import patch, MagicMock

from selfdb import SelfDBClient
from selfdb.exceptions import AuthenticationError, ResourceNotFoundError


class TestSelfDBClient(unittest.TestCase):
    """Tests for the SelfDBClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = SelfDBClient(baseurl="http://example.com/api/v1")
    
    def test_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.baseurl, "http://example.com/api/v1")
        self.assertIsNone(self.client.anon_key)
        self.assertIsNone(self.client.access_token)
        self.assertIsNone(self.client.refresh_token)
    
    def test_initialization_with_anon_key(self):
        """Test client initialization with anon key."""
        client = SelfDBClient(
            baseurl="http://example.com/api/v1",
            anon_key="test-anon-key"
        )
        self.assertEqual(client.anon_key, "test-anon-key")
    
    def test_initialization_with_storage_url(self):
        """Test client initialization with storage URL."""
        client = SelfDBClient(
            baseurl="http://example.com/api/v1",
            storageurl="http://storage.example.com"
        )
        self.assertEqual(client.storageurl, "http://storage.example.com")
    
    @patch('selfdb.client.requests.Session.request')
    def test_login(self, mock_request):
        """Test login method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "user_id": "123",
            "email": "test@example.com",
            "is_superuser": False
        }
        mock_response.status_code = 200
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        # Call login method
        result = self.client.login("test@example.com", "password")
        
        # Assertions
        mock_request.assert_called_once()
        self.assertEqual(self.client.access_token, "test-access-token")
        self.assertEqual(self.client.refresh_token, "test-refresh-token")
        self.assertEqual(result["email"], "test@example.com")
    
    @patch('selfdb.client.requests.Session.request')
    def test_list_tables(self, mock_request):
        """Test list_tables method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "table1", "schema": "public"},
            {"name": "table2", "schema": "public"}
        ]
        mock_response.status_code = 200
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        # Call list_tables method
        result = self.client.list_tables()
        
        # Assertions
        mock_request.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "table1")
        self.assertEqual(result[1]["name"], "table2")
    
    @patch('selfdb.client.requests.Session.request')
    def test_error_handling(self, mock_request):
        """Test error handling."""
        # Mock response for 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.ok = False
        mock_response.url = "http://example.com/api/v1/tables/nonexistent"
        mock_request.return_value = mock_response
        
        # Call method and check exception
        with self.assertRaises(ResourceNotFoundError):
            self.client.get_table("nonexistent")
        
        # Mock response for 401
        mock_response.status_code = 401
        with self.assertRaises(AuthenticationError):
            self.client.list_tables()


if __name__ == '__main__':
    unittest.main()