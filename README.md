# Module 5 Companion: RESTCONF & NETCONF

**Course**: Software Defined Networking - Network Automation  
**Module**: 5 - RESTCONF & NETCONF  
**Level**: Senior (Prerequisite: Linux+, Introduction to Python, Cisco 1,2,3)

## Table of Contents

1. [Introduction to YANG](#introduction-to-yang)
2. [View YANG Data Model for Cisco Catalyst 8k and 9k](#view-yang-data-model)
3. [Review API Documentation](#review-api-documentation)
4. [Create RESTCONF Request using Requests Library](#create-restconf-request)
5. [Parse RESTCONF Output](#parse-restconf-output)
6. [Create NETCONF Request using ncclient Library](#create-netconf-request)
7. [Parse NETCONF Output](#parse-netconf-output)
8. [Setup Instructions](#setup-instructions)

## Learning Objectives

By the end of this module, you will be able to:

- Understand YANG data modeling concepts
- Navigate and interpret YANG models for network devices
- Use RESTCONF APIs to retrieve and configure network devices
- Use NETCONF protocols for network device management
- Parse and process JSON, XML, and YANG data structures
- Apply Python libraries (requests, ncclient) for network automation

## Module Overview

This module focuses on modern network programmability interfaces - RESTCONF and NETCONF - and the YANG data modeling language that underpins them. You'll learn how to interact with Cisco network devices programmatically using standardized APIs.

### Key Technologies Covered

- **YANG**: Data modeling language for network configuration and state data
- **RESTCONF**: HTTP-based protocol providing a REST-like interface to YANG data
- **NETCONF**: Network management protocol using XML over SSH

## Introduction to YANG

YANG (Yet Another Next Generation) is a data modeling language used to model configuration and state data manipulated by network management protocols like NETCONF and RESTCONF.

**Key Concepts:**

- Data models define the structure of configuration and operational data
- Models are organized into modules with namespaces
- Data types, constraints, and relationships are explicitly defined
- Supports hierarchical data organization

📁 **See**: `docs/yang-introduction.md` for detailed explanation

## View YANG Data Model

Cisco Catalyst switches expose their configuration and operational data through YANG models. Understanding these models is crucial for effective network automation.

**Practice Files:**

- `yang-models/` - Sample YANG model excerpts
- `examples/yang_explorer.py` - Script to explore YANG capabilities

## Review API Documentation

Learn to navigate and understand REST API documentation for network devices.

**Resources:**

- `docs/api-documentation-guide.md` - How to read API docs
- `docs/cisco-restconf-reference.md` - Cisco-specific RESTCONF endpoints

## Create RESTCONF Request

Use Python's `requests` library to interact with network devices via RESTCONF.

**Examples:**

- `examples/restconf/basic_get.py` - Basic RESTCONF GET operations
- `examples/restconf/authentication.py` - Authentication methods
- `examples/restconf/configuration.py` - Configuration via RESTCONF

## Parse RESTCONF Output

Learn to process JSON responses from RESTCONF APIs.

**Examples:**

- `examples/restconf/parse_interfaces.py` - Parse interface data
- `examples/restconf/extract_statistics.py` - Extract operational statistics

## Create NETCONF Request

Use the `ncclient` library for NETCONF operations.

**Examples:**

- `examples/netconf/basic_operations.py` - Connect and basic operations
- `examples/netconf/get_config.py` - Retrieve configuration data
- `examples/netconf/edit_config.py` - Modify configuration

## Parse NETCONF Output

Process XML responses from NETCONF operations.

**Examples:**

- `examples/netconf/xml_parsing.py` - Parse XML responses
- `examples/netconf/xpath_queries.py` - Use XPath for data extraction

## Project Structure

```bash
Module-5-Companion/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── setup_environment.py       # Environment setup script
├── docs/                       # Documentation
│   ├── yang-introduction.md
│   ├── api-documentation-guide.md
│   └── cisco-restconf-reference.md
├── examples/                   # Code examples
│   ├── restconf/
│   │   ├── basic_get.py
│   │   ├── authentication.py
│   │   ├── configuration.py
│   │   ├── parse_interfaces.py
│   │   └── extract_statistics.py
│   └── netconf/
│       ├── basic_operations.py
│       ├── get_config.py
│       ├── edit_config.py
│       ├── xml_parsing.py
│       └── xpath_queries.py
├── data/                       # Sample data files
│   ├── json/                   # JSON examples
│   ├── yaml/                   # YAML examples
│   └── xml/                    # XML examples
└── yang-models/                # Sample YANG model excerpts
    ├── cisco-catalyst-interface.yang
    └── cisco-catalyst-routing.yang
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd Module-5-Companion
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script:**

   ```bash
   python setup_environment.py
   ```

## Prerequisites

- Python 3.8 or higher
- Basic understanding of REST APIs
- Familiarity with JSON and XML formats
- Access to Cisco network devices (physical or simulated)

## Additional Resources

- [RFC 7950 - YANG 1.1](https://tools.ietf.org/html/rfc7950)
- [RFC 8040 - RESTCONF Protocol](https://tools.ietf.org/html/rfc8040)  
- [RFC 6241 - NETCONF Protocol](https://tools.ietf.org/html/rfc6241)
- [Cisco DevNet](https://developer.cisco.com/)

## Support

If you encounter issues or have questions:

1. Check the documentation in the `docs/` folder
2. Review the example code for similar use cases
3. Consult the course materials and instructional videos
4. Reach out during office hours or course forum