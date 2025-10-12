"""
Basic NETCONF Operations using ncclient

This example demonstrates how to:
1. Connect to a Cisco device using NETCONF
2. Perform basic NETCONF operations (get, get-config)
3. Handle XML responses
4. Parse NETCONF data

Prerequisites:
- Cisco device with NETCONF enabled (SSH port 830)
- Valid SSH credentials
- ncclient library installed
"""

from ncclient import manager
from ncclient.operations import RPCError
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging

class NetconfClient:
    """Simple NETCONF client for Cisco devices."""
    
    def __init__(self, host, username, password, port=830):
        """
        Initialize NETCONF client.
        
        Args:
            host (str): Device IP address or hostname
            username (str): SSH username
            password (str): SSH password
            port (int): NETCONF port (default 830)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        
        # Set up logging to see NETCONF messages (optional)
        # logging.basicConfig(level=logging.DEBUG)
    
    def connect(self):
        """
        Establish NETCONF connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            self.connection = manager.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=30,
                device_params={'name': 'csr'},  # Use 'csr' for Cisco devices
                hostkey_verify=False  # Disable host key verification for lab
            )
            
            print(f"✓ Connected to {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close NETCONF connection."""
        if self.connection:
            self.connection.close_session()
            print("✓ NETCONF session closed")
    
    def get_capabilities(self):
        """
        Get server NETCONF capabilities.
        
        Returns:
            list: List of server capabilities
        """
        if not self.connection:
            print("✗ Not connected")
            return None
        
        try:
            capabilities = list(self.connection.server_capabilities)
            print(f"✓ Retrieved {len(capabilities)} capabilities")
            return capabilities
            
        except Exception as e:
            print(f"✗ Error getting capabilities: {e}")
            return None
    
    def get_config(self, source='running', filter_xml=None):
        """
        Get configuration from the device.
        
        Args:
            source (str): Configuration source ('running', 'candidate', 'startup')
            filter_xml (str): XML filter to apply (optional)
            
        Returns:
            str: Configuration XML
        """
        if not self.connection:
            print("✗ Not connected")
            return None
        
        try:
            if filter_xml:
                config = self.connection.get_config(source=source, filter=filter_xml)
            else:
                config = self.connection.get_config(source=source)
            
            print(f"✓ Retrieved {source} configuration")
            return config.data_xml
            
        except RPCError as e:
            print(f"✗ RPC Error getting config: {e}")
            return None
        except Exception as e:
            print(f"✗ Error getting config: {e}")
            return None
    
    def get_operational_data(self, filter_xml=None):
        """
        Get operational data from the device.
        
        Args:
            filter_xml (str): XML filter to apply (optional)
            
        Returns:
            str: Operational data XML
        """
        if not self.connection:
            print("✗ Not connected")
            return None
        
        try:
            if filter_xml:
                data = self.connection.get(filter=filter_xml)
            else:
                data = self.connection.get()
            
            print("✓ Retrieved operational data")
            return data.data_xml
            
        except RPCError as e:
            print(f"✗ RPC Error getting operational data: {e}")
            return None
        except Exception as e:
            print(f"✗ Error getting operational data: {e}")
            return None

def prettify_xml(xml_string):
    """
    Pretty print XML string.
    
    Args:
        xml_string (str): XML string to format
        
    Returns:
        str: Formatted XML string
    """
    try:
        parsed = minidom.parseString(xml_string)
        return parsed.toprettyxml(indent="  ")
    except Exception as e:
        print(f"Error formatting XML: {e}")
        return xml_string

def demonstrate_connection():
    """Demonstrate NETCONF connection and capabilities."""
    
    # Device connection parameters
    # Update these values for your environment
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("=== NETCONF Connection Demo ===")
    print(f"Connecting to device: {DEVICE_IP}")
    
    # Create and connect NETCONF client
    client = NetconfClient(DEVICE_IP, USERNAME, PASSWORD)
    
    if client.connect():
        # Get and display capabilities
        print("\n1. Getting server capabilities...")
        capabilities = client.get_capabilities()
        
        if capabilities:
            print(f"Server supports {len(capabilities)} capabilities:")
            
            # Show YANG models
            yang_models = [cap for cap in capabilities if 'module=' in cap]
            print(f"\nYANG Models ({len(yang_models)}):")
            for model in yang_models[:10]:  # Show first 10
                if 'module=' in model:
                    module_info = model.split('module=')[1].split('&')[0] if 'module=' in model else model
                    print(f"  - {module_info}")
            
            if len(yang_models) > 10:
                print(f"  ... and {len(yang_models) - 10} more")
            
            # Show protocol versions
            netconf_versions = [cap for cap in capabilities if 'netconf/base' in cap]
            print(f"\nNETCONF Protocol Versions:")
            for version in netconf_versions:
                print(f"  - {version}")
        
        # Close connection
        client.disconnect()

def demonstrate_get_config():
    """Demonstrate getting configuration data."""
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin" 
    PASSWORD = "password"
    
    print("\n=== NETCONF Get-Config Demo ===")
    
    client = NetconfClient(DEVICE_IP, USERNAME, PASSWORD)
    
    if client.connect():
        # 1. Get all interfaces configuration
        print("\n1. Getting interfaces configuration...")
        
        interfaces_filter = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
        </filter>
        """
        
        config_xml = client.get_config(source='running', filter_xml=interfaces_filter)
        if config_xml:
            print("Interfaces Configuration (first 1000 chars):")
            formatted_xml = prettify_xml(config_xml)
            print(formatted_xml[:1000] + "..." if len(formatted_xml) > 1000 else formatted_xml)
        
        # 2. Get system configuration
        print("\n2. Getting system configuration...")
        
        system_filter = """
        <filter>
            <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system"/>
        </filter>
        """
        
        system_config = client.get_config(source='running', filter_xml=system_filter)
        if system_config:
            print("System Configuration:")
            print(prettify_xml(system_config))
        
        # 3. Get specific interface
        print("\n3. Getting specific interface configuration...")
        
        # Update interface name for your device
        specific_interface_filter = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>GigabitEthernet1</name>
                </interface>
            </interfaces>
        </filter>
        """
        
        specific_config = client.get_config(source='running', filter_xml=specific_interface_filter)
        if specific_config:
            print("Specific Interface Configuration:")
            print(prettify_xml(specific_config))
        
        client.disconnect()

def demonstrate_get_operational():
    """Demonstrate getting operational data."""
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("\n=== NETCONF Get Operational Data Demo ===")
    
    client = NetconfClient(DEVICE_IP, USERNAME, PASSWORD)
    
    if client.connect():
        # 1. Get interface statistics
        print("\n1. Getting interface statistics...")
        
        stats_filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <statistics/>
                </interface>
            </interfaces-state>
        </filter>
        """
        
        stats_xml = client.get_operational_data(filter_xml=stats_filter)
        if stats_xml:
            print("Interface Statistics (first 1500 chars):")
            formatted_xml = prettify_xml(stats_xml)
            print(formatted_xml[:1500] + "..." if len(formatted_xml) > 1500 else formatted_xml)
        
        # 2. Get system state
        print("\n2. Getting system state information...")
        
        system_state_filter = """
        <filter>
            <system-state xmlns="urn:ietf:params:xml:ns:yang:ietf-system"/>
        </filter>
        """
        
        system_state = client.get_operational_data(filter_xml=system_state_filter)
        if system_state:
            print("System State Information:")
            print(prettify_xml(system_state))
        
        client.disconnect()

def parse_interface_statistics(xml_data):
    """
    Parse interface statistics from XML data.
    
    Args:
        xml_data (str): XML data containing interface statistics
        
    Returns:
        dict: Parsed statistics data
    """
    try:
        root = ET.fromstring(xml_data)
        
        # Define namespaces
        namespaces = {
            'if': 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
        }
        
        interfaces_stats = {}
        
        # Find all interface elements
        for interface in root.findall('.//if:interface', namespaces):
            name_elem = interface.find('if:name', namespaces)
            stats_elem = interface.find('if:statistics', namespaces)
            
            if name_elem is not None and stats_elem is not None:
                name = name_elem.text
                
                stats = {}
                for stat in stats_elem:
                    # Remove namespace from tag
                    tag = stat.tag.split('}')[1] if '}' in stat.tag else stat.tag
                    stats[tag] = stat.text
                
                interfaces_stats[name] = stats
        
        return interfaces_stats
        
    except Exception as e:
        print(f"Error parsing statistics: {e}")
        return {}

def demonstrate_xml_parsing():
    """Demonstrate XML parsing of NETCONF responses."""
    
    DEVICE_IP = "192.168.1.1"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("\n=== NETCONF XML Parsing Demo ===")
    
    client = NetconfClient(DEVICE_IP, USERNAME, PASSWORD)
    
    if client.connect():
        # Get interface statistics and parse them
        stats_filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name/>
                    <statistics/>
                </interface>
            </interfaces-state>
        </filter>
        """
        
        stats_xml = client.get_operational_data(filter_xml=stats_filter)
        if stats_xml:
            print("Parsing interface statistics...")
            parsed_stats = parse_interface_statistics(stats_xml)
            
            print(f"\nFound statistics for {len(parsed_stats)} interfaces:")
            for interface_name, stats in parsed_stats.items():
                print(f"\n{interface_name}:")
                for stat_name, stat_value in stats.items():
                    if stat_value and stat_value.isdigit():
                        # Format large numbers for readability
                        value = int(stat_value)
                        if value > 1000000:
                            formatted_value = f"{value:,}"
                        else:
                            formatted_value = stat_value
                        print(f"  {stat_name}: {formatted_value}")
        
        client.disconnect()

def main():
    """Main function demonstrating NETCONF operations."""
    
    print("=== NETCONF Basic Operations Demo ===")
    print("This demo shows basic NETCONF operations using ncclient")
    print("Update the device credentials in each function for your environment\n")
    
    # Run demonstrations
    demonstrate_connection()
    demonstrate_get_config()
    demonstrate_get_operational()
    demonstrate_xml_parsing()
    
    print("\n=== Demo Complete ===")
    print("Key takeaways:")
    print("1. NETCONF uses XML for all data exchange")
    print("2. Filters help retrieve specific data subsets")
    print("3. Configuration and operational data are separate")
    print("4. XML parsing is essential for processing responses")
    print("5. Always handle exceptions in production code")

if __name__ == "__main__":
    main()