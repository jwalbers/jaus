1. jaus2jsidl: Comments from CJSIDL fields are not making it into JSIDL interpretation.

    record PlatformSpecificationsRec {
      required string MobilityPlatformName = 1; // A human-readable string for the vehicle.
      optional uint16 Front meter = 3; // Measured from the vehicle coordinate frame.


      <variable_length_string name="MobilityPlatformName" optional="false">
        <count_field min_count="0" max_count="15" field_type_unsigned="unsigned integer"/>
      </variable_length_string>
      <fixed_field field_type="unsigned short integer" name="Front" optional="true" field_units="meter"/>

This is likely related to the parser generator error:

warning(200): jaus2jsidl.g:1769:66: Decision can match input such as "SL_COMMENT" using multiple alternatives: 1, 2
As a result, alternative(s) 2 were disabled for that input


2. jsidl2jaus: not fully supporting protocol_behavior grammar yet.  e.g. guard_condition.
