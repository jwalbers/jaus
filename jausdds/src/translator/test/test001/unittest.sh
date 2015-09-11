# unittest.sh
#
# Simple script to run one unit test.
#
# $Id$
#
TRANSLATOR='../../jsidl2idl.py'
PARSER='../../../parser/dds_idl_parser'
TEST_PATH=`pwd`
TEST_NAME=`basename $TEST_PATH`
RESULT="$TEST_NAME: "

# echo 'Translating ..............'
python $TRANSLATOR --in ${TEST_NAME}.xml --out ${TEST_NAME}_gen.idl

# echo 'Validating DDS IDL'
$PARSER --rule=specification < ${TEST_NAME}_gen.idl > $TEST_PATH/parse.out

if [ `wc -c $TEST_PATH/parse.out` -eq 0 ]; then
    RESULT="$RESULT VALID DDS IDL,"
else
    RESULT="$RESULT DDS IDL PARSER ERRORS,"
fi

if $PARSER --rule=specification < ${TEST_NAME}_gen.idl; then RESULT="$RESULT VALID DDS IDL,"; fi

# echo 'Comparing with expected results'
# Later, diff -w?
if diff ${TEST_NAME}_gen.idl ${TEST_NAME}.idl; then RESULT="$RESULT PASS"; fi

echo $RESULT


