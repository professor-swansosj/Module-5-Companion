# Module 05: NETCONF Fundamentals

## 📚 What is NETCONF and Why Should You Care?

**NETCONF = Network Configuration Protocol**. Think of it as the "enterprise database connection" for network devices, while RESTCONF is more like "web API calls."

### **NETCONF vs RESTCONF - The Big Picture**

| Feature | RESTCONF | NETCONF |
|---------|----------|---------|
| **Transport** | HTTP/HTTPS | SSH |
| **Data Format** | JSON | XML |
| **Connection** | Stateless (like web browsing) | Stateful (like database connection) |
| **Transactions** | No | Yes (all-or-nothing changes) |
| **Rollback** | Manual | Built-in |
| **Locking** | No | Yes (prevent conflicts) |
| **Validation** | Limited | Full validation before applying |
| **Learning Curve** | Easy (you know HTTP) | Harder (XML + SSH) |

### **When to Use Which?**

**Use RESTCONF for:**

- Simple operations (get status, basic config changes)
- Web integrations
- Quick scripts and automation
- When you want JSON responses

**Use NETCONF for:**

- Complex configuration changes
- Mission-critical operations (banking, telecom)
- When you need transactions and rollback
- Bulk configuration changes
- When you need to lock configurations

## 🔌 NETCONF Connection Basics

### **Connection Parameters**

```python
from ncclient import manager

# NETCONF uses SSH, not HTTP
connection_params = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "port": 830,  # Standard NETCONF port
    "username": "admin",
    "password": "C1sco12345",
    "hostkey_verify": False,  # Lab only!
    "device_params": {"name": "iosxe"}  # Cisco-specific
}

# Context manager automatically closes connection
with manager.connect_ssh(**connection_params) as session:
    # Do NETCONF operations here
    pass
```

### **Key Difference: Stateful Connection**

Unlike RESTCONF (where each request is independent), NETCONF maintains a session:

```python
# RESTCONF - each request is separate
response1 = requests.get(url1)  # Independent request
response2 = requests.get(url2)  # Independent request

# NETCONF - one connection, multiple operations  
with manager.connect_ssh(...) as session:
    data1 = session.get_config(source="running")  # Same session
    data2 = session.get(filter=filter_xml)       # Same session
    session.edit_config(config=new_config)       # Same session
```

## 🎯 NETCONF Operations

### **1. get_config() - Get Configuration Data**

```python
# Get running configuration (like "show running-config")
config = session.get_config(source="running")

# Other datastores
startup_config = session.get_config(source="startup")
candidate_config = session.get_config(source="candidate")  # If supported
```

### **2. get() - Get Operational Data**

```python
# Get operational state (like "show interfaces")
state_data = session.get()

# With filter to get specific data
filter_xml = '''
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
</interfaces>
'''
interfaces = session.get(filter=("subtree", filter_xml))
```

### **3. Device Capabilities**

```python
# See what the device supports
capabilities = session.server_capabilities
for capability in capabilities:
    print(capability)
```

## 📄 Working with XML (Not JSON!)

### **Why XML Instead of JSON?**

- **Namespaces**: Prevent naming conflicts between different YANG models
- **Validation**: Built-in schema validation  
- **Standards**: XML has mature parsing and validation tools
- **NETCONF History**: Protocol predates JSON popularity

### **Basic XML Parsing**

```python
import xml.etree.ElementTree as ET

# Parse NETCONF response
xml_response = session.get_config(source="running")
xml_string = str(xml_response)  # Convert to string
root = ET.fromstring(xml_string)

# Find elements (mind the namespaces!)
interfaces = root.findall('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}interface')
for interface in interfaces:
    name = interface.find('{urn:ietf:params:xml:ns:yang:ietf-interfaces}name')
    if name is not None:
        print(f"Interface: {name.text}")
```

### **XML Namespaces Explained**

XML uses namespaces to avoid conflicts:

```xml
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface>
    <name>GigabitEthernet1</name>
  </interface>
</interfaces>
```

The `xmlns=` part defines the namespace. You need this when searching XML!

## 🔒 NETCONF Advanced Features

### **1. Datastores**

- **running** - Active configuration (like "show run")
- **candidate** - Proposed configuration (edit safely, then commit)
- **startup** - Configuration loaded on boot

### **2. Transactions**

```python
# All changes succeed together, or all fail together
session.lock(target="candidate")          # Lock config
session.edit_config(target="candidate", config=change1)  # Stage change 1
session.edit_config(target="candidate", config=change2)  # Stage change 2
session.commit()                          # Apply all changes
session.unlock(target="candidate")        # Release lock
```

### **3. Validation**

```python
# Test configuration before applying
session.validate(source="candidate")  # Check if config is valid
```

## 🎯 Learning Goals

By the end of this module, you'll understand:

- [ ] Why NETCONF exists and when to use it over RESTCONF
- [ ] How to establish SSH connections with ncclient
- [ ] The difference between get_config() and get() operations
- [ ] Basic XML parsing for NETCONF responses  
- [ ] NETCONF's advanced features (transactions, locking, validation)
- [ ] How to explore device capabilities

## 💡 Pro Tips

**Start with Capabilities**: Always check `session.server_capabilities` to see what the device supports.

**Use Context Managers**: Always use `with manager.connect_ssh()` to ensure connections close properly.

**XML Namespaces**: Don't ignore them! They're required for reliable XML parsing.

**Filtering**: Use filters to get only the data you need - NETCONF responses can be huge.

**Error Handling**: NETCONF operations can raise exceptions - always use try/except blocks.

## 🚀 Ready for Enterprise Network Management?

Open `netconf_basics.py` and master the powerful world of NETCONF!