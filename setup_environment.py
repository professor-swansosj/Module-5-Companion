#!/usr/bin/env python3
"""
Environment Setup Script for Module 5 - RESTCONF & NETCONF

This script helps students set up their development environment
for the RESTCONF and NETCONF companion materials.

Functions:
- Check Python version
- Install required packages
- Verify package installations
- Set up example configuration files
- Test basic functionality
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    print("Checking Python version...")
    
    major, minor = sys.version_info[:2]
    required_major, required_minor = 3, 8
    
    if major < required_major or (major == required_major and minor < required_minor):
        print(f"✗ Python {required_major}.{required_minor}+ required, found {major}.{minor}")
        print("Please upgrade Python to continue.")
        return False
    else:
        print(f"✓ Python {major}.{minor} meets requirements")
        return True

def install_package(package_name):
    """Install a Python package using pip."""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name
        ])
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package_name}: {e}")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} is available")
        return True
    except ImportError:
        print(f"✗ {package_name} is not available")
        return False

def install_requirements():
    """Install all required packages."""
    print("\n=== Installing Required Packages ===")
    
    # Core packages needed for the examples
    packages = [
        "requests",
        "urllib3",
        "ncclient",
        "lxml",
        "PyYAML",
        "jsonschema"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\nInstallation Summary: {success_count}/{len(packages)} packages installed")
    return success_count == len(packages)

def verify_installations():
    """Verify that all required packages can be imported."""
    print("\n=== Verifying Package Installations ===")
    
    # Test imports with their actual import names
    test_imports = [
        ("requests", "requests"),
        ("urllib3", "urllib3"), 
        ("ncclient", "ncclient"),
        ("lxml", "lxml"),
        ("PyYAML", "yaml"),
        ("jsonschema", "jsonschema")
    ]
    
    success_count = 0
    for package_name, import_name in test_imports:
        if check_package(package_name, import_name):
            success_count += 1
    
    print(f"\nVerification Summary: {success_count}/{len(test_imports)} packages verified")
    return success_count == len(test_imports)

def create_sample_config():
    """Create sample configuration files for examples."""
    print("\n=== Creating Sample Configuration Files ===")
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Create sample device configuration
    device_config = """# Sample Device Configuration
# Update these values for your lab environment

[device]
host = 192.168.1.1
username = admin
password = password

[restconf]
port = 443
base_url = /restconf

[netconf]  
port = 830

[logging]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
"""
    
    config_file = config_dir / "device_config.ini"
    with open(config_file, 'w') as f:
        f.write(device_config)
    
    print(f"✓ Created sample configuration: {config_file}")
    
    # Create environment template
    env_template = """# Environment Variables Template
# Copy this to .env and update with your values

DEVICE_HOST=192.168.1.1
DEVICE_USERNAME=admin
DEVICE_PASSWORD=password
RESTCONF_PORT=443
NETCONF_PORT=830

# Optional: Enable debug logging
DEBUG=false
"""
    
    env_file = config_dir / "env_template"
    with open(env_file, 'w') as f:
        f.write(env_template)
    
    print(f"✓ Created environment template: {env_file}")
    
    return True

def test_basic_functionality():
    """Test basic functionality of installed packages."""
    print("\n=== Testing Basic Functionality ===")
    
    # Test requests
    try:
        import requests
        print("✓ requests library loaded")
    except Exception as e:
        print(f"✗ requests test failed: {e}")
        return False
    
    # Test YAML processing
    try:
        import yaml
        test_data = {"test": "value", "number": 42}
        yaml_string = yaml.dump(test_data)
        loaded_data = yaml.safe_load(yaml_string)
        assert loaded_data == test_data
        print("✓ YAML processing works")
    except Exception as e:
        print(f"✗ YAML test failed: {e}")
        return False
    
    # Test JSON schema validation
    try:
        import jsonschema
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
        test_data = {"name": "test"}
        jsonschema.validate(test_data, schema)
        print("✓ JSON schema validation works")
    except Exception as e:
        print(f"✗ JSON schema test failed: {e}")
        return False
    
    # Test XML processing
    try:
        from lxml import etree
        xml_string = "<root><child>text</child></root>"
        root = etree.fromstring(xml_string)
        assert root.find("child").text == "text"
        print("✓ XML processing works")
    except Exception as e:
        print(f"✗ XML test failed: {e}")
        return False
    
    print("✓ All basic functionality tests passed")
    return True

def check_network_connectivity():
    """Check if basic network tools are available."""
    print("\n=== Checking Network Connectivity Tools ===")
    
    # Check if ping is available (for testing device connectivity)
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "8.8.8.8"] if os.name != 'nt' else ["ping", "-n", "1", "8.8.8.8"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Network connectivity available")
        else:
            print("⚠ Network connectivity test failed (but this is not critical)")
    except Exception as e:
        print(f"⚠ Could not test network connectivity: {e}")
    
    return True

def display_next_steps():
    """Display next steps for students."""
    print("\n" + "="*60)
    print("SETUP COMPLETE - Next Steps:")
    print("="*60)
    
    print("""
1. Update Configuration Files:
   - Edit config/device_config.ini with your device details
   - Copy config/env_template to .env and customize
   
2. Test Your Setup:
   - Run: python examples/restconf/basic_get.py
   - Run: python examples/netconf/basic_operations.py
   
3. Explore the Examples:
   - Start with basic examples in each directory
   - Progress to more advanced configuration examples
   - Practice with sample data files in data/
   
4. Study the Documentation:
   - Read docs/yang-introduction.md
   - Review docs/api-documentation-guide.md
   - Check out the sample YANG models in yang-models/
   
5. Common Issues:
   - Ensure your device has RESTCONF/NETCONF enabled
   - Verify firewall settings allow connections
   - Check credentials and IP addresses
   - Review device documentation for specific requirements

6. Resources:
   - Cisco DevNet: developer.cisco.com
   - NETCONF/RESTCONF RFCs: tools.ietf.org
   - Course materials and videos
   
Happy automating! 🚀
""")

def main():
    """Main setup function."""
    print("="*60)
    print("Module 5 - RESTCONF & NETCONF Environment Setup")
    print("="*60)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Install packages
    if not install_requirements():
        print("\n⚠ Some packages failed to install. You may need to:")
        print("1. Check your internet connection")
        print("2. Update pip: python -m pip install --upgrade pip")
        print("3. Install packages manually")
        
    # Verify installations
    if not verify_installations():
        print("\n⚠ Some packages could not be verified.")
        print("Try running the examples to see if they work despite verification issues.")
    
    # Create configuration files
    create_sample_config()
    
    # Test functionality
    test_basic_functionality()
    
    # Check network tools
    check_network_connectivity()
    
    # Show next steps
    display_next_steps()

if __name__ == "__main__":
    main()