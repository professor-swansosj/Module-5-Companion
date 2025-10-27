"""
Module 01: Network Device Explorer

TODO: Build functions to explore network devices using RESTCONF
CHALLENGE: Figure out how to connect to network devices using HTTP!

Hints:
- RESTCONF uses HTTPS (like a web API)  
- You need the right headers: {"Accept": "application/yang-data+json"}
- Base URL: https://sandbox-iosxe-latest-1.cisco.com/restconf/data/
- Credentials: admin/C1sco12345
- Don't forget to disable SSL warnings!
"""

# TODO: Import what you need (you know this from Module 4!)

def get_device_hostname():
    """
    TODO: Create a function to get the device hostname
    
    CHALLENGE: Make a GET request to get system hostname
    RESTCONF endpoint: /ietf-system:system-state/hostname
    
    Hint: Build the full URL, add auth, add headers, handle the response
    """
    pass

def get_interfaces_list():
    """
    TODO: Create a function to list all device interfaces
    
    CHALLENGE: Get all interfaces from the device
    RESTCONF endpoint: /ietf-interfaces:interfaces
    
    Hint: Response will be JSON - dig into it to find interface names
    """
    pass

def explore_yang_paths():
    """
    TODO: Try different YANG paths to see what data you can get
    
    CHALLENGE: Experiment with these endpoints:
    - /Cisco-IOS-XE-native:native/hostname
    - /ietf-interfaces:interfaces/interface=GigabitEthernet1
    
    Hint: Some might work, some might not - that's learning!
    """
    pass

# TODO: Write a main() function to test everything

# TODO: Don't forget if __name__ == "__main__":