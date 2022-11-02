#!/usr/bin/env python3
#
# LOAD or RELOAD (if already exists) the C-LAEF suite
#
# C. Wastl, 2019-01-15
###################################################

import ecflow

try:
    ci = ecflow.Client()
    #ci.load("sumo.def")
    ci.suspend("/sumo")  # so that we can resume manually in ecflow_ui
    ci.replace("/sumo", "sumo.def")
    ci.begin_suite("/sumo")

except RuntimeError as e:
    print ("(!) Failed:"),   e
