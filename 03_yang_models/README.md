# Section 03: YANG Models - The Network "Blueprint"

## 📚 What the Heck is YANG?

**YANG = Yet Another Next Generation** (seriously, that's what it stands for!)

Think of YANG as the **"menu" for network devices**. Just like a restaurant menu tells you what food is available and how it's organized, YANG models tell you what data is available on a network device and how it's structured.

### **The Problem YANG Solves**

**Before YANG (CLI Hell):**

```bash
# Every vendor had different commands
Cisco: show ip interface brief
Juniper: show interfaces terse  
Arista: show interfaces status
```

**After YANG (Universal Structure):**

```bash
/ietf-interfaces:interfaces/interface  # Works on ANY device!
```

### **Real-World Analogy**

Imagine you're at a restaurant in a foreign country:

| Restaurant | Network Device |
|------------|----------------|
| Menu shows available dishes | YANG shows available data |
| Organized by sections (appetizers, mains) | Organized by containers (interfaces, routing) |
| Tells you ingredients & price | Tells you data types & constraints |
| Same menu format everywhere | Same YANG structure across vendors |

## 🧱 YANG Building Blocks

### **1. Container = Folder/Group**

Groups related information together

```yaml
container interfaces:
  description: "All interface information"
```

### **2. List = Multiple Items**

Like an array - multiple instances of the same thing

```yaml
list interface:
  key: "name"
  description: "Individual interface"
```

### **3. Leaf = Single Value**

The actual data you want

```yaml
leaf name:
  type: string
  description: "Interface name like GigabitEthernet1"

leaf admin-status:
  type: enumeration
  enum: up, down
```

### **4. Complete Example**

```bash
ietf-interfaces:interfaces          (container)
├── interface                       (list)
    ├── name                       (leaf) = "GigabitEthernet1"
    ├── description               (leaf) = "Link to Server"
    ├── admin-status              (leaf) = "up"
    └── oper-status               (leaf) = "up"
```

## 🌐 YANG to URL Translation

### **YANG Path → RESTCONF URL**

| YANG Concept | YANG Path | RESTCONF URL |
|--------------|-----------|-------------|
| All interfaces | `/ietf-interfaces:interfaces` | `/restconf/data/ietf-interfaces:interfaces` |
| Specific interface | `/ietf-interfaces:interfaces/interface[name="GigabitEthernet1"]` | `/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1` |
| Interface description | `/ietf-interfaces:interfaces/interface[name="GigabitEthernet1"]/description` | `/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1/description` |

### **Translation Rules**

1. Add `/restconf/data/` prefix
2. Replace `[name="value"]` with `=value`
3. Keep the namespace prefix (`ietf-interfaces:`)

## 🏭 Standard vs Vendor Models

### **IETF Standard Models (Work Everywhere)**

- `ietf-interfaces` - Basic interface info
- `ietf-system` - System information (hostname, uptime)
- `ietf-ip` - IP configuration
- `ietf-routing` - Routing tables

### **Cisco Vendor Models (Cisco Only)**

- `Cisco-IOS-XE-native` - Full CLI configuration
- `Cisco-IOS-XE-interfaces` - Extended interface features
- `Cisco-IOS-XE-bgp` - BGP routing protocol

### **When to Use Which?**

- **Standard Models**: Use for basic operations that work across vendors
- **Vendor Models**: Use for advanced features specific to that vendor

## 🔍 Finding Available YANG Models

### **Discovery Endpoints**

```python
# See all available YANG models
"/restconf/data/ietf-yang-library:yang-library"

# See device capabilities  
"/restconf/data/ietf-restconf-monitoring:restconf-state/capabilities"
```

### **Common Patterns to Try**

```python
# System information
"/ietf-system:system"
"/ietf-system:system-state"

# Interface information
"/ietf-interfaces:interfaces"
"/ietf-interfaces:interfaces-state"

# Routing information
"/ietf-routing:routing"
"/ietf-ip:ipv4"
```

## 🎯 Learning Goals

By the end of this module, you'll understand:

- [ ] What YANG models are and why they exist
- [ ] How to navigate YANG hierarchies (container → list → leaf)
- [ ] The difference between standard and vendor models
- [ ] How to translate YANG paths to RESTCONF URLs
- [ ] Where to find available models on a device
- [ ] How to explore YANG structure through API responses

## 💡 Pro Tips

**Start with Standard Models**: `ietf-interfaces` and `ietf-system` work on almost every device.

**Explore Responses**: The JSON structure mirrors the YANG structure - use it to understand the hierarchy.

**Use Browser Tools**: You can explore YANG models visually with tools like YANG Suite.

**Check Namespaces**: The part before the `:` is the namespace - it tells you which YANG model you're using.

## 🚀 Ready to Explore?

Open `yang_explorer.py` and start mapping the blueprint of your network device!
