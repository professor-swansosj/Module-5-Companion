"""
Basic RESTCONF GET operations using the requests library.

This example demonstrates how to:
1. Connect to a Cisco device using RESTCONF
2. Perform basic GET operations
3. Handle HTTP responses and errors
4. Parse JSON data from responses

Prerequisites:
- Cisco device with RESTCONF enabled
- Valid credentials
- Network connectivity to the device
"""

import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for lab environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RestconfClient:
    """Simple RESTCONF client for Cisco devices."""
    
    def __init__(self, host, username, password, port=443):
        """
        Initialize RESTCONF client.
        
        Args:
            host (str): Device IP address or hostname
            username (str): Username for authentication
            password (str): Password for authentication  
            port (int): RESTCONF port (default 443)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_url = f"https://{host}:{port}/restconf"
        
        # Set up session
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = False  # Disable SSL verification for lab
        
        # Set headers
        self.session.headers.update({
            'Accept': 'application/yang-data+json',
            'Content-Type': 'application/yang-data+json'
        })
    
    def get_capabilities(self):
        """
        Get device RESTCONF capabilities.
        
        Returns:
            dict: Capabilities information
        """
        try:
            url = f"{self.base_url}/data/ietf-restconf-monitoring:restconf-state/capabilities"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting capabilities: {e}")
            return None
    
    def get_interfaces(self):
        """
        Get all interfaces from the device.
        
        Returns:
            dict: Interface information
        """
        try:
            url = f"{self.base_url}/data/ietf-interfaces:interfaces"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting interfaces: {e}")
            return None
    
    def get_interface(self, interface_name):
        """
        Get specific interface information.
        
        Args:
            interface_name (str): Name of the interface
            
        Returns:
            dict: Interface information
        """
        try:
            # URL encode the interface name
            encoded_name = requests.utils.quote(interface_name, safe='')
            url = f"{self.base_url}/data/ietf-interfaces:interfaces/interface={encoded_name}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting interface {interface_name}: {e}")
            return None
    
    def get_interface_statistics(self, interface_name):
        """
        Get interface statistics.
        
        Args:
            interface_name (str): Name of the interface
            
        Returns:
            dict: Interface statistics
        """
        try:
            encoded_name = requests.utils.quote(interface_name, safe='')
            url = f"{self.base_url}/data/ietf-interfaces:interfaces-state/interface={encoded_name}/statistics"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting statistics for {interface_name}: {e}")
            return None
    
    def get_system_info(self):
        """
        Get system information.
        
        Returns:
            dict: System information
        """
        try:
            url = f"{self.base_url}/data/ietf-system:system"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting system info: {e}")
            return None

def print_json(data, title="Data"):
    """Pretty print JSON data."""
    if data:
        print(f"\n{title}:")
        print(json.dumps(data, indent=2))
    else:
        print(f"\n{title}: No data available")

def main():
    """Main function demonstrating RESTCONF operations."""
    
    # Device connection parameters
    # Update these values for your environment
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("=== RESTCONF Basic GET Operations Demo ===")
    print(f"Connecting to device: {DEVICE_IP}")
    
    # Create RESTCONF client
    client = RestconfClient(DEVICE_IP, USERNAME, PASSWORD)
    
    # 1. Get device capabilities
    print("\n1. Getting RESTCONF capabilities...")
    capabilities = client.get_capabilities()
    if capabilities:
        print("Available capabilities:")
        for capability in capabilities.get('ietf-restconf-monitoring:capabilities', {}).get('capability', []):
            print(f"  - {capability}")
    
    # 2. Get all interfaces
    print("\n2. Getting all interfaces...")
    interfaces = client.get_interfaces()
    if interfaces:
        interface_list = interfaces.get('ietf-interfaces:interfaces', {}).get('interface', [])
        print(f"Found {len(interface_list)} interfaces:")
        for interface in interface_list:
            print(f"  - {interface.get('name')} (Type: {interface.get('type')}, Status: {interface.get('enabled', 'unknown')})")
    
    # 3. Get specific interface details
    print("\n3. Getting specific interface details...")
    if interfaces:
        # Get the first interface name
        first_interface = interface_list[0]['name'] if interface_list else None
        if first_interface:
            print(f"Getting details for interface: {first_interface}")
            interface_detail = client.get_interface(first_interface)
            print_json(interface_detail, f"Interface {first_interface} Details")
            
            # Get interface statistics
            print(f"\n4. Getting statistics for interface: {first_interface}")
            stats = client.get_interface_statistics(first_interface)
            print_json(stats, f"Interface {first_interface} Statistics")
    
    # 5. Get system information
    print("\n5. Getting system information...")
    system_info = client.get_system_info()
    if system_info:
        system_data = system_info.get('ietf-system:system', {})
        print(f"Hostname: {system_data.get('hostname', 'N/A')}")
        print(f"Contact: {system_data.get('contact', 'N/A')}")
        print(f"Location: {system_data.get('location', 'N/A')}")

if __name__ == "__main__":
    main()