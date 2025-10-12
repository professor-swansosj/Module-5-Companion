# Introduction to YANG Data Modeling

## What is YANG?

YANG (Yet Another Next Generation) is a data modeling language used to model configuration and state data manipulated by network management protocols like NETCONF and RESTCONF.

## Key Concepts

### Data Models

- Define the structure of configuration and operational data
- Specify constraints, types, and relationships
- Provide a contract between client and server

### Modules and Namespaces

- YANG models are organized into modules
- Each module has a unique namespace
- Modules can import other modules

### Data Types

YANG supports various built-in types:

- `int8`, `int16`, `int32`, `int64` - Integer types
- `uint8`, `uint16`, `uint32`, `uint64` - Unsigned integer types
- `string` - Text strings
- `boolean` - True/false values
- `enumeration` - Predefined set of values
- `leafref` - Reference to another data node

### Node Types

#### Container

Groups related data nodes together:

```yang
container interface {
    description "Interface configuration";
    
    leaf name {
        type string;
        description "Interface name";
    }
    
    leaf enabled {
        type boolean;
        default true;
        description "Administrative status";
    }
}
```

#### List

Represents multiple instances of the same data structure:

```yang
list interface {
    key "name";
    description "List of interfaces";
    
    leaf name {
        type string;
        description "Interface identifier";
    }
    
    leaf mtu {
        type uint16;
        default 1500;
        description "Maximum transmission unit";
    }
}
```

#### Leaf

Single data value:

```yang
leaf hostname {
    type string;
    description "System hostname";
}
```

#### Leaf-list

Array of simple values:

```yang
leaf-list dns-server {
    type inet:ip-address;
    description "List of DNS server addresses";
}
```

## YANG Tree Structure

YANG models create a hierarchical tree structure. Here's an example for interface configuration:

```bash
+--rw interfaces
   +--rw interface* [name]
      +--rw name           string
      +--rw description?   string
      +--rw enabled?       boolean
      +--rw mtu?           uint16
      +--ro oper-status?   enumeration
      +--ro statistics
         +--ro in-octets?     yang:counter64
         +--ro out-octets?    yang:counter64
```

Legend:

- `+--rw` = read-write (configuration data)
- `+--ro` = read-only (operational data)
- `*` = list (multiple instances)
- `?` = optional node

## Cisco Catalyst YANG Models

Cisco devices expose their functionality through YANG models organized into several categories:

### Common Models

- `ietf-interfaces` - Standard interface model
- `ietf-ip` - IP configuration
- `ietf-routing` - Routing configuration

### Cisco-Specific Models

- `cisco-ios-xe-interfaces` - Cisco interface extensions
- `cisco-ios-xe-native` - Native IOS-XE configuration
- `cisco-ios-xe-bgp` - BGP configuration

### Model Categories

1. **Configuration Models** - Writeable data (configuration)
2. **Operational Models** - Read-only data (statistics, status)
3. **Notification Models** - Event notifications

## Exploring YANG Models

### Using NETCONF Capabilities

Query device capabilities to see available models:

```python
from ncclient import manager

with manager.connect(host="192.168.1.1", port=830, 
                    username="admin", password="password",
                    hostkey_verify=False) as m:
    for capability in m.server_capabilities:
        print(capability)
```

### Using RESTCONF

Get available data models via RESTCONF:

```bash
GET https://device-ip/restconf/data/ietf-yang-library:modules-state
```

## Best Practices

1. **Start Simple** - Begin with basic models like interfaces
2. **Understand Hierarchy** - Learn the tree structure before coding
3. **Check Capabilities** - Always verify what models the device supports
4. **Use Documentation** - Refer to Cisco DevNet for model documentation
5. **Validate Data** - Use YANG constraints to ensure data integrity

## Next Steps

Now that you understand YANG basics:

1. Explore sample YANG models in `../yang-models/`
2. Practice with RESTCONF examples in `../examples/restconf/`
3. Try NETCONF operations in `../examples/netconf/`

## Additional Resources

- [RFC 7950 - YANG 1.1](https://tools.ietf.org/html/rfc7950)
- [Cisco DevNet YANG Models](https://github.com/YangModels/yang)
- [YANG Explorer Tool](https://github.com/CiscoDevNet/yang-explorer)
