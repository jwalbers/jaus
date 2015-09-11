ddsidlTools
---------------------------------------------------------

Tools for working generating DDS IDL (CORBA 3.2) from AS-4 JAUS
Service Interface Definition Language (JSIDL) files, per SAE ARP6227

Copyright 2013 Jim Albers

$Id: README.txt 111 2013-08-27 01:02:28Z jalbers $

Help
============

If your installation is successful and you are having issues, please
take a close look at the contents of the ./test directory.  Make sure
you can run the unittest.sh script and get the results shown in
test/README.txt.

Developers
============

Do not commit any changes to the cjsidlTools repository unless your
code passes the ./test/unittest.sh.

If you discover and fix any bugs, make sure to add to the unit test a JSIDL
.xml file that demonstrates the bug, and shows that it is resolved.

Known Issues
============

1.  Current revision handles declared_type_sets as follows:
    -- declared_type_set_ref elements are translated into 'import <scoped_name>;' statements.
    -- Actual declarations, if any, are produced in module with the name of the declared type set.

    It is LIKELY that the import statements and declared type set handling is not yet correct
    for some or all DDS IDL compilers.

2. Preprocessor statements like #pragma and #include are currently
   included in the dds_idl.g grammar to make it easier to validate IDL
   files.  In real production systems should separate preprocessor from
   parser.
  

Installation ============

Prerequisites:

Python 2.7
Python lxml etree package (for DOM processing)

Install setuptools (http://pypi.python.org/pypi/setuptools), then:

$ easy_install lxml

This installation was tested with Python 2.7.1 and lxml 2.3


Translating from JSIDL XML to DDS IDL
====================================

Make sure that the jsidl2id.py script has execute permissions, or start it with python.

For the first example, convert the JSIDL in one of the test subdirectories.

$ python ./jsidl2idl.py -i test/test001/test001.xml
```
module CommandClass {
  // @JAUS(id="urn:jaus:test001:MessageSet:CommandClass", version="1.0")

  // //// message ////////////////////////////////////////////////////////////
  module SimpleMessage {
    // @JAUS(message,id=B001)
    // A SimpleMessage sends a single 32-bit signed integer.
    typedef struct JausAddress {
      unsigned short SubsystemID;
      octet NodeID;
      octet ComponentID;
    } JausAddress_;
    module header {
      typedef struct HeaderRec {
        unsigned short MessageID;
      } HeaderRec_;
    };
    module body {
      module SimpleRecord {
        typedef struct SimpleRecord {
          long SimpleFixedField; // @JAUS(units=one,index=1)
        } SimpleRecord_;
      };
    };
    struct Message {
      JausAddress_ source;
      JausAddress_ destination;
      header::HeaderRec_ JTS_Header;
      body::SimpleRecord::SimpleRecord_ SimpleBody;
    };
#pragma keylist Message
        source.SubsystemID
        source.NodeID
        source.ComponentID
  }; // message: SimpleMessage
};
$
```

Testing
===========

The ddsidl tools comes with a unit test framework to demonstrate
correct conversion of all AS5684 constructs to ARP6227 constructs.

To run the unit tests,
```
$ cd test
$ ./runtests.sh
```
The runtests.sh script runs unittest.sh in each test subdirectory.
The unit tests convert the JSIDL to IDL, then run the validating
parser to confirm that the output is correct.  Last, the unittest.sh
script diffs the output IDL with the expected output and displays the
results.


Validating DDS IDL
====================

This package includes a modified CORBA 3.2 IDL grammmar and validating parser.  See the README.md file in the ../parser subdirectory for instructions and examples.

If you have already created the parser files in ../parser, you can validate the DDS IDL produced by this translator as follows:

```
$ python ./jsidl2idl.py -i test/test001/test001.xml -o test/test001/test001_out.idl
$ python ../parser/dds_idl_parser --rule=specification < test/test001/test001_out.idl
```






