#!/bin/bash
PWDIR=`echo $PWD`
export PATH=$PATH:$PWDIR
#python3 scripts/run_test_suite.py conf/ut/ut_test.conf suite/ut/ut_test.conf
#python3 scripts/run_test_suite.py conf/archeros.conf suite/network.conf
python3 scripts/run_test_suite.py conf/lcm/lishizhen.conf suite/lcm.conf
