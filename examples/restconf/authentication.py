"""
RESTCONF Authentication Methods

This example demonstrates different authentication methods for RESTCONF:
1. Basic Authentication (most common)
2. Token-based authentication
3. Certificate-based authentication
4. Session management and token refresh

Prerequisites:
- Cisco device with RESTCONF enabled
- Valid credentials or certificates
"""

import requests
import json
import base64
import time
from datetime import datetime, timedelta
import urllib3

# Disable SSL warnings for lab environments  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RestconfAuthenticator:
    """Handles various RESTCONF authentication methods."""
    
    def __init__(self, host, port=443):
        """Initialize authenticator with device details."""
        self.host = host
        self.port = port
        self.base_url = f"https://{host}:{port}/restconf"
        self.session = requests.Session()
        self.session.verify = False
        self.token = None
        self.token_expiry = None
    
    def basic_auth(self, username, password):
        """
        Set up basic HTTP authentication.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if authentication setup successful
        """
        try:
            # Set basic auth
            self.session.auth = requests.auth.HTTPBasicAuth(username, password)
            
            # Set standard headers
            self.session.headers.update({
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+json'
            })
            
            # Test authentication with a simple request
            response = self.session.get(f"{self.base_url}/data/ietf-restconf-monitoring:restconf-state/capabilities")
            response.raise_for_status()
            
            print("✓ Basic authentication successful")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Basic authentication failed: {e}")
            return False
    
    def token_auth(self, username, password):
        """
        Authenticate using token-based method (if supported).
        Note: This is a conceptual example as token auth varies by device.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if token authentication successful
        """
        try:
            # Step 1: Get token (this endpoint varies by device)
            auth_data = {
                "username": username,
                "password": password
            }
            
            # This is a hypothetical endpoint - actual implementation varies
            token_url = f"{self.base_url}/auth/token"
            
            response = self.session.post(
                token_url,
                json=auth_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get('token')
                
                # Set token expiry (usually provided by server)
                expires_in = token_data.get('expires_in', 3600)  # Default 1 hour
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                
                # Update session headers with token
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}',
                    'Accept': 'application/yang-data+json',
                    'Content-Type': 'application/yang-data+json'
                })
                
                print("✓ Token authentication successful")
                print(f"Token expires at: {self.token_expiry}")
                return True
            else:
                print(f"✗ Token authentication failed: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Token authentication failed: {e}")
            print("Note: Token authentication may not be supported on this device")
            return False
    
    def certificate_auth(self, cert_file, key_file):
        """
        Set up certificate-based authentication.
        
        Args:
            cert_file (str): Path to certificate file
            key_file (str): Path to private key file
            
        Returns:
            bool: True if certificate authentication successful
        """
        try:
            # Set client certificate
            self.session.cert = (cert_file, key_file)
            
            # Set headers
            self.session.headers.update({
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+json'
            })
            
            # Test authentication
            response = self.session.get(f"{self.base_url}/data/ietf-restconf-monitoring:restconf-state/capabilities")
            response.raise_for_status()
            
            print("✓ Certificate authentication successful")
            return True
            
        except FileNotFoundError:
            print("✗ Certificate files not found")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Certificate authentication failed: {e}")
            return False
    
    def is_token_expired(self):
        """Check if current token is expired."""
        if not self.token or not self.token_expiry:
            return True
        return datetime.now() >= self.token_expiry
    
    def refresh_token(self, username, password):
        """
        Refresh authentication token.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if token refresh successful
        """
        if self.is_token_expired():
            print("Token expired, refreshing...")
            return self.token_auth(username, password)
        return True
    
    def make_authenticated_request(self, method, url, **kwargs):
        """
        Make an authenticated request with automatic token refresh.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            url (str): Request URL
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: HTTP response
        """
        # Check token expiry if using token auth
        if self.token and self.is_token_expired():
            print("Token expired during request, please re-authenticate")
            return None
        
        # Make request
        response = self.session.request(method, url, **kwargs)
        return response

def demonstrate_basic_auth():
    """Demonstrate basic authentication."""
    print("\n=== Basic Authentication Demo ===")
    
    # Update these for your environment
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin" 
    PASSWORD = "password"
    
    auth = RestconfAuthenticator(DEVICE_IP)
    
    if auth.basic_auth(USERNAME, PASSWORD):
        # Make a test request
        response = auth.make_authenticated_request(
            'GET', 
            f"{auth.base_url}/data/ietf-interfaces:interfaces"
        )
        
        if response and response.status_code == 200:
            data = response.json()
            interfaces = data.get('ietf-interfaces:interfaces', {}).get('interface', [])
            print(f"Successfully retrieved {len(interfaces)} interfaces")
        else:
            print("Failed to retrieve interfaces")

def demonstrate_token_auth():
    """Demonstrate token authentication (conceptual)."""
    print("\n=== Token Authentication Demo ===")
    
    # Update these for your environment
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    auth = RestconfAuthenticator(DEVICE_IP)
    
    # Try token authentication
    if auth.token_auth(USERNAME, PASSWORD):
        # Make authenticated requests
        for i in range(3):
            print(f"\nMaking request {i+1}...")
            response = auth.make_authenticated_request(
                'GET',
                f"{auth.base_url}/data/ietf-system:system/hostname"
            )
            
            if response and response.status_code == 200:
                hostname_data = response.json()
                print(f"Device hostname: {hostname_data}")
            
            time.sleep(1)  # Wait between requests

def demonstrate_certificate_auth():
    """Demonstrate certificate authentication."""
    print("\n=== Certificate Authentication Demo ===")
    
    # Update these paths for your environment
    DEVICE_IP = "192.168.1.1"
    CERT_FILE = "/path/to/client.crt"
    KEY_FILE = "/path/to/client.key"
    
    auth = RestconfAuthenticator(DEVICE_IP)
    
    if auth.certificate_auth(CERT_FILE, KEY_FILE):
        response = auth.make_authenticated_request(
            'GET',
            f"{auth.base_url}/data/ietf-interfaces:interfaces"
        )
        
        if response and response.status_code == 200:
            print("Certificate authentication working properly")
        else:
            print("Certificate authentication setup but request failed")

def demonstrate_session_management():
    """Demonstrate session management and error handling."""
    print("\n=== Session Management Demo ===")
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    auth = RestconfAuthenticator(DEVICE_IP)
    
    # Set up basic auth
    if not auth.basic_auth(USERNAME, PASSWORD):
        print("Failed to authenticate")
        return
    
    # Test different error conditions
    test_urls = [
        (f"{auth.base_url}/data/ietf-interfaces:interfaces", "Valid interfaces request"),
        (f"{auth.base_url}/data/nonexistent-module:data", "Invalid module request"),
        (f"{auth.base_url}/data/ietf-interfaces:interfaces/interface=InvalidInterface", "Invalid interface request")
    ]
    
    for url, description in test_urls:
        print(f"\nTesting: {description}")
        try:
            response = auth.make_authenticated_request('GET', url)
            if response:
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    print("✓ Request successful")
                elif response.status_code == 404:
                    print("⚠ Resource not found (expected for some tests)")
                elif response.status_code == 401:
                    print("✗ Authentication failed")
                elif response.status_code == 403:
                    print("✗ Access forbidden")
                else:
                    print(f"⚠ Unexpected status: {response.status_code}")
            else:
                print("✗ No response received")
        except Exception as e:
            print(f"✗ Request failed: {e}")

def main():
    """Main function demonstrating all authentication methods."""
    print("=== RESTCONF Authentication Methods Demo ===")
    
    # Demonstrate different authentication methods
    demonstrate_basic_auth()
    
    # Note: Token and certificate auth may not be supported on all devices
    # Uncomment these if your device supports them
    # demonstrate_token_auth()
    # demonstrate_certificate_auth()
    
    demonstrate_session_management()
    
    print("\n=== Demo Complete ===")
    print("Note: Update the device IP, credentials, and certificate paths for your environment")

if __name__ == "__main__":
    main()