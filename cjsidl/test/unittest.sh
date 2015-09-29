#!/usr/bin/env bash
#
# This test executes a series of translations as a general check of the tools.
# This is not an exhaustive test, but we will add test cases as issues are 
# reported.
#

# Setup antlr and java environment.  Must run the setupjava.sh script in root dir.
(cd ..; . setupjava.sh)

export CJSIDL_INCLUDE=./include
# Specify a Relax NG XML schema file (.rng suffix)
SCHEMA=jsidl_v1_1B.rng

TESTFILES=
for i in jsidl/*.xml
do
    fname=`basename $i | sed 's/.xml//'`
    if ! [ $fname = 'schemas' ]; then
        echo "------------------------------------------Translating JSIDL -> CJSIDL" ${fname}.xml
        python ../bin/jsidl2jaus.py --in $i --out jaus/${fname}.jaus
        TESTFILES+=" $fname"
    fi
done

# Output dir for converted JSIDL files.
if ! [ -d xml ]; then
    mkdir xml
fi

# Disable use of old broken test files for now.
XTESTFILES=''
XTESTFILES+=" 6091_AckermanDriver \
           BasicTypeSet \
           MissionSpooler \
           include_test_1 \
           DigitalAudioSensor \
           MissionManagement \
           6091_PlatformSpecificationsTypes \
           6111_PlatformSpecifications \
           5710A_Transport"
for i in $TESTFILES
do
    echo "------------------------------------------Translating and validating " ${i}.jaus
    # jaus2jsidl is executable so really don't need python, but works better w/ cygwin
    python ../grammar/jaus2jsidl --rule=jaus < jaus/${i}.jaus > xml/${i}.xml
    xmllint --relaxng ../schema/$SCHEMA xml/${i}.xml | grep ${i}.xml
done
