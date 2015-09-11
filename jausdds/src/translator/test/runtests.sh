# runtest.sh
#
# Simple framework to run unittests for JSIDL to DDS IDL translator.
#
# $Id$
#
TEST_DIRS='test001 test002 test003'
for td in $TEST_DIRS
do
    cd $td
    ../unittest.sh
    cd ..
done