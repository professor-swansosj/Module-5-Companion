"""
RESTCONF Configuration Operations

This example demonstrates how to:
1. Configure interfaces using RESTCONF PUT/PATCH/POST
2. Handle configuration transactions
3. Validate configuration changes
4. Rollback configurations

Prerequisites:
- Cisco device with RESTCONF enabled
- Write access credentials
- Understanding of YANG models
"""

import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for lab environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RestconfConfigurator:
    """RESTCONF client for configuration operations."""
    
    def __init__(self, host, username, password, port=443):
        """Initialize RESTCONF configuration client."""
        self.host = host
        self.port = port
        self.base_url = f"https://{host}:{port}/restconf"
        
        # Set up session
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = False
        
        # Set headers for configuration operations
        self.session.headers.update({
            'Accept': 'application/yang-data+json',
            'Content-Type': 'application/yang-data+json'
        })
    
    def get_interface_config(self, interface_name):
        """
        Get current interface configuration.
        
        Args:
            interface_name (str): Interface name (e.g., 'GigabitEthernet1/0/1')
            
        Returns:
            dict: Current interface configuration
        """
        try:
            encoded_name = requests.utils.quote(interface_name, safe='')
            url = f"{self.base_url}/data/ietf-interfaces:interfaces/interface={encoded_name}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting interface config: {e}")
            return None
    
    def create_interface_config(self, interface_config):
        """
        Create a new interface configuration using POST.
        
        Args:
            interface_config (dict): Interface configuration data
            
        Returns:
            bool: True if creation successful
        """
        try:
            url = f"{self.base_url}/data/ietf-interfaces:interfaces"
            
            # Wrap config in proper structure
            data = {
                "ietf-interfaces:interface": interface_config
            }
            
            response = self.session.post(url, json=data)
            response.raise_for_status()
            print(f"✓ Interface {interface_config['name']} created successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error creating interface: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False
    
    def update_interface_config(self, interface_name, config_updates):
        """
        Update interface configuration using PATCH.
        
        Args:
            interface_name (str): Interface name
            config_updates (dict): Configuration updates
            
        Returns:
            bool: True if update successful
        """
        try:
            encoded_name = requests.utils.quote(interface_name, safe='')
            url = f"{self.base_url}/data/ietf-interfaces:interfaces/interface={encoded_name}"
            
            # Wrap updates in proper structure
            data = {
                "ietf-interfaces:interface": config_updates
            }
            
            response = self.session.patch(url, json=data)
            response.raise_for_status()
            print(f"✓ Interface {interface_name} updated successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error updating interface: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False
    
    def replace_interface_config(self, interface_name, new_config):
        """
        Replace entire interface configuration using PUT.
        
        Args:
            interface_name (str): Interface name
            new_config (dict): New complete configuration
            
        Returns:
            bool: True if replacement successful
        """
        try:
            encoded_name = requests.utils.quote(interface_name, safe='')
            url = f"{self.base_url}/data/ietf-interfaces:interfaces/interface={encoded_name}"
            
            # Wrap config in proper structure
            data = {
                "ietf-interfaces:interface": new_config
            }
            
            response = self.session.put(url, json=data)
            response.raise_for_status()
            print(f"✓ Interface {interface_name} configuration replaced successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error replacing interface config: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False
    
    def delete_interface_config(self, interface_name):
        """
        Delete interface configuration.
        
        Args:
            interface_name (str): Interface name
            
        Returns:
            bool: True if deletion successful
        """
        try:
            encoded_name = requests.utils.quote(interface_name, safe='')
            url = f"{self.base_url}/data/ietf-interfaces:interfaces/interface={encoded_name}"
            
            response = self.session.delete(url)
            response.raise_for_status()
            print(f"✓ Interface {interface_name} deleted successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error deleting interface: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False
    
    def configure_hostname(self, hostname):
        """
        Configure system hostname.
        
        Args:
            hostname (str): New hostname
            
        Returns:
            bool: True if configuration successful
        """
        try:
            url = f"{self.base_url}/data/ietf-system:system/hostname"
            data = {
                "ietf-system:hostname": hostname
            }
            
            response = self.session.put(url, json=data)
            response.raise_for_status()
            print(f"✓ Hostname set to '{hostname}' successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error setting hostname: {e}")
            return False

def demonstrate_interface_lifecycle():
    """Demonstrate complete interface configuration lifecycle."""
    
    # Device connection parameters
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("=== Interface Configuration Lifecycle Demo ===")
    
    configurator = RestconfConfigurator(DEVICE_IP, USERNAME, PASSWORD)
    
    # Test interface name (adjust for your device)
    test_interface = "Loopback100"
    
    print(f"\n1. Creating interface {test_interface}...")
    
    # Create interface configuration
    interface_config = {
        "name": test_interface,
        "description": "Test loopback interface created via RESTCONF",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True
    }
    
    if configurator.create_interface_config(interface_config):
        # Get current configuration
        print(f"\n2. Reading current configuration...")
        current_config = configurator.get_interface_config(test_interface)
        if current_config:
            print(json.dumps(current_config, indent=2))
        
        # Update interface description
        print(f"\n3. Updating interface description...")
        updates = {
            "description": "Updated description via RESTCONF PATCH"
        }
        configurator.update_interface_config(test_interface, updates)
        
        # Add IP address (for loopback interfaces)
        print(f"\n4. Adding IP address configuration...")
        ip_config = {
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "192.168.100.1",
                        "netmask": "255.255.255.255"
                    }
                ]
            }
        }
        configurator.update_interface_config(test_interface, ip_config)
        
        # Read final configuration
        print(f"\n5. Reading final configuration...")
        final_config = configurator.get_interface_config(test_interface)
        if final_config:
            print(json.dumps(final_config, indent=2))
        
        # Clean up - delete the test interface
        print(f"\n6. Cleaning up - deleting interface...")
        configurator.delete_interface_config(test_interface)

def demonstrate_bulk_configuration():
    """Demonstrate bulk configuration operations."""
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("\n=== Bulk Configuration Demo ===")
    
    configurator = RestconfConfigurator(DEVICE_IP, USERNAME, PASSWORD)
    
    # Create multiple loopback interfaces
    loopback_configs = []
    for i in range(101, 104):
        config = {
            "name": f"Loopback{i}",
            "description": f"Bulk created loopback {i}",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": f"192.168.{i}.1",
                        "netmask": "255.255.255.255"
                    }
                ]
            }
        }
        loopback_configs.append(config)
    
    # Create all interfaces
    print("Creating multiple loopback interfaces...")
    success_count = 0
    for config in loopback_configs:
        if configurator.create_interface_config(config):
            success_count += 1
    
    print(f"Successfully created {success_count}/{len(loopback_configs)} interfaces")
    
    # Clean up
    print("\nCleaning up created interfaces...")
    for config in loopback_configs:
        configurator.delete_interface_config(config["name"])

def demonstrate_error_handling():
    """Demonstrate error handling in configuration operations."""
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("\n=== Error Handling Demo ===")
    
    configurator = RestconfConfigurator(DEVICE_IP, USERNAME, PASSWORD)
    
    # Test various error conditions
    
    print("1. Testing invalid interface name...")
    invalid_config = {
        "name": "InvalidInterface999/999/999",
        "description": "This should fail",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True
    }
    configurator.create_interface_config(invalid_config)
    
    print("\n2. Testing update of non-existent interface...")
    configurator.update_interface_config("NonExistentInterface", {"description": "test"})
    
    print("\n3. Testing invalid IP configuration...")
    invalid_ip_config = {
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "999.999.999.999",  # Invalid IP
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
    configurator.update_interface_config("Loopback0", invalid_ip_config)

def demonstrate_transaction_safety():
    """Demonstrate transaction safety and rollback concepts."""
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("\n=== Transaction Safety Demo ===")
    
    configurator = RestconfConfigurator(DEVICE_IP, USERNAME, PASSWORD)
    
    test_interface = "Loopback200"
    
    print("1. Saving current hostname...")
    # Get current hostname for rollback
    try:
        response = configurator.session.get(f"{configurator.base_url}/data/ietf-system:system/hostname")
        if response.status_code == 200:
            original_hostname = response.json().get("ietf-system:hostname")
            print(f"Original hostname: {original_hostname}")
        else:
            original_hostname = None
            print("Could not retrieve original hostname")
    except Exception as e:
        print(f"Error getting hostname: {e}")
        original_hostname = None
    
    print("\n2. Making configuration changes...")
    # Create test interface
    test_config = {
        "name": test_interface,
        "description": "Transaction safety test interface",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True
    }
    
    if configurator.create_interface_config(test_config):
        # Change hostname
        configurator.configure_hostname("RESTCONF-TEST-DEVICE")
        
        print("\n3. Simulating rollback...")
        # Rollback changes
        configurator.delete_interface_config(test_interface)
        
        if original_hostname:
            configurator.configure_hostname(original_hostname)
            print(f"Rolled back hostname to: {original_hostname}")

def main():
    """Main function demonstrating RESTCONF configuration operations."""
    
    print("=== RESTCONF Configuration Operations Demo ===")
    print("Note: This demo requires write access to the device!")
    print("Make sure you have proper credentials and backup your config.")
    
    input("\nPress Enter to continue or Ctrl+C to abort...")
    
    # Run demonstrations
    demonstrate_interface_lifecycle()
    demonstrate_bulk_configuration() 
    demonstrate_error_handling()
    demonstrate_transaction_safety()
    
    print("\n=== Demo Complete ===")
    print("Remember to:")
    print("1. Always backup configurations before making changes")
    print("2. Test changes in a lab environment first")
    print("3. Implement proper error handling in production code")
    print("4. Consider using configuration sessions for complex changes")

if __name__ == "__main__":
    main()