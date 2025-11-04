"""
Section 02: RESTCONF Foundations

TODO: Apply your Module 4 requests skills to network automation!
CHALLENGE: Build functions to get device information via RESTCONF

Key Concepts:
- RESTCONF = REST + NETCONF (HTTP API for network devices)
- Uses same requests library you know from Module 4
- Returns JSON data just like regular APIs
- Authentication and headers work the same way

Device Info:
- Host: sandbox-iosxe-latest-1.cisco.com
- Username: admin  
- Password: C1sco12345
- Base URL: https://HOST/restconf/data/
"""

# TODO: Import what you need

def get_device_hostname():
    """
    TODO: Get the device hostname via RESTCONF
    
    CHALLENGE: Make a GET request to get system hostname
    Endpoint: /ietf-system:system-state/hostname
    Headers: {"Accept": "application/yang-data+json"}
    
    Hint: Just like Module 4 APIs but for network devices!
    """
    pass

def list_all_interfaces():
    """
    TODO: Get a list of all device interfaces
    
    CHALLENGE: Parse the JSON response to show interface names
    Endpoint: /ietf-interfaces:interfaces
    
    Hint: The response structure has nested data - explore it!
    """
    pass

def get_interface_details(interface_name):
    """
    TODO: Get detailed info about a specific interface
    
    CHALLENGE: Get info for one interface by name
    Endpoint: /ietf-interfaces:interfaces/interface={name}
    
    Parameters:
    - interface_name: Name like "GigabitEthernet1"
    
    Hint: Try different interface names to see what exists!
    """
    pass

def explore_device_capabilities():
    """
    TODO: Explore what RESTCONF operations this device supports
    
    CHALLENGE: Try the capabilities endpoint
    Endpoint: /ietf-restconf-monitoring:restconf-state/capabilities
    
    Hint: This tells you what the device can do!
    """
    pass

# TODO: Write a main() function to test your functions

# TODO: Add proper if __name__ == "__main__" guard
