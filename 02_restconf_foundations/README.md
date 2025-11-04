# Section 02: RESTCONF Foundations

## 📚 What is RESTCONF?

**RESTCONF = REST + NETCONF**. It's a way to manage network devices using familiar HTTP methods (GET, POST, PUT, DELETE) that you already learned in Module 4!

### **The Problem RESTCONF Solves**

Traditional network management:

```bash
# Old way - manual CLI commands
ssh admin@router
show interfaces
configure terminal
interface GigabitEthernet1
description "Updated via CLI"
```

Modern network management:

```python
# New way - programmatic API calls
response = requests.get("https://router/restconf/data/interfaces")
data = response.json()
```

### **Why RESTCONF Matters**

- **Familiar**: Uses HTTP methods you already know
- **Standardized**: RFC 8040 standard (works across vendors)
- **JSON**: Returns data in JSON format (easy to parse)
- **Secure**: Uses HTTPS with authentication
- **Scalable**: Can manage hundreds of devices with code

## 🔧 RESTCONF Fundamentals

### **HTTP Methods = Network Operations**

| HTTP Method | Network Purpose | Example |
|-------------|----------------|---------|
| GET | Read configuration/status | Get interface information |
| POST | Create new configuration | Add new interface |
| PUT | Update/replace configuration | Change interface description |
| PATCH | Modify part of configuration | Update specific settings |
| DELETE | Remove configuration | Delete interface |

### **URL Structure Explained**

```bash
https://HOST/restconf/data/YANG-MODEL-PATH
```

**Example URLs:**

```python
# Get device hostname
"/restconf/data/ietf-system:system-state/hostname"

# Get all interfaces  
"/restconf/data/ietf-interfaces:interfaces"

# Get specific interface
"/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1"
```

### **Required Headers**

```python
headers = {
    "Accept": "application/yang-data+json",        # Want JSON response
    "Content-Type": "application/yang-data+json"   # Sending JSON data
}
```

### **Authentication (Same as Module 4!)**

```python
# Basic auth (most common in labs)
auth = ("admin", "password")

# Or session-based

session = requests.Session()
session.auth = ("admin", "password")
```

## 🎯 Building Blocks You'll Master

### **1. Basic GET Operations**

```python
# Template for RESTCONF GET
response = requests.get(
    url="https://device/restconf/data/path",
    auth=(username, password),
    headers={"Accept": "application/yang-data+json"},
    verify=False  # Lab only!
)

if response.status_code == 200:
    data = response.json()
    # Process data...
```

### **2. Error Handling**

RESTCONF uses standard HTTP status codes:

- **200** = Success
- **401** = Authentication failed
- **404** = Resource not found
- **500** = Server error

### **3. Data Processing**

```python
# Example: Extract interface names
interfaces_data = response.json()
interface_list = interfaces_data["ietf-interfaces:interfaces"]["interface"]
for interface in interface_list:
    print(interface["name"])
```

## 🎯 Learning Goals

By the end of this module, you'll:

- [ ] Apply Module 4 requests skills to network devices
- [ ] Understand RESTCONF URL patterns and YANG paths
- [ ] Extract useful information from JSON responses
- [ ] Handle authentication and headers properly
- [ ] Build reusable functions for network data retrieval
- [ ] Debug common RESTCONF issues

## 💡 Pro Tips

**Start with Working Code**: Copy a working requests example from Module 4, then modify the URL and headers for RESTCONF.

**Use Browser Tools**: You can test RESTCONF URLs in a browser (with basic auth) to see the JSON response.

**Check Status Codes**: Always check `response.status_code` before processing JSON.

**Print Responses**: Use `print(response.text)` to see raw responses when debugging.

## 🚀 Ready to Code?

Open `restconf_basics.py` and start building your first network automation functions!
