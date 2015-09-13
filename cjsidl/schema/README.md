This directory contains both Compact and XML forms of current and historical JSIDL schema.

To convert a Compact .rnc file to an XML .rng file, use trang.

java -jar trang.jar -I rnc -O rng <input_filename> <output_filename>

For example:
```
java -jar trang.jar jsidl_v1_1B.rnc jsidl_v1_1B.rng
```
