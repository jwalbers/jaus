# README.txt
# 
# Based on: $Id: README.txt 95 2013-08-26 16:27:28Z jalbers $

Valiating parser for DDS IDL produced using the jsidl2idl translator.

INSTALL THE ANTLR 3.1.3 DISTRIBUTION
====================================

This parser uses 3.1.3 since it is the latest release to support Python 2.x.

Download http://www.antlr.org/download/antlr-3.1.3.tar.gz and unpack
into the runtime subdirectory, so you see ./runtime/antlr-3.1.3/antlr.config.

Install the Python runtime in your Python 2.6 or 2.7 release as follows:

```
$ cd runtime/antlr-3.1.3/runtime/Python
$ python setup.py install
```

Open a shell session and change directory to this IDL directory (where this README.txt file resides).

If you install antlr-3.1.3 elsewhere, fix setupjava.sh to point to the right location.


CREATE A PARSER/VALIDATOR
-------------------------

To create a working parser/validator in this directory:

```
$ . setupjava.sh  # set CLASSPATH to point to the antlr-3.1.3 jar files.
$ java org.antlr.Tool dds_idl.g
```
After a succesful parser generation for 'dds_idl', you will see three files:
```
      ./dds_idl.tokens
      ./dds_idlLexer.py
      ./dds_idlParser.py
```


RUN THE PARSER/VALIDATOR
========================

(NOTE: #include processing is not yet supported. See http://www.antlr.org/wiki/pages/viewpage.action?pageId=557057)

Run the validating parser like this:

```
$ python dds_idl_parser --rule=specification < sample.idl
```

This will produce errors where the input file cannot parse, often with an informative error mesage.

You can validate the latest IDL generated for the ICD from the IDL directory with the following shell command:
```
for i in `find ../testing/* -name '*.idl' -print`
do
  echo "------------------------------------------------ $i"
  python dds_idl_parser --rule=specification < $i
done
```

CHANGE DEBUG OUTPUT
===================

If you edit the grammar file ucs_idl_2_1_dds_xtypes.g, you can change the DEBUG_LEVEL value.  Higher is more debug output, lower is less debug output.

If you want to add debug code, just follow the existing examples in the grammar file.


KNOWN ISSUES:

$ java org.antlr.Tool dds_idl.g
warning(200): dds_idl.g:717:2: Decision can match input such as "'0'..'9'{'E', 'e'}{'+', '-'}'0'..'9'{'D', 'F', 'd', 'f'}" using multiple alternatives: 3, 4
As a result, alternative(s) 4 were disabled for that input
error(208): dds_idl.g:723:1: The following token definitions can never be matched because prior tokens match the same input: FIXED_PT_LITERAL

