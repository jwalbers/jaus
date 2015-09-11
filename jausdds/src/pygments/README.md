# README.md

The scripts in this directory run the pygments syntax colorizer on XML or IDL input source to produce syntax colored RTF files that can be used in Word documents.

This initial set of scripts needs to be tuned for CORBA 3.2 IDL, and needs to reflect specific coloring styles (or custom coloring) that the JAUS/DDS team decides on going forward.

To use the scripts:

1. Install Python 2.7.
2. Install the latest Pygments package for Python 2.7.
3. Convert XML files:
```
    python xml2rtf.py <filename>.xml
```

4. Convert IDL files:
```
    python idl2rtf.py <filename>.idl
```


For example the text used in Table 1 of ARP6227.doc is created as:

```
    python idl2rtf.py idlsample.idl
    python xml2rtf.py xmlsample.xml
```

