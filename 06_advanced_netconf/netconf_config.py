"""
Section 06: NETCONF Configuration Management

TODO: Master configuration changes using NETCONF transactions
CHALLENGE: Use NETCONF's advanced features for safer config changes!

NETCONF Advantages:
- Transactions: All-or-nothing configuration changes
- Rollback: Undo changes if something goes wrong  
- Validation: Check config before applying
- Locking: Prevent conflicts with other users

WARNING: Real configuration changes ahead!
"""

# TODO: Import ncclient and XML libraries

def netconf_configuration_basics():
    """
    TODO: Learn NETCONF edit-config operation
    
    CHALLENGE: Use session.edit_config() to make changes
    - target parameter: 'running', 'candidate', 'startup'
    - config parameter: XML configuration data
    - Different from RESTCONF PUT/PATCH approach
    
    Hint: XML configuration format is more verbose than JSON
    """
    pass

def build_xml_configuration():
    """
    TODO: Learn to construct XML configuration data
    
    CHALLENGE: Build XML for interface description change
    Structure needed:
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>GigabitEthernet1</name>
          <description>Changed via NETCONF</description>
        </interface>
      </interfaces>
    </config>
    
    Hint: Mind the XML namespaces - they're critical!
    """
    pass

def use_candidate_configuration():
    """
    TODO: Use NETCONF's candidate configuration feature
    
    CHALLENGE: Implement safe config workflow:
    1. Edit candidate configuration (not running)
    2. Validate the candidate config  
    3. Commit candidate to running (or discard if invalid)
    
    Advantage: Changes can be tested before applying!
    """
    pass

def configuration_rollback():
    """
    TODO: Implement configuration rollback capability
    
    CHALLENGE: 
    1. Save current configuration
    2. Make configuration change
    3. Test the change
    4. Rollback if test fails
    
    Methods to explore:
    - session.copy_config() for backup
    - session.discard_changes() for candidate rollback
    """
    pass

def netconf_locking():
    """
    TODO: Use NETCONF locks to prevent configuration conflicts
    
    CHALLENGE: Implement proper locking workflow:
    1. Lock the configuration datastore
    2. Make your changes safely
    3. Always unlock when done (even if error occurs)
    
    Hint: Use try/finally or context managers for guaranteed unlock!
    """
    pass

def validate_before_commit():
    """
    TODO: Use NETCONF validation to check config before applying
    
    CHALLENGE: 
    1. Edit candidate configuration
    2. Use session.validate() to check it
    3. Only commit if validation passes
    4. Show validation error messages if fails
    
    Question: Why is validation better than "hope and pray"?
    """
    pass

def bulk_configuration_with_transaction():
    """
    TODO: Make multiple related changes in one transaction
    
    CHALLENGE: Configure multiple interfaces in single transaction:
    - Change descriptions on several interfaces
    - Enable/disable multiple interfaces  
    - All succeed together or all fail together
    
    Hint: Build one large XML config with multiple interfaces
    """
    pass

# TODO: Create main() with step-by-step NETCONF config workflow

# TODO: Add comprehensive error handling and cleanup
