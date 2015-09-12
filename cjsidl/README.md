cjsidlTools - Tools for working with Compact JSIDL for AS-4 JAUS
================================================================

Copyright 2011-2015 Jim Albers

Last updated: Sat Sep 12 09:32:26 CDT 2015

Last tested with: Python 2.7.5 and Java 1.7.0_45

Help
============

If your installation is successful and you are having issues, please
take a close look at the contents of the ./test directory.  Make sure
you can run the unittest.sh script and get the results shown in
test/README.txt.

Developers
============

Do not commit any changes to the cjsidl repository unless your
code passes the ./test/unittest.sh.

If you discover and fix any bugs, make sure to add to the unit test a
.jaus file that demonstrates the bug, and shows that it is resolved.

Known Issues
============

1. If the CJSIDL_INCLUDE path includes the current directory, and an
include file is found in the current directory, it will be included
twice.

Workaround: keep all include files in as separate ./include subdirectory.
See how the ./test unit test subdir is set up.

2. The Translator does not yet handle namespaces completely, so type
references like 'CoreTypes.TimeStamp' are not (yet) properly resolved.

Workaround: See how the .jaus files in ./test use the include file
./test/include/BasicTypes.jaus.

In particular, for the AS5710 core types, you should use
BasicTypes.jaus as shown in the test .jaus files.


Installation
============

Prerequisites:

Python 2.5/2.6/2.7
Java 1.5 or later

Python lxml etree package (for DOM processing)

Install setuptools (http://pypi.python.org/pypi/setuptools), then:
```
$ easy_install lxml==3.2.3
```
You also need to install the Antlr3 3.1.3 Python runtime.
```
$ wget http://www.antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz
$ tar xvf antlr_python_runtime-3.1.3.tar.gz
$ cd antlr_python_runtime-3.1.3/
$ sudo python setup.py install
```
Test the installation by starting a Python interpreter, importing the antlr3 module, and confirming there are no errors.
```
Python 2.7.10 (default, May 25 2015, 13:06:17) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.56)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import antlr3
>>> 
```
Install the Java libraries for the Antlr3 tools
```
$ wget http://www.antlr3.org/download/antlr-3.1.3.tar.gz
$ tar zxvf antlr-3.1.3.tar.gz
```

If you unpack the antlr-3.1.3.tar.gz other than in the cjsidl
directory, edit the setupjava.sh script to set the appropriate java
classpath.

Have a current Java JRE in your path and check with the 'java -version' command.
```
$ java -version
java version "1.7.0_45"
Java(TM) SE Runtime Environment (build 1.7.0_45-b18)
Java HotSpot(TM) 64-Bit Server VM (build 24.45-b08, mixed mode)
```
Create the Parser/Translator Utility
====================================

To create the jaus2jsidl translator, run the antlr Tool on the grammar file.  The warning is expected in this version.
```
$ . setupjava.sh
$ ( cd grammar; java org.antlr.Tool jaus2jsidl.g )
ANTLR Parser Generator  Version 3.1.1
warning(200): jaus2jsidl.g:1936:66: Decision can match input such as "SL_COMMENT" using multiple alternatives: 1, 2
As a result, alternative(s) 2 were disabled for that input
```

This will produce the three files: 
     grammar/jaus2jsidl.tokens
     grammar/jaus2jsidlLexer.py
     grammar/jaus2jsidlParser.py

Translating CJSIDL to JSIDL -- Using the Parser/Translator directly
===================================================================

Run the translator by specifying the input and output:
```
$ python jaus2jsidlParser.py --rule=jaus < CJSIDL FILE > JSIDL_FILE
```
For example:
```
$ python jaus2jsidlParser.py --rule=jaus < ../test/6091_AckermanDriver.jaus > ../test/6091_AckermanDriver.xml
```
Translating CJSIDL to JSIDL -- Using the jaus2jsidl wrapper
===========================================================

The jaus2jsidl wrapper is used exactly like the Parser/Translator jaus2jsidlParser.py.

However, this wrapper will include referenced text files in-line
whenever it sees a directive like:

// #include <filename>

The environment variable CJSIDL_INCLUDE optionally provides a search
path for <filename>.  For example, with a current checkout, you can
run the following test:
```
$ export CJSIDL_INCLUDE=../test:/work/as6091
$ python jaus2jsidl --rule=jaus < ../test/include_test_1.jaus > ../test/out.xml
Processing #include include_test_1_1.jaus
Found include file=..\test\include_test_1_1.jaus
Processing #include include_test_1_1_1.jaus
Found include file=..\test\include_test_1_1_1.jaus
```
The CJSIDL_INCLUDE can be either in DOS or UNIX format, so this method
should work under bash/linux, bash/cygwin, or cmd.exe.

This particular test used bash/cygwin with sys.platform == 'win32'
(hence os.sep == '\\').

Translating from JSIDL XML to CJSIDL
====================================

To reverse-engineer a collection of XML, go to the root of the XML
directory, and run normalize_jsidl.py.  This will process all the .xml
files in the directory and its subdirectories, and for each
<service_def/> found, will create a file named
<service_name>Normalized.xml.

A normalized service definition file is self-contained with a complete
set of definitions to define the service.

As part of normalization, the normalize_jsidl.py script will find
record, list, variant, and sequence elements that have common names,
move the definitions into a declared_type_set section, and used
'declared_*_def' elements in the messages to improve readability and
remove redundancy.

NOTE: the script assumes that if there are two elements with exactly
the same name, they will have a common definition.  The script will
report any inconsistencies.

For example:
```
$ cd $AS4DOCS/AS5710_JSS/urn.jaus.jss.core
$ python normalize_jsidl.py .
... diagnostic/progress output & error messages ...
$ ls -l *Normalized*
-rwxr-xr-x 1 jalbers None 30721 2011-01-06 08:59 AccessControlNormalized.xml
-rwxr-xr-x 1 jalbers None 30067 2011-01-06 08:59 DiscoveryNormalized.xml
-rwxr-xr-x 1 jalbers None 27059 2011-01-06 08:59 EventsNormalized.xml
-rwxr-xr-x 1 jalbers None 23807 2011-01-06 08:59 ListManagerNormalized.xml
-rwxr-xr-x 1 jalbers None  2623 2011-01-06 08:59 LivenessNormalized.xml
-rwxr-xr-x 1 jalbers None 23479 2011-01-06 08:59 ManagementNormalized.xml
-rwxr-xr-x 1 jalbers None  6365 2011-01-06 08:59 TimeNormalized.xml
-rwxr-xr-x 1 jalbers None 13133 2011-01-06 08:59 TransportNormalized.xml
```

Each of these files can be converted into a standalone .jaus file, thus:
```
$ cd ..; mkdir CJSIDL; cd CJSIDL
$ for i in ../Normalized/*Normalized.xml; do bn=`basename $i`; jausn=`echo $bn | sed 's/.xml/.jaus/'`; python c:/Users/jalbers/svn/jalbers/fastpilot/cjsidlTools/bin/jsidl2jaus.py --in $i --out $jausn; done
$ ls -l *.jaus
-rwxr-xr-x 1 jalbers None 15031 2011-01-06 09:02 AccessControlNormalized.jaus
-rwxr-xr-x 1 jalbers None 18051 2011-01-06 09:02 DiscoveryNormalized.jaus
-rwxr-xr-x 1 jalbers None 14958 2011-01-06 09:02 EventsNormalized.jaus
-rwxr-xr-x 1 jalbers None 13864 2011-01-06 09:02 ListManagerNormalized.jaus
-rwxr-xr-x 1 jalbers None  1504 2011-01-06 09:02 LivenessNormalized.jaus
-rwxr-xr-x 1 jalbers None 11741 2011-01-06 09:02 ManagementNormalized.jaus
-rwxr-xr-x 1 jalbers None  3520 2011-01-06 09:02 TimeNormalized.jaus
-rwxr-xr-x 1 jalbers None  7201 2011-01-06 09:02 TransportNormalized.jaus
```
IMPORTANT NOTE: Round-tripping CJSIDL files does not preserve the multi-file, hierarchical organization of some JSIDL XML filesets.

Future versions of CJSIDL will support declared_type_sets.

Validating JSIDL XML
====================

This package includes an RNG schema taken from a recent JTS release.  The files schema/jsidl_plus.rnc is the master, schema/jsidl_plus.rng is the XML formatted version of same created using the trang utility.

To validate a JSIDL XML file, make sure that you have a working xmllint utility installed, then:
```
$ xmllint --relaxng schema/jsidl_plus.rng <myfile>
```
The xmllint utility dumps a pretty-printed output of the XML and reports on its validity.  To get just the result:
```
$ xmllint --relaxng schema/jsidl_plus.rng <myfile> | grep <myfile>
```
For example:
```
$ xmllint --relaxng ../schema/jsidl_plus.rng AS5710BasicTypes.xml | grep AS5710BasicTypes.xml
AS5710BasicTypes.xml validates
```

Sample Session, Including git clone
===================================
```
/work $ git clone ssh://git@<host.domain>/cjsidlTools.git
Cloning into cjsidlTools...
remote: Counting objects: 824, done.        
remote: Compressing objects: 100% (638/638), done.        
remote: Total 824 (delta 282), reused 627 (delta 162)        
Receiving objects: 100% (824/824), 6.61 MiB | 317 KiB/s, done.
Resolving deltas: 100% (282/282), done.
/work/ $ cd cjsidlTools
/work/cjsidlTools $ . setupjava.sh
/work/grammar $ (cd ./grammar; java org.antlr.Tool jaus2jsidl.g)
ANTLR Parser Generator  Version 3.1.1
warning(200): jaus2jsidl.g:1765:66: Decision can match input such as "SL_COMMENT" using multiple alternatives: 1, 2
As a result, alternative(s) 2 were disabled for that input
/work/cjsidlTools $ (cd test; ./unittest.sh)
------------------------------------------Translating and validating  6091_AckermanDriver.jaus
6091_AckermanDriver.xml validates
------------------------------------------Translating and validating  BasicTypeSet.jaus
BasicTypeSet.xml validates
------------------------------------------Translating and validating  MissionSpooler.jaus
Processing #include BasicTypes.jaus
Found include file=./include/BasicTypes.jaus
MissionSpooler.xml validates
------------------------------------------Translating and validating  include_test_1.jaus
Processing #include include_test_1_1.jaus
Found include file=./include/include_test_1_1.jaus
Processing #include include_test_1_1_1.jaus
Found include file=./include/include_test_1_1_1.jaus
include_test_1.xml validates
------------------------------------------Translating and validating  DigitalAudioSensor.jaus
DigitalAudioSensor.xml validates
------------------------------------------Translating and validating  MissionManagement.jaus
Processing #include BasicTypes.jaus
Found include file=./include/BasicTypes.jaus
MissionManagement.xml validates
```
