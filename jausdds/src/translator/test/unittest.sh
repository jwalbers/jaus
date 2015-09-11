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
$PARSER --rule=specification < ${TEST_NAME}_gen.idl &> $TEST_PATH/parse.out

if [ -s $TEST_PATH/parse.out ]; then
    cat $TEST_PATH/parse.out
    RESULT="$RESULT DDS IDL PARSER ERRORS,"
else
    RESULT="$RESULT VALID DDS IDL,"
fi

# echo 'Comparing with expected results'
# Later, diff -w?
if diff ${TEST_NAME}_gen.idl ${TEST_NAME}.idl; then
  RESULT="$RESULT PASS"
else
  RESULT="$RESULT FAIL"
fi

echo $RESULT


