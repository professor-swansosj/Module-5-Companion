"""
Section 03: YANG Model Explorer

TODO: Understand YANG models - the "blueprints" for network device data
CHALLENGE: Figure out how network devices organize their data!

Key Concepts:
- YANG = Data modeling language for network configuration/state
- Like a "schema" or "blueprint" that defines what data exists
- RESTCONF uses YANG paths to access specific data
- Think: YANG is the "menu", RESTCONF is how you "order"
"""

# TODO: Import what you need

def explore_yang_structure():
    """
    TODO: Examine how device data is organized using YANG models
    
    CHALLENGE: Compare these different YANG paths:
    1. /ietf-interfaces:interfaces (IETF standard model)  
    2. /Cisco-IOS-XE-native:native (Cisco-specific model)
    3. /ietf-system:system-state (System information)
    
    Hint: Try each endpoint and see what data structure you get back!
    """
    pass

def find_interface_yang_paths():
    """
    TODO: Discover different ways to access interface data
    
    CHALLENGE: Try these interface-related YANG paths:
    - All interfaces: /ietf-interfaces:interfaces
    - One interface: /ietf-interfaces:interfaces/interface=GigabitEthernet1  
    - Interface stats: /ietf-interfaces:interfaces-state
    
    Question: What's the difference between config vs state data?
    """
    pass

def compare_yang_models():
    """
    TODO: Compare IETF standard vs Cisco proprietary YANG models
    
    CHALLENGE: Get hostname using both approaches:
    1. IETF way: /ietf-system:system-state/hostname
    2. Cisco way: /Cisco-IOS-XE-native:native/hostname
    
    Discussion: Why might there be multiple ways to get the same data?
    """
    pass

def build_yang_path_from_cli():
    """
    TODO: Practice converting CLI commands to YANG paths
    
    CHALLENGE: Figure out YANG equivalents for these CLI commands:
    - show interface GigabitEthernet1
    - show ip interface brief  
    - show version
    
    Hint: Use trial and error with different YANG paths!
    """
    pass

def yang_data_types_exploration():
    """
    TODO: Explore different YANG data types in responses
    
    CHALLENGE: Find examples of:
    - Container: Groups related data (like "interfaces")
    - List: Multiple items (like interface list) 
    - Leaf: Single values (like hostname)
    
    Hint: Look at the JSON structure from your requests!
    """
    pass

# TODO: Create a main() function that calls these challenges

# TODO: Add error handling and user-friendly output
