# Run this file with '.' from the cjsidl root directory
#
ANTLRLIB=`pwd`/antlr-3.1.3/lib
CLSPATH=".:$ANTLRLIB/antlr-3.1.3.jar:$ANTLRLIB/antlr-runtime-3.1.3.jar:$ANTLRLIB/gunit.jar:$ANTLRLIB/stringtemplate-3.2.jar"

if [ "x$OSTYPE" = "xcygwin" ]; then
    export CLASSPATH=`cygpath -w -p $CLSPATH`
else
    export CLASSPATH=$CLSPATH
fi