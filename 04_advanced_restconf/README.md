# Section 04: RESTCONF Configuration Management

## 📚 Making Real Changes to Network Devices

**You've been reading data - now it's time to CHANGE it!** This module teaches you how to safely modify network device configurations using RESTCONF.

### **⚠️ IMPORTANT SAFETY WARNING**

You're about to make **REAL configuration changes** to network devices. These changes can:

- Disrupt network connectivity
- Break device functionality  
- Cause outages if done incorrectly

**Always follow the "Read-Modify-Write" pattern!**

## 🔧 HTTP Methods for Network Configuration

### **The CRUD Operations**

| HTTP Method | Purpose | Network Example | Risk Level |
|-------------|---------|----------------|------------|
| **GET** | Read data | `show interfaces` | 🟢 Safe |
| **POST** | Create new | Add new interface | 🟡 Medium |
| **PUT** | Replace/Update | Change interface description | 🟡 Medium |
| **PATCH** | Modify partially | Update specific setting | 🟡 Medium |
| **DELETE** | Remove | Delete interface config | 🔴 High |

### **Safe Configuration Workflow**

```python
# 1. READ current configuration
current_config = requests.get(url, auth=auth, headers=headers)

# 2. MODIFY the configuration data  
modified_config = current_config.copy()
modified_config["description"] = "New description"

# 3. WRITE the updated configuration
response = requests.put(url, auth=auth, headers=headers, json=modified_config)

# 4. VERIFY the change was applied
verify = requests.get(url, auth=auth, headers=headers)
```

## 🎯 PUT vs POST vs PATCH

### **PUT - Replace Entire Resource**

```python
# PUT replaces the ENTIRE interface configuration
interface_config = {
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet1",
        "description": "Updated via RESTCONF",
        "enabled": True,
        "type": "iana-if-type:ethernetCsmacd"
    }
}

response = requests.put(
    "https://device/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1",
    auth=(user, pass),
    headers={"Content-Type": "application/yang-data+json"},
    json=interface_config
)
```

### **PATCH - Modify Specific Fields**

```python
# PATCH only changes specific fields
description_change = {
    "ietf-interfaces:description": "New description only"
}

response = requests.patch(
    "https://device/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1",
    auth=(user, pass),
    headers={"Content-Type": "application/yang-data+json"},
    json=description_change
)
```

### **POST - Create New Resources**

```python
# POST creates new configuration (like new VLAN)
new_interface = {
    "ietf-interfaces:interface": {
        "name": "Loopback100", 
        "description": "Created via RESTCONF",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True
    }
}

response = requests.post(
    "https://device/restconf/data/ietf-interfaces:interfaces",
    auth=(user, pass),
    headers={"Content-Type": "application/yang-data+json"},
    json=new_interface
)
```

## �️ Error Handling & Rollback

### **HTTP Status Codes for Configuration**

| Status Code | Meaning | Action |
|-------------|---------|--------|
| **200/201** | Success | Configuration applied ✅ |
| **400** | Bad Request | Check your JSON syntax |
| **401** | Unauthorized | Check credentials |
| **404** | Not Found | Check URL/resource exists |
| **409** | Conflict | Resource already exists/locked |
| **500** | Server Error | Device problem - investigate |

### **Rollback Strategy**

```python
def safe_config_change(url, new_config):
    # 1. Backup current configuration
    backup = requests.get(url, auth=auth, headers=headers)
    if backup.status_code != 200:
        raise Exception("Can't backup current config!")
    
    original_config = backup.json()
    
    try:
        # 2. Apply new configuration  
        response = requests.put(url, auth=auth, headers=headers, json=new_config)
        
        if response.status_code not in [200, 201, 204]:
            raise Exception(f"Config failed: {response.status_code}")
            
        # 3. Verify the change
        verify = requests.get(url, auth=auth, headers=headers)
        # Add verification logic here...
        
        return True
        
    except Exception as e:
        # 4. Rollback on any error
        print(f"Error occurred: {e}")
        print("Rolling back to original configuration...")
        rollback = requests.put(url, auth=auth, headers=headers, json=original_config)
        return False
```

## 🎯 Common Configuration Tasks

### **1. Interface Description Changes** (Safest)

```python
url = "/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1/description"
new_description = "Link to Server Room A"

response = requests.put(url, auth=auth, headers=headers, json=new_description)
```

### **2. Enable/Disable Interface** (Medium Risk)

```python
url = "/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1/enabled"
enable_interface = True  # or False to disable

response = requests.put(url, auth=auth, headers=headers, json=enable_interface)
```

### **3. IP Address Configuration** (Higher Risk)

```python
ip_config = {
    "ietf-ip:ipv4": {
        "address": [{
            "ip": "192.168.1.1",
            "prefix-length": 24
        }]
    }
}

url = "/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1/ietf-ip:ipv4"
response = requests.put(url, auth=auth, headers=headers, json=ip_config)
```

## 🎯 Learning Goals

By the end of this module, you'll:

- [ ] Understand when to use PUT vs POST vs PATCH vs DELETE
- [ ] Implement the "Read-Modify-Write" pattern safely
- [ ] Handle configuration errors and implement rollback
- [ ] Make common configuration changes (descriptions, enable/disable)
- [ ] Validate configuration changes after applying them
- [ ] Build robust, production-ready configuration functions

## 💡 Pro Tips

**Always Test First**: Try configuration changes on lab devices before production.

**Use Specific URLs**: Target the exact field you want to change, not the entire interface.

**Check Before and After**: Always verify your changes were applied correctly.

**Have a Rollback Plan**: Save original configuration before making changes.

**Start Simple**: Begin with descriptions, then move to more critical settings.

## 🚀 Ready to Configure?

Open `advanced_config.py` and start making safe configuration changes!
