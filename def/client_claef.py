#!/usr/bin/env python3
#
# LOAD or RELOAD (if already exists) the C-LAEF suite
#
# C. Wastl, 2019-04-11
###################################################

import ecflow

try:
    ci = ecflow.Client()
#    ci.load("claef.def")
    ci.suspend("/claef")  # so that we can resume manually in ecflow_ui
    ci.replace("/claef", "claef.def")
    ci.begin_suite("/claef")

except RuntimeError as e:
    print ("(!) Failed:"),   e
