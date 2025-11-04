# Section 01: Network Device Explorer

## 🎯 What You'll Learn

**Welcome to Network Programmability!** You're about to discover how to talk to network devices using code instead of CLI commands. This is the foundation of network automation.

## 📚 Key Concepts

### **What is Network Programmability?**

Instead of logging into devices and typing commands like `show interfaces`, you can write Python code that gets the same information automatically. Think of it as APIs for network equipment!

### **Two Main Approaches**

1. **RESTCONF** - Uses HTTP/HTTPS (like web APIs you know)
2. **NETCONF** - Uses SSH with XML (more powerful but different)

### **Why Both Exist?**

- **RESTCONF** = Easier for developers, JSON responses, HTTP-based
- **NETCONF** = More features (transactions, rollback), XML-based

### **What You Already Know**

From Module 4, you learned to use the `requests` library to call APIs. **RESTCONF is just another API!** Same concepts:

- Base URLs
- Authentication
- Headers
- GET requests
- JSON responses

## 🔧 Connection Basics

### **Lab Device Info**

```python
# Your sandbox device (always available)
HOST = "sandbox-iosxe-latest-1.cisco.com"
USERNAME = "admin"
PASSWORD = "C1sco12345"

# RESTCONF uses HTTPS on port 443 (default)
# NETCONF uses SSH on port 830
```

### **RESTCONF Headers**

```python
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
```

### **Disabling SSL Warnings (Lab Only!)**
```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## 🎯 Learning Goals

By the end of this module, you'll:
- [ ] Understand the difference between RESTCONF and NETCONF
- [ ] Make your first connection to a network device
- [ ] Explore what data is available on the device
- [ ] Compare JSON vs XML responses for the same data
- [ ] Build confidence that this is just "APIs for network devices"

## 💡 Pro Tips

**Start with `help()`**: Use Python's built-in help to explore libraries
```python
help(requests)
dir(requests)
```

**URL Structure**: RESTCONF URLs look like:
```
https://HOST/restconf/data/YANG-PATH
```

**Try Different Endpoints**:
- `/ietf-system:system-state/hostname` - Get device name
- `/ietf-interfaces:interfaces` - Get all interfaces
- `/ietf-yang-library:yang-library` - See what's available

## 🚀 Ready to Start?

Open `device_explorer.py` and start connecting to your first network device!
