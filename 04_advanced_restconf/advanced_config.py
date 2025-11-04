"""
Section 04: RESTCONF Configuration

TODO: Master configuration changes using RESTCONF PUT/PATCH operations  
CHALLENGE: Make safe configuration changes to network devices!

WARNING: These are REAL configuration changes!
- Start with safe changes (descriptions, non-critical settings)
- Always read current config before changing
- Verify changes after applying

Key Concepts:  
- GET = Read configuration
- PUT = Replace/Update configuration  
- PATCH = Modify part of configuration
- DELETE = Remove configuration
"""

# TODO: Import what you need

def read_before_write():
    """
    TODO: ALWAYS read current configuration before making changes
    
    CHALLENGE: Get current interface description for GigabitEthernet1
    Endpoint: /ietf-interfaces:interfaces/interface=GigabitEthernet1
    
    Best Practice: Never change config without knowing current state!
    """
    pass

def update_interface_description():
    """
    TODO: Safely update an interface description
    
    CHALLENGE: Use PUT to change interface description
    Endpoint: /ietf-interfaces:interfaces/interface=GigabitEthernet1/description
    Method: PUT
    Data: Just a string with new description
    
    Hint: PUT replaces the entire description field
    """
    pass

def enable_disable_interface():
    """
    TODO: Practice enabling/disabling an interface  
    
    CHALLENGE: Change admin-status of an interface
    Endpoint: /ietf-interfaces:interfaces/interface=GigabitEthernet1/enabled
    Data: true (enable) or false (disable)
    
    WARNING: Be careful - this affects network connectivity!
    """
    pass

def bulk_configuration_change():
    """
    TODO: Update multiple interface properties at once
    
    CHALLENGE: Use PUT on entire interface to change multiple things:
    - description
    - enabled status  
    - maybe MTU?
    
    Endpoint: /ietf-interfaces:interfaces/interface=GigabitEthernet1
    
    Hint: Send complete interface object with all properties
    """
    pass

def configuration_rollback():
    """
    TODO: Learn to undo changes (restore original settings)
    
    CHALLENGE: 
    1. Save original configuration
    2. Make a change
    3. Restore original configuration
    
    Hint: Store the original data from your GET request!
    """
    pass

def error_handling_and_validation():
    """
    TODO: Handle configuration errors gracefully
    
    CHALLENGE: Try these scenarios and handle errors:
    - Invalid interface name
    - Invalid configuration data
    - Device busy/locked
    - Authentication failure
    
    Hint: Check response status codes and error messages!
    """
    pass

# TODO: Create main() function with step-by-step configuration workflow

# TODO: Add proper error handling and rollback capabilities
