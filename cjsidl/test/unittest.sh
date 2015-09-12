#!/usr/bin/env bash
#
# This test executes a series of translations as a general check of the tools.
# This is not an exhaustive test, but we will add test cases as issues are 
# reported.
#

# Setup antlr and java environment
. ../setupjava.sh

export CJSIDL_INCLUDE=./include

# jaus2jsidl is executable so really don't need python, but works better w/ cygwin
#
if ! [ -d xml ]; then
    mkdir xml
fi

for i in 6091_AckermanDriver BasicTypeSet MissionSpooler include_test_1 DigitalAudioSensor MissionManagement 6091_PlatformSpecificationsTypes 6111_PlatformSpecifications_init 5710A_Transport
do
    echo "------------------------------------------Translating and validating " ${i}.jaus
    python ../grammar/jaus2jsidl --rule=jaus < jaus/${i}.jaus > xml/${i}.xml
    xmllint --relaxng ../schema/jsidl_plus.rng xml/${i}.xml | grep ${i}.xml
done
