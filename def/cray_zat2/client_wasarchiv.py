#!/usr/bin/env python3
#
# LOAD or RELOAD (if already exists) the WASARCHIV suite
#
# C. Wastl, 2019-01-15
###################################################

import ecflow

try:
    ci = ecflow.Client()
    #ci.load("wasarchiv.def")
    ci.suspend("/wasarchiv")  # so that we can resume manually in ecflow_ui
    ci.replace("/wasarchiv", "wasarchiv.def")
    ci.begin_suite("/wasarchiv")

except RuntimeError as e:
    print ("(!) Failed:"),   e
