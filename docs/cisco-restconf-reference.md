# Cisco RESTCONF API Reference Guide

## Overview

This guide provides quick reference information for working with Cisco RESTCONF APIs on Catalyst switches and routers. It covers common endpoints, request patterns, and response formats.

## Base URL Structure

```bash
https://{device-ip}:{port}/restconf
```

- **Default Port**: 443 (HTTPS)
- **Protocol**: HTTPS only
- **Authentication**: HTTP Basic Auth or Token-based

## Common Headers

### Request Headers

```bash
Accept: application/yang-data+json
Content-Type: application/yang-data+json
Authorization: Basic {base64-encoded-credentials}
```

### Response Headers

```bash
Content-Type: application/yang-data+json
Server: nginx/1.x.x
```

## Core Endpoints

### 1. Capabilities and Discovery

#### Get RESTCONF Root Resource

```bash
GET /restconf
```

Returns: Links to available resources and capabilities

#### Get Yang Library Modules

```bash
GET /restconf/data/ietf-yang-library:modules-state
```

Returns: List of available YANG modules

#### Get Device Capabilities

```bash
GET /restconf/data/ietf-restconf-monitoring:restconf-state/capabilities
```

Returns: RESTCONF capabilities supported by device

### 2. Interface Management

#### Get All Interfaces

```bash
GET /restconf/data/ietf-interfaces:interfaces
```

Returns: Configuration of all interfaces

#### Get Specific Interface

```bash
GET /restconf/data/ietf-interfaces:interfaces/interface={name}
```

Parameters:

- `name`: Interface identifier (URL encoded)

#### Create Interface

```bash
POST /restconf/data/ietf-interfaces:interfaces
Content-Type: application/yang-data+json

{
  "ietf-interfaces:interface": {
    "name": "Loopback100",
    "description": "Test Interface",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true
  }
}
```

#### Update Interface (Full Replace)

```bash
PUT /restconf/data/ietf-interfaces:interfaces/interface={name}
Content-Type: application/yang-data+json

{
  "ietf-interfaces:interface": {
    "name": "GigabitEthernet1/0/1",
    "description": "Updated Description", 
    "enabled": true
  }
}
```

#### Update Interface (Partial)

```bash
PATCH /restconf/data/ietf-interfaces:interfaces/interface={name}
Content-Type: application/yang-data+json

{
  "ietf-interfaces:interface": {
    "description": "New Description"
  }
}
```

#### Delete Interface

```bash
DELETE /restconf/data/ietf-interfaces:interfaces/interface={name}
```

### 3. Interface Statistics (Operational Data)

#### Get Interface Statistics

```bash
GET /restconf/data/ietf-interfaces:interfaces-state/interface={name}/statistics
```

Returns: Counters and operational statistics

#### Get All Interface States

```bash
GET /restconf/data/ietf-interfaces:interfaces-state
```

Returns: Operational state of all interfaces

### 4. System Configuration

#### Get System Information

```bash
GET /restconf/data/ietf-system:system
```

Returns: System configuration (hostname, contact, location, etc.)

#### Update Hostname

```bash
PUT /restconf/data/ietf-system:system/hostname
Content-Type: application/yang-data+json

{
  "ietf-system:hostname": "NEW-HOSTNAME"
}
```

#### Get System State

```bash
GET /restconf/data/ietf-system:system-state
```

Returns: System operational information

### 5. Routing Information

#### Get Routing Table

```bash
GET /restconf/data/ietf-routing:routing/routing-instance=default/ribs/rib=ipv4-default/routes
```

Returns: IPv4 routing table entries

#### Get OSPF Configuration

```bash
GET /restconf/data/ietf-routing:routing/control-plane-protocols/control-plane-protocol=ietf-ospf:ospfv2,{instance-name}
```

Returns: OSPF protocol configuration

### 6. VLAN Configuration (Cisco-Specific)

#### Get VLAN Database

```bash
GET /restconf/data/cisco-ios-xe-vlan:vlans
```

Returns: VLAN configuration database

#### Create VLAN

```bash
POST /restconf/data/cisco-ios-xe-vlan:vlans
Content-Type: application/yang-data+json

{
  "cisco-ios-xe-vlan:vlan": {
    "vlan-id": 100,
    "name": "SERVERS",
    "status": "active"
  }
}
```

## Query Parameters

### Depth Control

```bash
GET /restconf/data/ietf-interfaces:interfaces?depth=1
```

Limits response depth to specified level

### Field Selection

```bash
GET /restconf/data/ietf-interfaces:interfaces/interface={name}?fields=name;description;enabled
```

Returns only specified fields

### Content Type Selection

```bash
GET /restconf/data/ietf-interfaces:interfaces?content=config
GET /restconf/data/ietf-interfaces:interfaces?content=nonconfig  
GET /restconf/data/ietf-interfaces:interfaces?content=all
```

Filters configuration vs operational data

## Response Formats

### Successful Responses

#### HTTP 200 (OK) - GET Request

```json
{
  "ietf-interfaces:interface": {
    "name": "GigabitEthernet1/0/1",
    "description": "Sample Interface",
    "type": "iana-if-type:ethernetCsmacd",
    "enabled": true,
    "ietf-ip:ipv4": {
      "enabled": true,
      "address": [
        {
          "ip": "192.168.1.1",
          "netmask": "255.255.255.0"
        }
      ]
    }
  }
}
```

#### HTTP 201 (Created) - POST Request

```json
{
  "location": "/restconf/data/ietf-interfaces:interfaces/interface=Loopback100"
}
```

#### HTTP 204 (No Content) - PUT/PATCH/DELETE

No response body

### Error Responses

#### HTTP 400 (Bad Request)

```json
{
  "ietf-restconf:errors": {
    "error": [
      {
        "error-type": "application",
        "error-tag": "invalid-value",
        "error-message": "Invalid interface name format"
      }
    ]
  }
}
```

#### HTTP 401 (Unauthorized)

```json
{
  "ietf-restconf:errors": {
    "error": [
      {
        "error-type": "protocol", 
        "error-tag": "access-denied",
        "error-message": "Authentication required"
      }
    ]
  }
}
```

#### HTTP 404 (Not Found)

```json
{
  "ietf-restconf:errors": {
    "error": [
      {
        "error-type": "application",
        "error-tag": "invalid-value", 
        "error-message": "Interface not found"
      }
    ]
  }
}
```

#### HTTP 409 (Conflict)

```json
{
  "ietf-restconf:errors": {
    "error": [
      {
        "error-type": "application",
        "error-tag": "data-exists",
        "error-message": "Interface already exists"
      }
    ]
  }
}
```

## Best Practices

### 1. URL Encoding

Always URL encode interface names and other path parameters:

```python
import urllib.parse
encoded_name = urllib.parse.quote("GigabitEthernet1/0/1", safe='')
url = f"/restconf/data/ietf-interfaces:interfaces/interface={encoded_name}"
```

### 2. Error Handling

Always check HTTP status codes and parse error responses:

```python
if response.status_code != 200:
    error_info = response.json()
    error_message = error_info.get('ietf-restconf:errors', {}).get('error', [{}])[0].get('error-message', 'Unknown error')
    print(f"Error: {error_message}")
```

### 3. Content Negotiation

Specify accept headers for desired response format:

```python
headers = {
    'Accept': 'application/yang-data+json',  # Preferred
    # 'Accept': 'application/yang-data+xml'  # Alternative
}
```

### 4. Pagination

For large datasets, use query parameters to limit response size:

```bash
GET /restconf/data/ietf-interfaces:interfaces?depth=2&limit=10&offset=0
```

### 5. Transaction Safety

Use appropriate HTTP methods:

- **GET**: Read data (safe, idempotent)
- **PUT**: Replace entire resource (idempotent)  
- **PATCH**: Partial update (not idempotent)
- **POST**: Create new resource (not idempotent)
- **DELETE**: Remove resource (idempotent)

## Common YANG Namespaces

| Prefix | Namespace | Description |
|--------|-----------|-------------|
| ietf-interfaces | urn:ietf:params:xml:ns:yang:ietf-interfaces | Standard interface model |
| ietf-ip | urn:ietf:params:xml:ns:yang:ietf-ip | IP configuration |
| ietf-system | urn:ietf:params:xml:ns:yang:ietf-system | System configuration |
| ietf-routing | urn:ietf:params:xml:ns:yang:ietf-routing | Routing configuration |
| cisco-ios-xe-native | http://cisco.com/ns/yang/Cisco-IOS-XE-native | Cisco native configuration |
| cisco-ios-xe-interfaces | http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces | Cisco interface extensions |

## Debugging Tips

### 1. Enable Request Logging

```python
import logging
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
```

### 2. Use curl for Testing

```bash
curl -k -u admin:password \
  -H "Accept: application/yang-data+json" \
  https://192.168.1.1/restconf/data/ietf-interfaces:interfaces
```

### 3. Validate JSON Payloads

Use online JSON validators or Python jsonschema library to validate request payloads before sending.

### 4. Check Device Documentation

Always refer to device-specific RESTCONF documentation for:

- Supported YANG models
- Vendor-specific extensions  
- Configuration limitations
- Feature availability by software version

## Security Considerations

### 1. Always Use HTTPS

RESTCONF should always be used over HTTPS to protect credentials and data.

### 2. Strong Authentication

- Use strong passwords
- Consider certificate-based authentication  
- Implement proper access control

### 3. Rate Limiting

Be aware of device rate limits and implement appropriate delays between requests.

### 4. Input Validation  

Always validate and sanitize input data before sending to device.

## Additional Resources

- [RFC 8040 - RESTCONF Protocol](https://tools.ietf.org/html/rfc8040)
- [Cisco DevNet RESTCONF Documentation](https://developer.cisco.com/docs/ios-xe)
- [YANG Models Repository](https://github.com/YangModels/yang)
- [Cisco IOS XE YANG Models](https://github.com/YangModels/yang/tree/master/vendor/cisco/xe)